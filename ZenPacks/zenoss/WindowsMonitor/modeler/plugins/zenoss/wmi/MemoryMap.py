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

__doc__="""MemoryMap

Uses WMI to map memory information on memory objects

"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId
from Products.DataCollector.plugins.DataMaps import ObjectMap

class MemoryMap(WMIPlugin):

    maptype = "MemoryMap" 
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    compname = "os"
        
    attrs = (
        'TotalVisibleMemorySize',
        'TotalVirtualMemorySize',
    )

    def queries(self):
        return {
     "Win32_OperatingSystem": \
     "Select %s From Win32_OperatingSystem" % ",".join(self.attrs),
    }
        
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        maps = []
        
        for record in results["Win32_OperatingSystem"]:
            if record.TotalVisibleMemorySize:
                totalMemory = int(record.TotalVisibleMemorySize) * 1024
                maps.append(ObjectMap({"totalMemory": totalMemory}, compname="hw")) 
            if record.TotalVirtualMemorySize:
                totalSwap = int(record.TotalVirtualMemorySize) * 1024
                maps.append(ObjectMap({"totalSwap": totalSwap}, compname="os"))
        
        return maps
