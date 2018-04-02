# Prototype python module of simobserve that doesn't use stack variables or the casapy 
# environment

import sys
import os

from task_simobserve import simobserve

class simobserve_wrapper:
	__name__ = "simobserve"

	def __init__(self):
		self.parameters={'project':None, 'skymodel':None, 'inbright':None, 'indirection':None, 'incell':None, 'incenter':None, 'inwidth':None, 'complist':None, 'compwidth':None, 'setpointings':None, 'ptgfile':None, 'integration':None, 'direction':None, 'mapsize':None, 'maptype':None, 'pointingspacing':None, 'caldirection':None, 'calflux':None, 'obsmode':None, 'refdate':None, 'hourangle':None, 'totaltime':None, 'antennalist':None, 'sdantlist':None, 'sdant':None, 'outframe':None, 'thermalnoise':None, 'user_pwv':None, 't_ground':None, 't_sky':None, 'tau0':None, 'seed':None, 'leakage':None, 'graphics':None, 'verbose':None, 'overwrite':None, }

	def result(self, key=None):
		''' why is this here? '''
		return None
	
	def __call__(self,
			project = "sim",
			skymodel = "30dor.fits",
			inbright = "0.06mJy/pixel",
			indirection = "J2000 10h00m00 -40d00m00",
			incell = "0.15arcsec",
			incenter = "230GHz",
			inwidth = "2GHz",
			complist = "",
			compwidth = "8GHz",
			setpointings = True,
			ptgfile = "$project.ptg.txt",
			integration = "600s",
			direction = "",
			mapsize = ['', ''],
			maptype = "ALMA",
			pointingspacing = "",
			caldirection = "",
			calflux = "1Jy",
			obsmode = "int",
			refdate = "2014/05/21",
			hourangle = "transit",
			totaltime = "7200s",
			antennalist = "alma_cycle1_1.cfg",
			sdantlist = "aca.tp.cfg",
			sdant = 0,
			outframe = "LSRK",
			thermalnoise = "",
			user_pwv = 0.5,
			t_ground = 270.0,
			t_sky = 260.0,
			tau0 = 0.1,
			seed = 11111,
			leakage = 0.0,
			graphics = "both",
			verbose = False,
			overwrite = True ):
	
		result = simobserve(project, skymodel, inbright, indirection, incell, incenter, inwidth, complist, compwidth, setpointings, ptgfile, integration, direction, mapsize, maptype, pointingspacing, caldirection, calflux, obsmode, refdate, hourangle, totaltime, antennalist, sdantlist, sdant, outframe, thermalnoise, user_pwv, t_ground, t_sky, tau0, seed, leakage, graphics, verbose, overwrite)

		return result

