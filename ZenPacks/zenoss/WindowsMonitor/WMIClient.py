###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, 2008 Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

from ZenPacks.zenoss.PySamba.twisted.callback import WMIFailure
from ZenPacks.zenoss.PySamba.twisted.reactor import eventContext
from ZenPacks.zenoss.PySamba.wbem.Query import Query

from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient

from twisted.internet import defer

import os
import socket
import sys
import logging
log = logging.getLogger("zen.WMIClient")


BaseName = os.path.basename(sys.argv[0])
MyName = None

def _myname():
    global MyName
    if not MyName:
        MyName = BaseName.split('.')[0]
        try:
            os.mkdir(zenPath('var', _myname()))
        except os.error:
            pass
    return MyName

def _filename(device):
    return zenPath('var', _myname(), device)

class BadCredentials(Exception): pass

class WMIClient(BaseClient):

    def __init__(self, device, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
        self.host = device.id
        self._wmi = None
        if socket.getfqdn().lower() == device.id.lower(): 
            self.host = "."
            device.zWinUser = device.zWinPassword = ""
        elif device.manageIp is not None:
            self.host = device.manageIp
        self.name = device.id
        self.user = device.zWinUser
        self.passwd = device.zWinPassword
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def connect(self):
        log.debug("connect to %s, user %r", self.host, self.user)
        if not self.user:
            log.warning("Windows login name is unset: "
                        "please specify zWinUser and "
                        "zWinPassword zProperties before adding devices.")
            raise BadCredentials("Username is empty")
        self._wmi = Query()
        creds = '%s%%%s' % (self.user, self.passwd)
        return self._wmi.connect(eventContext, self.device.id, self.host, creds)


    def close(self):
        if self._wmi:
            self._wmi.close()


    def query(self, queries):
        def inner(driver):
            try:
                queryResult = {}
                for tableName, query in queries.items():
                    query = query.replace ("\\", "\\\\")
                    yield self._wmi.query(query)
                    result = driver.next()
                    queryResult[tableName] = []
                    while 1:
                        more = None
                        yield result.fetchSome()
                        try:
                            more = driver.next()
                        except WMIFailure, ex:
                            msg = 'Received %s from query: %s'
                            
                            # Look for specific errors that should be equated
                            # to an empty result set.
                            if str(ex) in (
                                "NT code 0x80041010",
                                "WBEM_E_INVALID_CLASS",
                                ):
                                log.debug(msg % (ex, query))
                            else:
                                log.error(msg % (ex, query))
                                raise
                        if not more:
                            break
                        queryResult[tableName].extend(more)
                yield defer.succeed(queryResult)
                driver.next()
            except Exception, ex:
                log.debug("Exception collecting query: %s", str(ex))
                raise
        return drive(inner)

    def run(self):
        def inner(driver):
            try:
                yield self.connect()
                driver.next()
                for plugin in self.plugins:
                    pluginName = plugin.name()
                    log.debug("Sending queries for plugin: %s", pluginName)
                    log.debug("Queries: %s" % str(plugin.queries().values()))
                    try:
                        yield self.query(plugin.queries())
                        self.results.append((plugin, driver.next()))
                    except Exception, ex:
                        self.results.append((plugin, ex))
                self.close()
            except Exception, ex:
                log.warn("Unable to collect WMI data from %s: %s",
                         self.device.id, ex)
                self.close()
                raise
        d = drive(inner)
        def finish(result):
            if self.datacollector:
                self.datacollector.clientFinished(self)
        d.addBoth(finish)
        return d


    def getResults(self):
        """Return data for this client
        """
        return self.results
