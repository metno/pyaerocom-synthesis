#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings for analysis setup

The information set here
"""
raise NotImplementedError('work in progress...')
#: Base directory for output storage
OUT_BASE = './output/' 

# alternative ts_types in case one of the provided in setup is not in dataset
TS_TYPE_READ_ALT = {'daily'      :   ['hourly', '3hourly'],
                    'monthly'    :   ['daily', 'hourly', '3hourly']}            
# Todo: put this into class
TS_TYPE_SETUP = dict(monthly=['monthly', 'yearly'],
                     daily = ['monthly', 'yearly'],
                     read_alt=TS_TYPE_READ_ALT)

# Years to be analysed
YEARS = sorted([2008, 2010])

#: Insert here the observation networks (keys) and corresponding variables to 
#: be analysed
OBS_INFO = {
     'AeronetSunV3Lev2.daily' :  ['od550aer', 
                                  'ang4487aer'],
     'AeronetSDAV3Lev2.daily' :  ['od550lt1aer', 
                                  'od550gt1aer'],
     'AeronetInvV3Lev2.daily' : ['abs550aer'],
     'MODIS6.terra'          :   ['od550aer'],
     'MODIS6.aqua'           :   ['od550aer']
     }

# =============================================================================
# OBS_INFO = {'EBASMC'    :   ['absc550aer', 
#                              'scatc550aer']}
# =============================================================================

OBS_IDS = list(OBS_INFO.keys())

FILTER = 'WORLD-noMOUNTAINS'

      