#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 07:52:38 2018

@author: jonasg
"""

import pyaerocom as pya

MODEL_ID = 'SPRINTARS-T213_AP3-CTRL2016-PD' #large file

MODEL_ID = 'CAM5.3-Oslo_AP3-CTRL2016-PD' #file that can be handled

OBS_ID = 'EBASMC'

#OBS_ID = 'MODIS6.aqua'

VERT_SCHEME = 'surface'

ALT_VARS = {'ec550aer': 'scatc550aer'}


if __name__ == '__main__':
    
    stp = pya.analysis.AnalysisSetup(model_id=MODEL_ID,
                                     obs_id=OBS_ID,
                                     vars_to_analyse='ec550aer',
                                     start=2010,
                                     stop=None,
                                     vert_scheme=VERT_SCHEME,
                                     alt_vars=ALT_VARS,
                                     RAISE_EXCEPTIONS=True,
                                     REANALYSE_EXISTING=True)


    ana = pya.analysis.Analyser(stp)
    
    print(ana)
    
    ana.run()