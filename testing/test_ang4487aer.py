#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 07:52:38 2018

@author: jonasg
"""

import pyaerocom as pya

MODEL_ID = 'INCA-BCext_CTRL2016-PD' #large file
OBS_ID = pya.const.AERONET_SUN_V3L2_AOD_DAILY_NAME

if __name__ == '__main__':
    
    stp = pya.analysis.AnalysisSetup(model_id=MODEL_ID,
                                     obs_id=OBS_ID,
                                     vars_to_analyse='ang4487aer',
                                     start=2010,
                                     stop=None,
                                     ts_types_ana='daily',
                                     ts_types_read='3hourly',
                                     RAISE_EXCEPTIONS=True,
                                     REANALYSE_EXISTING=True)


    ana = pya.analysis.Analyser(stp)
    
    print(stp)
    
    ana.run()
    
    