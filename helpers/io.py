#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input / output methods for colocated data
"""
import os
import pyaerocom as pya
import ipywidgets as ipw
import pandas as pd
from IPython.display import display

def ProgressBarLabelled(num, label=''):
    try:
        f = ipw.IntProgress(0, max=num)
        l = ipw.Label(label)
        display(ipw.HBox([l, f]))
        return f
    except:
        pass

class ReadColocatedData(object):
    def __init__(self, base_dir=None, init=True):
        if base_dir is None:
            self.search_data_dir()
        if not os.path.exists(base_dir):
            raise IOError('Directory {} does not exist'.format(base_dir))
        self.base_dir = base_dir
        self.model_ids = []
        
        self._meta_info = []
        self._stats_computed = False
        
        self.files = []
        
        if init:
            self.search_all_files()
    
    @property
    def number_of_files(self):
        return len(self.files)
    
    def search_data_dir(self):
        raise NotImplementedError
        
    def search_all_files(self):
        paths = []
        self._meta_info = []    
        self._stats_computed = False
        for model_id in os.listdir(self.base_dir):
            model_dir = os.path.join(self.base_dir, model_id)
            files = os.listdir(model_dir)
            if not model_id in self.model_ids:
                self.model_ids.append(model_id)
            for file in files:
                if file.endswith('COLL.nc'):
                    paths.append(os.path.join(model_dir, file))
        self.files = paths

        return paths
    
    def read_meta_from_files(self):
        results = []
        self._stats_computed = False
        data = pya.ColocatedData()
        f = ProgressBarLabelled(len(self.files), 'Reading meta from {} files'
                                .format(self.number_of_files))
        
        for file in self.files:
            info = data.get_meta_from_filename(file)
            info['model_id'] = info['data_source'][1]
            info['obs_id'] = info['data_source'][0]
            info['year'] = info['start'].year
            
            results.append(info)
            if f is not None:
                f.value += 1
        self._meta_info = results
    
    def compute_statistics(self):
        if not len(self._meta_info) == self.number_of_files:
            self.read_meta_from_files()
        d = pya.ColocatedData()
        f = ProgressBarLabelled(len(self.files), 'Computing statistics ({} '
                                'files)'.format(self.number_of_files))
        for i, file in enumerate(self.files):
            data = d.read_netcdf(file)
            self._meta_info[i].update(data.calc_statistics())
            if f is not None:
                f.value += 1
        self._stats_computed=True
            
    def compute_statistics_table(self):
        if not len(self._meta_info) == self.number_of_files:
            self.read_meta_from_files()
        if not self._stats_computed:
            self.compute_statistics()
        header = ['Model', 'Year', 'Variable', 'Obs', 'Freq', 'FreqSRC',
                  'Bias', 'RMS', 'R', 'FGE']
        data = []
        for info in self._meta_info:
            file_data = [info['model_id'], 
                         info['year'], 
                         info['var_name'], 
                         info['obs_id'],
                         info['ts_type'],
                         info['ts_type_src'],
                         info['nmb'], 
                         info['rms'], 
                         info['R'], 
                         info['fge']]
            
            data.append(file_data)
        df = pd.DataFrame(data, columns=header)
        df.set_index(['Model', 'Year', 'Variable', 'Obs'], inplace=True)
        df.sort_index(inplace=True)
        return df
    
    @staticmethod
    def read_statistics_table_csv(file_path):
        return pd.DataFrame().from_csv(file_path, index_col=['Model',
                                                               'Year',
                                                               'Variable',
                                                               'Obs'], parse_dates=False)
        

from pandas import DataFrame
class MultiModelObsTable(DataFrame):
    def __init__(self, *args, **kwargs):
        super(self, DataFrame).__init__(*args, **kwargs)
    
    def plot_heatmap(self, ts_type):
        raise NotImplementedError
        
if __name__ == '__main__':
    
    basedir = pya.const.OUT_BASEDIR_PPI + 'colocated_data'
    reader = ReadColocatedData(basedir)
    reader.read_meta_from_files()
    reader.compute_statistics()
    
    
        
    
    
