#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 19:37:58 2019

@author: jonasg
"""



import pyaerocom as pya

f = 'US0035R.20100101000000.20190131170718.aerosol_light_scattering_coefficient.pm10.1y.1h.lev2.nas'

data = pya.io.EbasNasaAmesFile(f)
print(data)