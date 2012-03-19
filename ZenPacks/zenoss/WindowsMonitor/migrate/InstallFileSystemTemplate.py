######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

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

    
