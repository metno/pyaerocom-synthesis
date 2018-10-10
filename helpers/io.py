#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input / output methods for colocated data
"""
import os
import pyaerocom as pya
import ipywidgets as ipw
import pandas as pd
from IPython.display import display, Math

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
        self.var_obs_combinations = []
        
        self._meta_info = []
        self._stats_computed = False
        
        self.stats_table = None
        self.files = []
        
        if init:
            self.search_all_files()
            self.read_meta_from_files()
    
    @property
    def number_of_files(self):
        return len(self.files)
    
    def model_dir(self, model_id):
        return os.path.join(self.base_dir, model_id)
    
    def model_files(self, model_id):
        mdir = self.model_dir(model_id)
        return [os.path.join(mdir, f) for f in os.listdir(mdir) if f.endswith('COLL.nc')]
    
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
        moc = []
        for file in self.files:
            info = data.get_meta_from_filename(file)
            info['model_id'] = info['data_source'][1]
            info['obs_id'] = info['data_source'][0]
            info['year'] = info['start'].year
            info['file'] = file
            mo = [info['var_name'], info['obs_id']]
            found = False
            for _mo in moc:
                if _mo == mo:
                    found = True
                    break
            if not found:
                moc.append(mo)
            
            results.append(info)
            if f is not None:
                f.value += 1
        self._meta_info = results
        self.var_obs_combinations = moc
    
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
            
    def find_meta_unique(self, ts_type_src, flex_search=True):
        ovmy_found = {}
        for meta in self._meta_info:
            for moc in self.var_obs_combinations:
                #candidate
                if [meta['var_name'], meta['obs_id']] == moc:
                    ovmy = '_'.join(moc + [meta['model_id'], str(meta['year'])])
                    
                    # exact match
                    if meta['ts_type_src'] == ts_type_src:
                        ovmy_found[ovmy] = meta
                    # take first match
                    elif flex_search:
                        add_ovmy = True
                        for _ovmy in ovmy_found.keys():
                            if _ovmy == ovmy:
                                add_ovmy=False
                                break

                        if add_ovmy:
                            ovmy_found[ovmy] = meta
        return ovmy_found
                        
    def compute_statistics_table_unique(self, ts_type_src, flex_search=True):
        
        ovm = self.find_meta_unique(ts_type_src, flex_search)
        
        return self.compute_statistics_table(ovm.values()) 
        
    def compute_statistics_table(self, meta_info=None):
        
        if meta_info is None:
            if not len(self._meta_info) == self.number_of_files:
                self.read_meta_from_files()
            meta_info = self._meta_info
            
        header = ['model_id', 'year', 'var_name', 'obs_id', 'ts_type', 
                  'ts_type_src', 'nmb', 'rms', 'R', 'fge']
        data = []
        f = ProgressBarLabelled(len(meta_info), 'Computing statistics table b({} '
                                'files)'.format(len(meta_info)))
        d = pya.ColocatedData()
        for info in meta_info:
            if not 'nmb' in info:
                dat = d.read_netcdf(info['file'])
                info.update(dat.calc_statistics())
                
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
            if f is not None:
                f.value += 1
        df = pd.DataFrame(data, columns=header)
        df.set_index(['model_id', 'year', 'var_name', 'obs_id'], 
                     inplace=True)
        df.sort_index(inplace=True)
        self.stats_table = df
        return df
    
    

    def read_statistics_table_csv(self, file_path):
        self.stats_table = pd.DataFrame().from_csv(file_path, 
                                                   index_col=['model_id',
                                                              'year',
                                                              'var_name',
                                                              'obs_id'], 
                                                   parse_dates=False)
        return self.stats_table
    
    def read(self, filename):
        return pya.ColocatedData(filename)
    
def plot_heatmap(table, colname, ts_type='monthly',
                 cols=['model_id', 'year'], rows=['var_name', 'obs_id'], 
                 output_dir=None, savefig=True,
                 **kwargs):
    subset=table[table['ts_type'] == ts_type]
    try:
        subset = [colname].unstack(cols)
    except:
        subset = pd.pivot_table(subset, values=colname,
                                      columns=cols, index=rows)
    ax = pya.plot.heatmaps.df_to_heatmap(subset,**kwargs)
    ax.set_title('{} ({})'.format(colname, ts_type))
    if savefig and output_dir and os.path.exists(output_dir):
        ax.figure.tight_layout()
        ax.figure.savefig(output_dir + 'heatmap_{}_{}.png'.format(colname,
                                                                  ts_type))
    return ax
    
    
    
        
if __name__ == '__main__':
    '/lustre/storeA/project/aerocom/aerocom2/pyaerocom_out/colocated_data/GEOS5-freegcm_CTRL2016-PD'
    basedir = pya.const.OUTPUTDIR + 'colocated_data'
    reader = ReadColocatedData(basedir)
    
    m = reader.find_meta_unique(ts_type_src='monthly')
    y = reader.find_meta_unique(ts_type_src='yearly')
    d = reader.find_meta_unique(ts_type_src='daily')
    #tab = reader.compute_statistics_table_unique('monthly')


    
    
    
        
    
    
