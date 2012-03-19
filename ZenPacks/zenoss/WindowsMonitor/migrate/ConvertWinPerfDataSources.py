######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackDataSourceMigrateBase
from ZenPacks.zenoss.WindowsMonitor.datasources.WinPerfDataSource \
        import WinPerfDataSource


class ConvertWinPerfDataSources(ZenPackDataSourceMigrateBase):
    version = Version(2, 1, 2)
    
    # These provide for conversion of datasource instances to the new class
    dsClass = WinPerfDataSource
    oldDsModuleName = 'Products.ZenWinPerf.datasources.WinPerfDataSource'
    oldDsClassName = 'WinPerfDataSource'
    
    # Reindex all applicable datasource instances
    reIndex = True
            
