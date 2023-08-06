"""
Wrapper for ``mediainfo`` command
"""

from .. import errors, utils
from . import JobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class MediainfoJob(JobBase):
    """
    Get output from ``mediainfo`` command

    See :func:`.utils.video.mediainfo` for more information.
    """

    name = 'mediainfo'
    label = 'Mediainfo'

    # Don't show mediainfo output in TUI. It is printed out to stdout if this is
    # the only/final job.
    hidden = True

    @property
    def cache_id(self):
        """Final segment of `content_path`"""
        return utils.fs.basename(self._content_path)

    def initialize(self, *, content_path, from_all_videos=False):
        """
        Set internal state

        :param content_path: Path to video file or directory that contains a
            video file
        :param bool from_all_videos: Whether to get ``mediainfo`` output from
            each video file or only from the first video

            See :func:`.video.find_videos` for more information.
        """
        self._content_path = content_path
        self._from_all_videos = from_all_videos

    def execute(self):
        """Call ``mediainfo`` in an asynchronous thread"""
        self.attach_task(
            coro=self._get_mediainfo(from_all_videos=self._from_all_videos),
            finish_when_done=True,
        )

    async def _get_mediainfo(self, *, from_all_videos):
        if from_all_videos:
            method = self._get_mediainfo_from_all_videos
        else:
            method = self._get_mediainfo_from_first_video

        # Run synchronous function in thread to make it asynchronous
        loop = utils.get_aioloop()
        await loop.run_in_executor(None, method)

    def _get_mediainfo_from_first_video(self):
        try:
            mediainfo = utils.video.mediainfo(self._content_path, only_first=True)
        except errors.ContentError as e:
            self.error(e)
        else:
            self.send(mediainfo)

    def _get_mediainfo_from_all_videos(self):
        try:
            mediainfos = utils.video.mediainfo(self._content_path, only_first=False)
        except errors.ContentError as e:
            self.error(e)
        else:
            for mediainfo in mediainfos:
                self.send(mediainfo)
