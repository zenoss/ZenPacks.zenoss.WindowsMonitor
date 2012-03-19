######################################################################
#
# Copyright 2007, 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

default: egg


egg:
    # setup.py will call 'make build' before creating the egg
	python setup.py bdist_egg


build:


clean:
	rm -rf dist
	rm -rf ZenPacks.zenoss.WindowsMonitor.egg-info
	find . -name '*.pyc' | xargs rm
