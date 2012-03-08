######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

__doc__="ZenPack Template"

__import__('pkg_resources').declare_namespace(__name__)

import Globals
import os.path

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase

_discovery_plugins = ('zenoss.wmi.IpInterfaceMap', 'zenoss.wmi.IpRouteMap')

def _addPluginsToDiscovered(dmd):
    # Get a reference to the device class
    dmd = dmd.primaryAq()
    devcls = dmd.Devices.Discovered
    # Only add plugins that aren't already there
    current = tuple(devcls.zCollectorPlugins)
    new = _discovery_plugins
    toadd = tuple(set(new) - set(current))
    if not toadd: return
    newstate = current + toadd
    # Set the zProperty
    devcls.setZenProperty('zCollectorPlugins', newstate)

def _removePluginsFromDiscovered(dmd):
    # Get a reference to the device class
    dmd = dmd.primaryAq()
    devcls = dmd.Devices.Discovered
    current=tuple(devcls.zCollectorPlugins)
    # The intersection of the current plugins for this object
    # and the discovery plugins is what we want to remove
    toremove = tuple( set(current) & set(_discovery_plugins) )
    if not toremove: return
    newstate = tuple( set(current) - set(toremove) )
    devcls.setZenProperty('zCollectorPlugins',newstate)

class ZenPack(ZenPackBase):
    def install(self, app):
        ZenPackBase.install(self, app)
        _addPluginsToDiscovered(self.dmd)

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            _removePluginsFromDiscovered(self.dmd)
        ZenPackBase.remove(self, app, leaveObjects)
