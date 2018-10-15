#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 07:52:38 2018

@author: jonasg
"""

import pyaerocom as pya
import matplotlib.pyplot as plt
import os
MODEL_ID = 'CAM5.3-Oslo_AP3-CTRL2016-PD'

AERONET_V3 = pya.const.AERONET_SUN_V3L2_AOD_DAILY_NAME
AERONET_V2 = pya.const.AERONET_SUN_V2L2_AOD_DAILY_NAME

OUTDIR = os.path.abspath('./output/')
if __name__ == '__main__':
    plt.close('all')
    
    ### READ OBSDATA
    obs_reader = pya.io.ReadUngridded()
    
    aero2 = obs_reader.read(AERONET_V2, 
                            vars_to_retrieve=['od550aer',
                                              'ang4487aer',
                                              'ang4487aer_calc'])

    aero3 = obs_reader.read(AERONET_V3, 
                            vars_to_retrieve=['od550aer',
                                              'ang4487aer',
                                              'ang4487aer_calc'])

    ### READ MODELDATA
    model_reader = pya.io.ReadGridded(MODEL_ID)
    
    od440aer = model_reader.read_var('od440aer')
    od870aer = model_reader.read_var('od870aer')
    
    od550aer = model_reader.read_var('od550aer')
    
    ang4487aer = model_reader.read_var('ang4487aer')
    
    
    # COLOCATION
    od550aer_col_v2 = pya.colocation.colocate_gridded_ungridded_2D(od550aer,
                                                                   aero2,
                                                                   ts_type='monthly',
                                                                   filter_name='WORLD-noMOUNTAINS')
    
    
    od550aer_col_v2.plot_scatter(savefig=True, 
                                 save_dir=OUTDIR, 
                                 save_name='od550aer_scat_v2.png')
    
    
    
    
    
    coldata_v2 = pya.colocation.colocate_gridded_ungridded_2D(ang4487aer,
                                                              aero2,
                                                              ts_type='monthly',
                                                              filter_name='WORLD-noMOUNTAINS')
    
    
    coldata_v2.plot_scatter(savefig=True, 
                            save_dir=OUTDIR, 
                            save_name='ang4487aer_scat_v2.png')
    
    
    coldata_v2_CALC = pya.colocation.colocate_gridded_ungridded_2D(ang4487aer,
                                                                   aero2,
                                                                   var_ref='ang4487aer_calc',
                                                                   ts_type='monthly',
                                                                   filter_name='WORLD-noMOUNTAINS')
    
    
    coldata_v2_CALC.plot_scatter(savefig=True, 
                                 save_dir=OUTDIR, 
                                 save_name='ang4487aer_calc_scat_v2.png')
    
    
    od550aer_col_v3 = pya.colocation.colocate_gridded_ungridded_2D(od550aer,
                                                                   aero3,
                                                                   ts_type='monthly',
                                                                   filter_name='WORLD-noMOUNTAINS')
    
    
    od550aer_col_v3.plot_scatter(savefig=True, 
                                 save_dir=OUTDIR, 
                                 save_name='od550aer_scat_v3.png')
    
    coldata_v3 = pya.colocation.colocate_gridded_ungridded_2D(ang4487aer,
                                                              aero3,
                                                              ts_type='monthly',
                                                              filter_name='WORLD-noMOUNTAINS')
    
    
    coldata_v3.plot_scatter(savefig=True, 
                            save_dir=OUTDIR, 
                            save_name='ang4487aer_scat_v3.png')
    
    
    coldata_v3_CALC = pya.colocation.colocate_gridded_ungridded_2D(ang4487aer,
                                                                   aero3,
                                                                   var_ref='ang4487aer_calc',
                                                                   ts_type='monthly',
                                                                   filter_name='WORLD-noMOUNTAINS')
    
    
    coldata_v3_CALC.plot_scatter(savefig=True, 
                                 save_dir=OUTDIR, 
                                 save_name='ang4487aer_calc_scat_v3.png')
    
    
    
    