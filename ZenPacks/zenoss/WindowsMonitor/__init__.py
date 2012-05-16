###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2012, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__="WindowsMonitor ZenPack"

__import__('pkg_resources').declare_namespace(__name__)

import Globals
import logging
import os.path
from zope.event import notify
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.Zuul.interfaces import ICatalogTool
from Products.Zuul.catalog.events import IndexingEvent

log = logging.getLogger("zen.windowsmonitor")


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

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

    packZProperties =  [
                ('zWinPerfCycleSeconds', 300, 'int'),
                ('zWinPerfCyclesPerConnection', 5, 'int'),
                ('zWinPerfTimeoutSeconds', 10, 'int'),
                ]

    def install(self, app):
        self._removePreviousZenPacks(self.dmd)
        ZenPackBase.install(self, app)
        _addPluginsToDiscovered(self.dmd)

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            _removePluginsFromDiscovered(self.dmd)
        ZenPackBase.remove(self, app, leaveObjects)

    def _removePreviousZenPacks(self, dmd):
        """
        Since this zenpack came from two WinModelerPlugins and ZenWinPerf
        we need to remove the packables from both of those zenpack as well
        as update the class for the WinPerfDataSources that came from ZenWinPerf
        """
        log.info("Removing Packables from previous zenpacks")
        self._movepacks(dmd)
        log.info("Migrating WinPerfDataSources to new class")
        self._migrateWinPerfDataSrouce(dmd)

    def _movepacks(self, dmd):
        """
        Take every pack relationship from WinModeler and ZenWinPerf and move it to this
        zenpack. This normally happens in ZenPackCmd.py when you have one zenpack replacing another.
        """
        packables = []
        try:
            modeler = dmd.ZenPackManager.packs._getOb('ZenPacks.zenoss.WinModelerPlugins')
            if modeler:
                for p in modeler.packables():
                    packables.append(p)
                    modeler.packables.removeRelation(p)
        except AttributeError:
            log.debug("ZenPacks.zenoss.WinModelerPlugins is not installed")
        try:
            zenwinperf = dmd.ZenPackManager.packs._getOb('ZenPacks.zenoss.ZenWinPerf')
            if zenwinperf:
                for p in zenwinperf.packables():
                    packables.append(p)
                    zenwinperf.packables.removeRelation(p)
        except AttributeError:
            log.debug("ZenPacks.zenoss.ZenWinPerf is not installed")
        # we do not need to readd the packable because that will be taken care of
        # in this zenpacks objects.xml
        return packables

    def _persistDataSource(self, datasource):
        """after switching the __class__ attribute, call this function to make the
        change permanent"""
        id = datasource.id
        from cStringIO import StringIO
        xml_file = StringIO()
        datasource.exportXml(xml_file)
        parent = datasource.getPrimaryParent()
        parent._delObject(datasource.id)
        from Products.ZenRelations.ImportRM import NoLoginImportRM
        xml_importer = NoLoginImportRM(parent)
        xml_file.seek(0)
        xml_importer.loadObjectFromXML(xml_file)
        xml_importer.processLinks()
        ds = parent._getOb(id)
        notify(IndexingEvent(ds))

    def _migrateWinPerfDataSrouce(self, dmd):
        from ZenPacks.zenoss.WindowsMonitor.datasources.WinPerfDataSource import WinPerfDataSource
        oldCls = "ZenPacks.zenoss.ZenWinPerf.datasources.WinPerfDataSource.WinPerfDataSource"
        results = ICatalogTool(dmd).search(oldCls)
        log.info("Converting %d datasources", results.total)
        for brain in results:
            obj = brain.getObject()
            obj.__class__ = WinPerfDataSource
            obj._p_changed = True
            self._persistDataSource(obj)
