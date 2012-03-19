###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2008, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import string

_transTable = string.maketrans("#()/", "_[]_")

def standardizeInstance(rawInstance):
    """
    Convert a raw perfmon instance name into a standardized one by replacing
    unfriendly characters with one that Windows expects.
    """
    return rawInstance.translate(_transTable)

