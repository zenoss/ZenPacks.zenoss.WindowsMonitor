###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
from Products.Zuul.infos import ProxyProperty
from zope.interface import implements
from Products.Zuul.infos import InfoBase
from ZenPacks.zenoss.WindowsMonitor.interfaces import IWinPerfDataSourceInfo


class WinPerfDataSourceInfo(InfoBase):
    implements(IWinPerfDataSourceInfo)

    @property
    def id(self):
        return '/'.join( self._object.getPrimaryPath() )

    @property
    def source(self):
        return self._object.getDescription()
    
    @property
    def type(self):
        return self._object.sourcetype
    
    counter = ProxyProperty('counter')
    enabled = ProxyProperty('enabled')

    @property
    def testable(self):
        """
        We can test this datasource against a specific windows device
        """
        return True
    


