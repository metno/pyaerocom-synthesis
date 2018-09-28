#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for intercomparison of optical properties between models and 
"""

from helpers.model_list import get_model_ids
import pyaerocom as pya

### TODOs

# 1. include untis and automatic unit conversion (e.g. extinction coeffs
# sometimes in Mm-1 and sometimes in m-1)
# 2. flexible
### Analysis options
# if True, existing output files will be overwritten
REANALYSE_EXISTING = False
# if False, no analysis is performed
RUN_ANALYSIS = True
# if True, only the first model / obsnetwork is analysed
ONLY_FIRST = False
# if True, the analysis will stop whenever an error occurs (else, errors that 
# occurred will be written into the logfiles)
RAISE_EXCEPTIONS = False

### Setup of TS_TYPES for colocation 
# NOTE: THIS WILL CHANGE SOON as this is too complicated and redundant, that is, 
# the analysis should be performed at the highest possible resolution (if not 
# other specified) and then downscaling can be done in post based on colocated
# data files

# keys are model source ts_types (i.e. the original model resolution, values
# are corresponding ts_types used for analysis)
TS_TYPE_SETUP = dict(monthly    =   ['monthly', 'yearly'],
                     daily      =   ['monthly', 'yearly'])

# Setup alternative ts_types in case one of the provided in setup is not in dataset                     
TS_TYPE_READ_ALT = dict(daily   =  ['hourly', '3hourly'],
                        monthly =   ['daily', 'hourly', '3hourly'])

TS_TYPE_SETUP['read_alt'] = TS_TYPE_READ_ALT

# Years to be analysed
YEARS = sorted([2008, 2010])

OBS_INFO = {'EBASMC'    :   ['absc550aer', 
                             'scatc550aer'],
            'AeronetSunV3Lev2.daily' :  ['od550aer', 'ang4487aer'],
            'AeronetSDAV3Lev2.daily' :  ['od550lt1aer', 
                                         'od550gt1aer'],
            pya.const.AERONET_INV_V3L2_DAILY_NAME : ['abs550aer'],
            'MODIS6.terra'          :   ['od550aer'],
            'MODIS6.aqua'           :   ['od550aer']}

# lis
# key -> in Model, value -> in observation
VARS_ALT = {'ec550aer': 'scatc550aer'}
OBS_IDS = list(OBS_INFO.keys())

FILTER = 'WORLD-noMOUNTAINS'

# TODO: needs to be variable / obsnetwork specific
VERT_SCHEME = 'surface'

### output directories
OUT_BASE = './output/'
             
if __name__ == '__main__':
    from time import time
    
    t0 = time()
    
    models = get_model_ids()
    
    if ONLY_FIRST:
        OBS_IDS = [OBS_IDS[0]]
    
    for OBS_ID in OBS_IDS:  
        VARS = OBS_INFO[OBS_ID] + list(VARS_ALT.keys())
        stp = pya.analysis.Analyser(vars_to_analyse=VARS, 
                                    alt_vars=VARS_ALT,
                                    obs_id=OBS_ID, 
                                    years=YEARS,
                                    filter_name=FILTER, 
                                    vert_scheme=VERT_SCHEME,
                                    ts_type_setup=TS_TYPE_SETUP,
                                    out_basedir=OUT_BASE,
                                    REANALYSE_EXISTING=REANALYSE_EXISTING,
                                    ONLY_FIRST=ONLY_FIRST,
                                    RAISE_EXCEPTIONS=RAISE_EXCEPTIONS)
        
        if RUN_ANALYSIS:
            stp.run(models)
                        
    dt = (time()-t0)/60
    print('Analysis finished. Total time: {} min'.format(dt))
