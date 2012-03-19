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
from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IWinPerfDataSourceInfo(IInfo):
    name = schema.TextLine(title=_t(u"Name"),
                           xtype="idfield",
                           description=_t(u"The name of this datasource"))
    type = schema.TextLine(title=_t(u"Type"),
                           readonly=True)
    counter = schema.TextLine(title=_t(u"Perf Counter"),
                              description=_t(u"Example: \Memory\Available bytes "))
    enabled = schema.Bool(title=_t(u"Enabled"))
