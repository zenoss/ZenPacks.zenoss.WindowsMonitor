###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = """WinServiceMap
Collect Windows service information using WMI, which enables monitoring
of Windows services via zenwin.
"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

class WinServiceMap(WMIPlugin):

    compname = "os"
    relname = "winservices"
    modname = "Products.ZenModel.WinService"
    
    attrs = ("name","caption",
             "pathName","serviceType","startMode","startName","state")

    
    def queries(self):
        return {
            "Win32_Service" :
            "Select %s From Win32_Service" % (",".join(self.attrs)),
            }
    
    def process(self, device, results, log):
        """Collect win service info from this device.
        """
        log.info('Processing WinServices for device %s' % device.id)
        
        rm = self.relMap()
        for svc in results["Win32_Service"]:
            om = self.objectMap()
            om.id = prepId(svc.name)
            om.serviceName = svc.name
            om.caption = svc.caption
            om.setServiceClass = {'name':svc.name, 'description':svc.caption}
            for att in self.attrs:
                if att in ("name", "caption", "state"): continue
                setattr(om, att, getattr(svc, att, "")) 
            rm.append(om)
        
        return rm

