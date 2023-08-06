"""
Concrete :class:`~.base.TrackerConfigBase` subclass for PTP
"""

import base64

from ...utils import argtypes, configfiles, imghosts, types
from ..base import TrackerConfigBase


class PtpTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly9wYXNzdGhlcG9wY29ybi5tZQ==').decode('ascii'),
        'username': '',
        'password': '',
        'announce_url': configfiles.config_value(
            value='',
            description='Your personal announce URL.',
        ),
        'source': 'PTP',
        'image_host': types.Choice('ptpimg', options=imghosts.imghost_names()),
        'screenshots': configfiles.config_value(
            value=types.Integer(3, min=3, max=10),
            description='How many screenshots to make.',
        ),
        'exclude': (
            r'\.(?i:nfo|txt|jpg|jpeg|png|sfv|md5)$',
            r'/(?i:sample|extra|bonus|feature)',
            r'(?i:sample\.[a-z]+)$',
        ),
    }

    argument_definitions = {
        'submit': {
            ('--not-main-movie', '--nmm'): {
                'help': 'Upload ONLY contains extras, Rifftrax, Workprints',
                'action': 'store_true',
            },
            ('--personal-rip', '--pr'): {
                'help': 'Tag as your own encode',
                'action': 'store_true',
            },
            ('--screenshots', '--ss'): {
                'help': ('How many screenshots to make '
                         f'(min={defaults["screenshots"].min}, '
                         f'max={defaults["screenshots"].max})'),
                'type': argtypes.number_of_screenshots(
                    min=defaults['screenshots'].min,
                    max=defaults['screenshots'].max,
                ),
            },
            ('--upload-token', '--ut'): {
                'help': 'Upload token from staff',
            },
        },
    }
