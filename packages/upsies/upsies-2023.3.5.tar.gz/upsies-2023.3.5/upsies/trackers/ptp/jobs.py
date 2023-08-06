"""
Concrete :class:`~.base.TrackerJobsBase` subclass for PTP
"""

from datetime import datetime

from ... import errors, jobs, utils
from ...utils import cached_property
from ...utils.release import ReleaseType
from ..base import TrackerJobsBase
from ._ptp_tags import PTP_TAGS

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PtpTrackerJobs(TrackerJobsBase):

    @cached_property
    def jobs_before_upload(self):
        return (
            # Common background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,
            self.ptp_group_id_job,

            # Common interactive jobs
            self.type_job,
            self.imdb_job,
            self.title_job,
            self.scene_check_job,

            # Jobs that only run if movie exists on PTP and we add a release

            # Jobs that only run if movie does not exists on PTP yet
            self.year_job,
            self.plot_job,
            self.tags_job,
            self.cover_art_job,
        )

    @cached_property
    def type_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('type'),
            label='Type',
            precondition=self.make_precondition('type_job'),
            autodetect=self.autodetect_type,
            choices=(
                ('Feature Film', 'Feature Film'),
                ('Short Film', 'Short Film'),
                ('Miniseries', 'Miniseries'),
                ('Stand-up Comedy', 'Stand-up Comedy'),
                ('Live Performance', 'Live Performance'),
                ('Movie Collection', 'Movie Collection'),
            ),
            **self.common_job_args(),
        )

    def autodetect_type(self, _):
        if self.release_name.type == ReleaseType.season:
            return 'Miniseries'

        main_video = utils.video.filter_main_videos(
            tuple(utils.video.find_videos(self.content_path))
        )[0]

        # Short film if runtime 45 min or less (Rule 1.1.1)
        if utils.video.duration(main_video) <= 45 * 60:
            return 'Short Film'

    @property
    def imdb_id(self):
        if self.imdb_job.is_finished:
            return self.imdb_job.output[0]

    @cached_property
    def ptp_group_id_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('ptp-group-id'),
            label='PTP Group ID',
            precondition=self.make_precondition('ptp_group_id_job'),
            prejobs=(
                self.imdb_job,
            ),
            worker=self.fetch_ptp_group_id,
            catch=(errors.RequestError,),
            **self.common_job_args(),
        )

    async def fetch_ptp_group_id(self, _):
        assert self.imdb_job.is_finished
        group_id = await self.tracker.get_ptp_group_id_by_imdb_id(self.imdb_id)
        return '' if group_id is None else group_id

    @property
    def ptp_group_id(self):
        """
        PTP group ID if :attr:`ptp_group_id_job` is finished and group ID
        was found, `None` otherwise
        """
        if self.ptp_group_id_job.is_finished:
            if self.ptp_group_id_job.output:
                return self.ptp_group_id_job.output[0]

    @cached_property
    def title_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('title'),
            label='Title',
            precondition=self.make_precondition('title_job'),
            prejobs=(
                self.imdb_job,
            ),
            text=self.fetch_title,
            normalizer=self.normalize_title,
            validator=self.validate_title,
            **self.common_job_args(),
        )

    async def fetch_title(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='title')

    def normalize_title(self, text):
        return text.strip()

    def validate_title(self, text):
        if not text:
            raise ValueError('Title must not be empty')

    @cached_property
    def year_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('year'),
            label='Year',
            precondition=self.make_precondition('year_job'),
            prejobs=(
                self.imdb_job,
            ),
            text=self.fetch_year,
            normalizer=self.normalize_year,
            validator=self.validate_year,
            **self.common_job_args(),
        )

    async def fetch_year(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='year')

    def normalize_year(self, text):
        return text.strip()

    def validate_year(self, text):
        try:
            year = int(text)
        except ValueError:
            raise ValueError('Year is not a number')
        else:
            if not 1800 < year < datetime.now().year + 10:
                raise ValueError('Year is not reasonable')

    @cached_property
    def tags_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('tags'),
            label='Tags',
            precondition=self.make_precondition('tags_job'),
            prejobs=(
                self.imdb_job,
            ),
            text=self.fetch_tags,
            normalizer=self.normalize_tags,
            validator=self.validate_tags,
            **self.common_job_args(),
        )

    async def fetch_tags(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='tags')

    def normalize_tags(self, text):
        tags = [tag.strip() for tag in text.split(',')]
        deduped = list(dict.fromkeys(tags))
        return ', '.join(tag for tag in deduped if tag)

    def validate_tags(self, text):
        for tag in text.split(','):
            if tag.strip() not in PTP_TAGS:
                raise ValueError(f'Tag is not valid: {tag}')

    @cached_property
    def cover_art_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('cover_art'),
            label='Cover Art',
            precondition=self.make_precondition('cover_art_job'),
            prejobs=(
                self.imdb_job,
            ),
            text=self.fetch_cover_art,
            autofinish=True,
            **self.common_job_args(),
        )

    async def fetch_cover_art(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='art')

    @cached_property
    def plot_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('plot'),
            label='Plot',
            precondition=self.make_precondition('plot_job'),
            prejobs=(
                self.imdb_job,
            ),
            text=self.fetch_plot,
            normalizer=self.normalize_plot,
            validator=self.validate_plot,
            autofinish=True,
            **self.common_job_args(),
        )

    async def fetch_plot(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='plot')

    def normalize_plot(self, text):
        return text.strip()

    def validate_plot(self, text):
        if not text:
            raise ValueError('Plot must not be empty')

    @property
    def post_data(self):
        post_data = self._post_data_common

        _log.debug('PTP group ID: %r', self.ptp_group_id)
        if self.ptp_group_id:
            _log.debug('Adding format to existing group')
            post_data.update(self._post_data_add_format)
        else:
            _log.debug('Creating new group')
            post_data.update(self._post_data_add_movie)

        return post_data

    @property
    def _post_data_common(self):
        data = {
            # Feature Film, Miniseries, Short Film, etc
            'type': self.get_job_attribute(self.type_job, 'choice'),
            # Mediainfo and Screenshots
            'release_desc': self.get_job_output(self.description_job, slice=0),

            # Autodetected values
            # 'source': 'Other',  # Custom source
            # 'other_source': ...,
            # 'codec': 'Other',  # Custom codec
            # 'other_codec': ...,
            # 'resolution': ...,  # 1080p, 720p, etc
            # 'other_resolution': ...,  # Custom resolution, e.g. 423x859
            # 'container': 'Other',  # Custom container
            # 'other_container': ...,

            # TODO

            # 'remaster_title': ...,  # Edition Information ("Director's Cut", "Dual Audio", etc.)
            # 'remaster_year': ...,
            # 'remaster_other_input': ...,

            # 'nfo_text': releaseInfo.Nfo,
            # 'subtitles[]': releaseInfo.Subtitles,
            # 'trumpable[]': releaseInfo.Trumpable,

            # Is not main movie (bool)
            'special': '1' if self.options['not_main_movie'] else None,
            # Is personal rip (bool)
            'internalrip': '1' if self.options['personal_rip'] else None,
            # Is scene Release (bool)
            'scene': '1' if self.get_job_attribute(self.scene_check_job, 'is_scene_release') else None,

            # Upload token from staff
            'uploadtoken': self.options['upload_token'] if self.options['upload_token'] else None,
        }

        # Tick "Edition Information" checkbox?
        if any(key in data for key in (
                'remaster_year',
                'remaster_title',
                'remaster_other_input',
        )):
            data['remaster'] = '1'

        return data

    @property
    def _post_data_add_format(self):
        return {
            'groupid': self.ptp_group_id,
        }

    @property
    def _post_data_add_movie(self):
        post_data = {
            'imdb': self.tracker.normalize_imdb_id(self.imdb_id),
            'title': self.get_job_output(self.title_job, slice=0),
            'year': self.get_job_output(self.year_job, slice=0),
            'album_desc': self.get_job_output(self.plot_job, slice=0),
            'tags': self.get_job_output(self.tags_job, slice=0),
            # 'trailer': ...,
            'image': self.get_job_output(self.cover_art_job, slice=0),
        }

        # TODO: Send artists
        # # ???: For some reason PtpUploader uses "artist" and "importance" in the
        # #      POST data while the website form uses "artists", "importances"
        # #      and "roles".
        # artists = self.get_job_output(self.artists_job):
        # if artists:
        #     post_data['artist'] = []
        #     post_data['importance'] = []
        #     for name in artists:
        #         # `importance` is the artist type:
        #         # 1: Director
        #         # 2: Writer
        #         # 3: Producer
        #         # 4: Composer
        #         # 5: Actor
        #         # 6: Cinematographer
        #         post_data['importance'].append('1')
        #         post_data['artist'].append(name)
        #         post_data['role'].append(name)

        return post_data

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)
