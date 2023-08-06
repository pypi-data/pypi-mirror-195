"""
Print ``mediainfo`` output
"""

from .... import jobs, utils
from .base import CommandBase


class mediainfo(CommandBase):
    """
    Print ``mediainfo`` output

    Directories are recursively searched for the first video file in natural
    order, e.g. "File1.mp4" comes before "File10.mp4".

    Any irrelevant leading parts in the file path are removed from the output.
    """

    names = ('mediainfo', 'mi')

    argument_definitions = {
        'CONTENT': {
            'type': utils.argtypes.content,
            'help': 'Path to release content',
        },
        ('--from-all-videos', '-a'): {
            'action': 'store_true',
            'help': 'Get mediainfo from each video file beneath CONTENT',
        },
    }

    @utils.cached_property
    def jobs(self):
        return (
            jobs.mediainfo.MediainfoJob(
                home_directory=self.home_directory,
                cache_directory=self.cache_directory,
                ignore_cache=self.args.ignore_cache,
                content_path=self.args.CONTENT,
                from_all_videos=self.args.from_all_videos,
            ),
        )
