###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2008-2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__="""WindowsDeviceMap

Uses WMI to map Windows OS & hardware information

"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.ZenUtils.Utils import prepId
import re

class WindowsDeviceMap(WMIPlugin):

    maptype = "WindowsDeviceMap"
    
    def queries(self):
        return  {
            "Win32_OperatingSystem":"select * from Win32_OperatingSystem",
            "Win32_SystemEnclosure":"select * from Win32_SystemEnclosure",
        }
    
    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)

        om = self.objectMap()
        
        for os in results["Win32_OperatingSystem"]:
            if re.search(r'Microsoft', os.manufacturer, re.I):
                os.manufacturer = "Microsoft"
                os.caption = re.sub(r'\s*\S*Microsoft\S*\s*', '', os.caption)
            
            om.setOSProductKey = MultiArgs(os.caption, os.manufacturer)
            om.snmpSysName = os.csname # lies!
            om.snmpContact = os.registereduser # more lies!
            break

        for e in results["Win32_SystemEnclosure"]:
            om.setHWTag = e.smbiosassettag.rstrip()
            om.setHWSerialNumber = e.serialnumber.rstrip()
            model = e.model
            if not model: model = "Unknown"
            manufacturer = e.manufacturer
            if not manufacturer:
                manufacturer = "Unknown"
            elif re.search(r'Dell', manufacturer):
                manufacturer = "Dell"
            om.setHWProductKey = MultiArgs(model, manufacturer)
            break 

        return om


