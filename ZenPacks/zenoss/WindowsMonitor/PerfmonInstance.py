###########################################################################
#
# Copyright 2008 Zenoss, Inc. All Rights Reserved.
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

