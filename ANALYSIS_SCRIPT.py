#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for intercomparison of optical properties between models and 
"""

from helpers.model_list import get_model_ids
import pyaerocom as pya

# alternative ts_types in case one of the provided in setup is not in dataset
TS_TYPE_READ_ALT = {'daily'      :   ['hourly', '3hourly'],
                    'monthly'    :   ['daily', 'hourly', '3hourly']}            
# Todo: put this into class
TS_TYPE_SETUP = dict(monthly=['monthly', 'yearly'],
                     daily = ['monthly', 'yearly'],
                     read_alt=TS_TYPE_READ_ALT)

# Years to be analysed
YEARS = sorted([2008, 2010])

OBS_INFO = {'AeronetSunV3Lev2.daily' :  ['od550aer', 'ang4487aer'],
            'AeronetSDAV3Lev2.daily' :  ['od550lt1aer', 
                                         'od550gt1aer'],
            pya.const.AERONET_INV_V3L2_DAILY_NAME : ['abs550aer'],
            'MODIS6.terra'          :   ['od550aer'],
            'MODIS6.aqua'           :   ['od550aer']}

# =============================================================================
# OBS_INFO = {'EBASMC'    :   ['absc550aer', 
#                              'scatc550aer']}
# =============================================================================

OBS_IDS = list(OBS_INFO.keys())

FILTER = 'WORLD-noMOUNTAINS'

### output directories
OUT_BASE = './output/'       
             
if __name__ == '__main__':
    from time import time
    
    t0 = time()
    REANALYSE_EXISTING = False
    RUN_ANALYSIS = True
    ONLY_FIRST = False
    RAISE_EXCEPTIONS = False
    
    models = get_model_ids()
    
    if ONLY_FIRST:
        OBS_IDS = [OBS_IDS[0]]
    
    for OBS_ID in OBS_IDS:  
        VARS = OBS_INFO[OBS_ID]
        stp = pya.analysis.Analyser(vars_to_analyse=VARS, 
                                    obs_id=OBS_ID, 
                                    years=YEARS,
                                    filter_name=FILTER, 
                                    ts_type_setup=TS_TYPE_SETUP,
                                    out_basedir=OUT_BASE,
                                    REANALYSE_EXISTING=REANALYSE_EXISTING,
                                    ONLY_FIRST=ONLY_FIRST,
                                    RAISE_EXCEPTIONS=RAISE_EXCEPTIONS)
        
        if RUN_ANALYSIS:
            stp.run(models)
                        
    dt = (time()-t0)/60
    print('Analysis finished. Total time: {} min'.format(dt))
