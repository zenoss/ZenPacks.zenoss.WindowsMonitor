##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, 2012, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


default: egg


egg:
    # setup.py will call 'make build' before creating the egg
	python setup.py bdist_egg


build:


clean:
	rm -rf dist
	rm -rf ZenPacks.zenoss.WindowsMonitor.egg-info
	find . -name '*.pyc' | xargs rm
