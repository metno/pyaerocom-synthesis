#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 13:53:02 2018

@author: jonasg
"""

import os

MODEL_DIR = '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III-CTRL2018/'

def all_model_ids():
    models = []
    all_files = os.listdir(MODEL_DIR)
    
    for item in all_files:
        if os.path.isdir(MODEL_DIR + item):
            models.append(item)
    return models
            
if __name__ == '__main__':
    files = os.listdir(MODEL_DIR)
    
    for f in files:
        if os.path.isdir(MODEL_DIR + f):
            print(f)

