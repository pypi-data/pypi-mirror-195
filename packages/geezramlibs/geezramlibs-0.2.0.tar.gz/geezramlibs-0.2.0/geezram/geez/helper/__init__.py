import os
import sys
from pyrogram import Client

from geezram.geez.helper.adminHelpers import *
from geezram.geez.helper.aiohttp_helper import*
from geezram.geez.helper.basic import *
from geezram.geez.helper.constants import *
from geezram.geez.helper.data import *
from geezram.geez.helper.inline import *
from geezram.geez.helper.interval import *
from geezram.geez.helper.parser import *
from geezram.geez.helper.PyroHelpers import *
from geezram.geez.helper.utility import *
from geezram.geez.helper.what import *
from geezram.geez.helper.pluginhelper import *

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Geez"])

