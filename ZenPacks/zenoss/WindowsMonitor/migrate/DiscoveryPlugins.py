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
import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack
import logging

class DiscoveryPlugins:
    version = Version(2, 0, 6)

    def migrate(self, pack):
        # Get a reference to the device class
        dmd = pack.dmd.primaryAq()
        devcls = dmd.Devices.Discovered
        # Only add plugins that aren't already there
        current = tuple(devcls.zCollectorPlugins)
        new = ('zenoss.wmi.IpInterfaceMap', 'zenoss.wmi.IpRouteMap')
        toadd = tuple(set(new) - set(current))
        newstate = current + toadd
        # Set the zProperty
        devcls.setZenProperty('zCollectorPlugins', newstate)
