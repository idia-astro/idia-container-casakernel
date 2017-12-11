#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Refactored minimalist casapy

We want to execute CASA tools in an a singular environment.  All the machinery for dealing
with a variety of operating systems and environments isn't necessary when using containers
and removing it streamlines the startup and execution process, saving time and resources. 

Example:
    Compute the payment on a loan::

        $ python interest_calculator.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Todo:
    * Do total interest
"""

import os
import sys
import time

try:
    os.setpgid(0,0)
except OSError, e:
    print "setgpid( ) failed: " + e.strerror
    print "                   processes may be left dangling..."


import casac
import matplotlib
# from asap_init import *
# This module is basically a dat file with build details
import casadef

# Why is this here?
homedir = os.getenv('HOME')

'''
global variable:
	casa: Apparently we need global variables for each independent CASA tool.  Rather than remove 
	this from the tools, let's define them here for now.
'''
casa = { 'build': {
             'time': casadef.build_time,
             'version': casadef.casa_version,
             'number': casadef.subversion_revision
         },
         'source': {
             'url': casadef.subversion_url,
             'revision': casadef.subversion_revision
         },
         'helpers': {
             'crashPoster' : 'CrashReportPoster',
             'logger': 'casalogger',
             'viewer': 'casaviewer',
             'info': None,
             'dbus': None,
             'ipcontroller': None,
             'ipengine': None
         },
         'dirs': {
             'rc': homedir + '/.casa',
             'data': None,
             'recipes': None,
             'root': None,
             'python': None,
             'pipeline': None,
             'xml': None
         },
         'flags': { },
         'files': { 
             'logfile': os.getcwd( ) + '/casa-'+time.strftime("%Y%m%d-%H%M%S", time.gmtime())+'.log'
         },
         'state' : {
             'startup': True,
             'unwritable': set( )
         }
       }
       
## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
## set up casa root
## ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
if os.environ.has_key('CASAPATH') :
    __casapath__ = os.environ['CASAPATH'].split(' ')[0]
    __casaarch__ = os.environ['CASAPATH'].split(' ')[1]
    if not os.path.exists(__casapath__ + "/data") :
        print "DEBUG: CASAPATH = %s" % (__casapath__)
        raise RuntimeError, "Unable to find the data repository directory in your CASAPATH. Please fix."
    else :
        casa['dirs']['root'] = __casapath__
        casa['dirs']['data'] = __casapath__ + "/data"
        if os.path.exists(__casapath__ + "/" + __casaarch__ + "/python/2.7/assignmentFilter.py"):
            casa['dirs']['python'] = __casapath__ + "/" + __casaarch__ + "/python/2.7"
        elif os.path.exists(__casapath__ + "/lib/python2.7/assignmentFilter.py"):
            casa['dirs']['python'] = __casapath__ + "/lib/python2.7"
        elif os.path.exists(__casapath__ + "/Resources/python/assignmentFilter.py"):
            casa['dirs']['python'] = __casapath__ + "/Resources/python"

        if casa['dirs']['python'] is not None:
            casa['dirs']['recipes'] = casa['dirs']['python'] + "/recipes"

        if os.path.exists(__casapath__ + "/" + __casaarch__ + "/xml"):
            casa['dirs']['xml'] = __casapath__ + "/" + __casaarch__ + "/xml"
        elif os.path.exists(__casapath__ + "/xml"):
            casa['dirs']['xml'] = __casapath__ + "/xml"
        else:
            raise RuntimeError, "Unable to find the XML constraints directory in your CASAPATH"
else :
    __casapath__ = casac.__file__
    while __casapath__ and __casapath__ != "/" :
        if os.path.exists( __casapath__ + "/data") :
            break
        __casapath__ = os.path.dirname(__casapath__)
    if not os.path.exists(__casapath__ + "/data") :
        raise RuntimeError, "casa path could not be determined"
    else :
        casa['dirs']['root'] = __casapath__
        casa['dirs']['data'] = __casapath__ + "/data"
        if os.path.exists(__casapath__ + "/" + __casaarch__ + "python/2.7/assignmentFilter.py"):
            casa['dirs']['python'] = __casapath__ + "/" + __casaarch__ + "/python/2.7"
        elif os.path.exists(__casapath__ + "/lib/python2.7/assignmentFilter.py"):
            casa['dirs']['python'] = __casapath__ + "/lib/python2.7"
        elif os.path.exists(__casapath__ + "/Resources/python/assignmentFilter.py"):
            casa['dirs']['python'] = __casapath__ + "/Resources/python"

        if casa['dirs']['python'] is not None:
            casa['dirs']['recipes'] = casa['dirs']['python'] + "/recipes"

        if os.path.exists(__casapath__ + "/" + __casaarch__ + "/xml"):
            casa['dirs']['xml'] = __casapath__ + "/" + __casaarch__ + "/xml"
        elif os.path.exists(__casapath__ + "/xml"):
            casa['dirs']['xml'] = __casapath__ + "/xml"
        else:
            raise RuntimeError, "Unable to find the XML constraints directory in your CASAPATH"



# ----------------------------------------------------------------------------------------
# Wrap Tasks
# ----------------------------------------------------------------------------------------

from functools import wraps

def set_parameter_if_not_exists(task, param, value, args, kwargs):
    pos = inspect.getargspec(task)[0].index(param)
    if (len(args) <= pos) and (param not in kwargs):
        kwargs[param] = value
        return True
    return False

def set_parameter(task, param, value, args, kwargs):
    pos = inspect.getargspec(task)[0].index(param)
    if (len(args) > pos):
        args[pos] = value
    else:
        kwargs[param] = value

def get_parameter(task, param, args, kwargs):
    pos = inspect.getargspec(task)[0].index(param)
    if (len(args) > pos):
        return args[pos]
    elif param in kwargs:
        return kwargs[param]
    return None


# Wraps tasks which have the 'listfile' argument. If the user has not already
# set 'listfile' then we supply our own and print the result to the screen.
def wrap_listfile(task):
    def print_logfile(filename):
        f = open(filename, 'r')
        line = f.readline()
        while line != "":
            print line,
            line = f.readline()
        f.close()

    @wraps(task)
    def wrapped_task(*args, **kwargs):
        tempfile = 'casapy_temp.txt'
        print_logfile(tempfile)
        doprint = set_parameter_if_not_exists(task, 'listfile', tempfile, args, kwargs)
        set_parameter(task, 'overwrite', True, args, kwargs)
        # Run task and optionally print results to the screen
        retval = task(*args, **kwargs)
        if retval and doprint:
            print_logfile(tempfile)
        return retval
    return wrapped_task


# print "loading module taskinit"
# from taskinit import *
# print "loading math"
# from math import *
# print "loading tasks_wrapped"
# from tasks_wrapped import *
print "loading parameter_dictionary"
from parameter_dictionary import *
print "loading task_help"
from task_help import *

# 
# print "loading accum"       
# from accum import  accum
# 
# print "task wrapper"
# from tasks_wrapped import *

print "loading all modules"

from accum import  accum
from applycal import  applycal
from asdmsummary import  asdmsummary
from autoclean import  autoclean
from bandpass import  bandpass
from blcal import  blcal
from boxit import  boxit
from browsetable import  browsetable
from calstat import  calstat
from caltabconvert import  caltabconvert
from clean import  clean
from clearcal import  clearcal
from clearplot import  clearplot
from clearstat import  clearstat
from concat import  concat
from conjugatevis import  conjugatevis
from csvclean import  csvclean
from cvel import  cvel
from cvel2 import  cvel2
from deconvolve import  deconvolve
from delmod import  delmod
from exportasdm import  exportasdm
from exportfits import  exportfits
from exportuvfits import  exportuvfits
from feather import  feather
from find import  find
from fixplanets import  fixplanets
from fixvis import  fixvis
from flagcmd import  flagcmd
from flagdata import  flagdata
from flagmanager import  flagmanager
from fluxscale import  fluxscale
from ft import  ft
from gaincal import  gaincal
from gencal import  gencal
from hanningsmooth import  hanningsmooth
from imcollapse import  imcollapse
from imcontsub import  imcontsub
from imfit import  imfit
from imhead import  imhead
from imhistory import  imhistory
from immath import  immath
from immoments import  immoments
from impbcor import  impbcor
from importatca import  importatca
from importasap import  importasap
from importasdm import  importasdm
from importevla import  importevla
from importfits import  importfits
from importfitsidi import  importfitsidi
from importgmrt import  importgmrt
from importmiriad import  importmiriad
from importnro import  importnro
from importuvfits import  importuvfits
from importvla import  importvla
from imrebin import  imrebin
from imreframe import  imreframe
from imregrid import  imregrid
from imsmooth import  imsmooth
from imstat import  imstat
from imsubimage import  imsubimage
from imtrans import  imtrans
from imval import  imval
from imview import  imview
from initweights import  initweights
from listcal import  listcal
from listhistory import  listhistory
from listfits import  listfits
from listobs import  listobs
#listobs = wrap_listfile(listobs)
from listpartition import  listpartition
from listsdm import  listsdm
from listvis import  listvis
#from makemask import  makemask
from mosaic import  mosaic
from msview import  msview
from mstransform import  mstransform
from msuvbin import  msuvbin
from oldhanningsmooth import  oldhanningsmooth
from oldsplit import  oldsplit
from plotants import  plotants
from plotbandpass import  plotbandpass
from plotcal import  plotcal
from plotms import  plotms
# plotms = wrap_plotms(plotms)
from plotuv import  plotuv
from plotweather import  plotweather
from plotprofilemap import  plotprofilemap
from partition import  partition
from polcal import  polcal
from predictcomp import  predictcomp
from impv import  impv
from rmfit import  rmfit
from rmtables import  rmtables
from sdgaincal import  sdgaincal
from setjy import  setjy
from ssoflux import  ssoflux
from simalma import  simalma
from simobserve import  simobserve
from simanalyze import  simanalyze
from slsearch import  slsearch
from smoothcal import  smoothcal
from specfit import  specfit
from specflux import  specflux
from specsmooth import  specsmooth
from splattotable import  splattotable
from split import  split
from spxfit import  spxfit
from statwt import  statwt
from tclean import  tclean
from tclean2 import  tclean2
from testconcat import  testconcat
# from tsdbaseline import  tsdbaseline
# from tsdcal import  tsdcal
# from tsdfit import  tsdfit
# from tsdsmooth import  tsdsmooth
from uvcontsub import  uvcontsub
from uvcontsub3 import  uvcontsub3
from uvmodelfit import  uvmodelfit
from uvsub import  uvsub
#from viewer import  viewer
#viewer = wrap_viewer(viewer)
from wvrgcal import  wvrgcal
from virtualconcat import  virtualconcat
from vishead import  vishead
from visstat import  visstat
from visstat2 import  visstat2
from widebandpbcor import  widebandpbcor
from widefield import  widefield

from split import  split
from hanningsmooth import  hanningsmooth
from tget import *

print "done loading modules"


# from IPython.terminal.embed import InteractiveShellEmbed
# from traitlets.config.loader import Config
# cfg = Config()
# 
# ipshell = InteractiveShellEmbed(user_ns=globals(), config=cfg)
# ipshell()
