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

import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.ZenPackLoader import ZPLObject
from Products.ZenRelations.Exceptions import ObjectNotFound

class InstallFileSystemTemplate(ZenPackMigration):
    version = Version(2, 1, 3)
    
    def migrate(self, pack):
        devices = pack.dmd.getDmdRoot("Devices")
        # remove the old FileSystem template
        try:
            templates = devices.Server.Windows.WMI.rrdTemplates
            templates.removeRelation(templates.FileSystem)
        except ObjectNotFound:
            pass
        # add the one in objects.xml
        zplo = ZPLObject()
        zplo.load(pack, pack.dmd.getPhysicalRoot())

    
