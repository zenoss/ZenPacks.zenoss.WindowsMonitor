###########################################################################
#
# Copyright 2010 Zenoss, Inc.  All Rights Reserved.
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
