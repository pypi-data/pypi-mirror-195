"""Expose the classes in the API."""

import gettext
import locale
import os

LOC = locale.getdefaultlocale()[0]
LOC = 'en_GB'

locales_exe = os.path.join(os.getcwd(), 'locale')
locales_run = '../bfgsupport/bfgsupport/locale'
if os.path.isdir(locales_exe):
    LOCALES_DIRECTORY = locales_exe
else:
    LOCALES_DIRECTORY = locales_run

if not os.path.isdir(LOCALES_DIRECTORY):
    LOCALES_DIRECTORY = '/locale'


translation = gettext.translation('bfg', localedir=LOCALES_DIRECTORY, languages=[LOC], fallback=False)
translation.install()
_ = translation.gettext


from ._version import __version__
VERSION = __version__

from .source.hand import Hand
from .source.comment_xref import CommentXref, convert_text_to_html
from .source.strategy_xref import StrategyXref, strategy_descriptions
from .source.bidding import Bid, Pass, Double
from .source.player import Player
