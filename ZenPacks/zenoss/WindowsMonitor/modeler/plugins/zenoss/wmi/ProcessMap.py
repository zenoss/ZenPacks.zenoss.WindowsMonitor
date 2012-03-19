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

__doc__ = """ProcessMap
Gather process information using WMI.
Currently not supported.
"""

import re
from sets import Set

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenModel.OSProcess import getProcessIdentifier

class ProcessMap(WMIPlugin):

    maptype = "OSProcessMap" 
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"

    def queries(self):
        return{
        "Win32_Process":"Select * From Win32_Process",
    }
    
    def copyDataToProxy(self, device, proxy):
        WMIPlugin.copyDataToProxy(self, device, proxy)
        processes = device.getDmdRoot("Processes")
        pcs = []
        for pc in processes.getSubOSProcessClassesGen():
            pcProxy = {}
            pcProxy['regex'] = pc.regex
            pcProxy['PrimaryDmdId'] = pc.getPrimaryDmdId()
            pcProxy['ignoreParameters'] = pc.ignoreParameters
            pcs.append(pcProxy)
        setattr(proxy, 'processClasses', pcs)

    def process(self, device, results, log):
        """collect wmi information from this device"""
        
        # TODO: Remove the next two lines when WMI process monitoring is
        # implemented.
        log.warn("WMI process discovery is currently not supported")
        return [self.relMap(),]
        
        log.info('Collecting process information for device %s' % device.id)
        procs = Set()
        maps = []
        rm = self.relMap()
        for p in results['Win32_Process']:
            commandline = getattr(p, 'commandline', p.executablepath)
            if commandline:
                om = self.objectMap()
                fullname = commandline.strip()
                om.procName = fullname.split()[0]
                om.parameters = ' '.join(fullname.split())
                for pc in device.processClasses:
                    if re.search(pc['regex'], fullname):
                        om.setOSProcessClass = pc['PrimaryDmdId']
                        id = getProcessIdentifier(om.procName, None if pc['ignoreParameters'] else om.parameters.strip())
                        om.id = self.prepId(id)
                        if id not in procs:
                            procs.add(id)
                            rm.append(om)
                        break
        maps.append(rm)
        return maps
