#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for intercomparison of optical properties between models and 
"""
from warnings import filterwarnings
from helpers.model_list import get_model_ids #list of model IDs
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
TS_TYPES_ANA_OBS_GRIDDED = ['monthly', 'yearly']
TS_TYPES_ANA_OBS_UNGRIDDED = ['daily', 'monthly', 'yearly']

# Leave read ts_type of obsdata flexible, that is, if the analysis ts_type
# is e.g., monthly and the read ts_type for model is e.g., daily, then the
# observation data ts_type can be anything that is in higher resolution or 
# equal resolution monthly. If False, it is required to be the same ts_type
# as the model read ts_type (i.e. daily in this example)
TS_TYPE_OBS_FLEX = True

from pyaerocom.analysis import AnalysisSetup as STP

# specify here information about the observation networks and variables (and 
# sample frequencies). The script below iterates over all analysis setup 
# instances created here (they are dictionaries !), respecively for each 
# time interval specified above
ANALYSIS_SETUP = [
        # EBAS multicolumn
        STP(obs_id='EBASMC', 
            vars_to_analyse=['ec550aer'], # model domain
            alt_vars={'ec550aer': 'scatc550aer'}, #observation
            ts_types_ana=TS_TYPES_ANA_OBS_UNGRIDDED,
            vert_scheme='surface'),
        
            # Aeronet Sun v3, level 2
        STP(obs_id='AeronetSunV3Lev2.daily',
            vars_to_analyse=['ang4487aer', 'od550aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_UNGRIDDED),
        
        # Aeronet SDA v3, level 2
        STP(obs_id='AeronetSDAV3Lev2.daily',
            vars_to_analyse=['od550lt1aer', 'od550gt1aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_UNGRIDDED),
        
        # Aeronet INV v3, level2
        STP(obs_id='AeronetInvV3Lev2.daily',
            vars_to_analyse=['abs550aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_UNGRIDDED),
        # Caliop v3
        STP(obs_id='CALIOP3',
            vars_to_analyse=['od550aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_GRIDDED),
            
        # MISR v3.1
        STP(obs_id='MISR_V31',
            vars_to_analyse=['od550aer', 'ang4487aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_GRIDDED),
        
        # AATSR v4.3
        STP(obs_id='AATSR_SU_v4.3',
            vars_to_analyse= ['abs550aer', 'ang4487aer', 'od550aer', 
                              'od550dust', 'od550gt1aer', 'od550lt1aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_GRIDDED),
        
        # MODIS 6 aqua
        STP(obs_id='MODIS6.aqua',
            vars_to_analyse= ['od550aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_GRIDDED),
            
        # MODIS 6 terra
        STP(obs_id='MODIS6.terra',
            vars_to_analyse= ['od550aer'],
            ts_types_ana=TS_TYPES_ANA_OBS_GRIDDED)
            ]        
  
# Time intervals to be analysed: (start, stop) -> for single years use year 
# number at start and None at stop)
TIME_IVALS = [(2008, None),
              (2010, None)]

# Regional filter for analysis
FILTER_NAME = 'WORLD-noMOUNTAINS'
          
if __name__ == '__main__':
    from time import time

    filterwarnings('ignore')
    t0 = time()
    
    models = get_model_ids()
    
    num = len(ANALYSIS_SETUP)
    for i, stp in enumerate(ANALYSIS_SETUP):
        if i==1 and ONLY_FIRST:
            print(stp)
            break
        for (START, STOP) in TIME_IVALS:
            
            stp.update(start=START,
                       stop=STOP,
                       filter_name=FILTER_NAME,
                       RAISE_EXCEPTIONS=RAISE_EXCEPTIONS,
                       TS_TYPE_OBS_FLEX=TS_TYPE_OBS_FLEX,
                       REANALYSE_EXISTING=REANALYSE_EXISTING)
            
            
            ana = pya.analysis.Analyser(stp)
        
            if RUN_ANALYSIS:
                pya.print_log.info('At: {}, start time = {} ({} of {})'
                                   .format(stp.obs_id, stp.start, i, num))
                ana.run(models)
            
       
                            
    dt = (time()-t0)/60
    print('Analysis finished. Total time: {} min'.format(dt))
