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
        self.model_ids = {}
        
        self.model_year_combinations = []
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
                self.model_ids[model_id] = model_id.split('_')[0].split('-')[0]
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
        my_all = []
        vo_all = []
        
        for file in self.files:
            info = data.get_meta_from_filename(file)
            info['model_id'] = info['data_source'][1]
            info['obs_id'] = info['data_source'][0]
            info['year'] = info['start'].year
            info['file'] = file
            vo = [info['var_name'], info['obs_id']]
            my = [info['model_id'], info['year']]
            found = False
            for _vo in vo_all:
                if _vo == vo:
                    found = True
                    break
            if not found:
                vo_all.append(vo)
            
            found = False
            for _my in my_all:
                if _my == my:
                    found = True
                    break
            if not found:
                my_all.append(my)
            
            results.append(info)
            if f is not None:
                f.value += 1
        self._meta_info = results
        self.var_obs_combinations = vo_all
        self.model_year_combinations = my_all
    
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
        raise NotImplementedError
        ovm = self.find_meta_unique(ts_type_src, flex_search)
        
        return self.compute_statistics_table(ovm.values()) 
        
    def compute_statistics_table(self, var_obs_combinations=None, 
                                 model_year_combinations=None):
        
        if var_obs_combinations is None:
            var_obs_combinations = self.var_obs_combinations
        
        if model_year_combinations is None:
            model_year_combinations = self.model_year_combinations
            
        meta_info = self._meta_info
        
        header = ['model_id', 'year', 'var_name', 'obs_id', 'ts_type', 
                  'ts_type_src', 'nmb', 'rms', 'R', 'fge']
        data = []
        f = ProgressBarLabelled(len(meta_info), 
                                'Computing statistics table ({} files)'
                                .format(len(meta_info)))
        
        d = pya.ColocatedData()
        for info in meta_info:
            vo_match, my_match = False, False
            for vo in var_obs_combinations:
                if [info['var_name'], info['obs_id']] == vo:
                    vo_match = True
                    break
            for my in model_year_combinations:
                if [info['model_id'], info['year']] == my:
                    my_match = True
                    break
            if vo_match and my_match:
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
                 row_order=None,
                 output_dir=None, savefig=False, savename_add=None,
                 fontsize=None, **kwargs):
    if fontsize:
        from matplotlib import rcParams
        rcParams.update({'font.size': fontsize})
    subset=table[table['ts_type'] == ts_type]
    try:
        subset = subset[colname].unstack(cols)
    except:
        subset = pd.pivot_table(subset, values=colname,
                                      columns=cols, index=rows)
    
    if row_order:
        _new_order = []
        for item in row_order:
            for comb in subset.index:
                if tuple(item) == comb:
                    _new_order.append(tuple(item))
                    
        if len(_new_order) == len(subset.index):
            print('Reordering row indices according to input selection')
            subset = subset.reindex(_new_order)
# =============================================================================
#             subset.set_index(pd.MultiIndex.from_tuples(_new_order,sortorder=False), 
#                             inplace=True)
# =============================================================================
    ax = pya.plot.heatmaps.df_to_heatmap(subset,**kwargs)
    if 'table_name' in kwargs:
        title = kwargs['table_name']
    else:
        title = colname
    ax.set_title('{} ({})'.format(title, ts_type))
    if savefig and output_dir and os.path.exists(output_dir):
        ax.figure.tight_layout()
        if savename_add is not None:
            savename = 'heatmap_{}_{}.png'.format(colname, ts_type)
        else:
            savename = 'heatmap_{}_{}_{}.png'.format(colname, ts_type, savename_add)
        ax.figure.savefig(output_dir + savename)
    return ax
    
    
    
        
if __name__ == '__main__':
    '/lustre/storeA/project/aerocom/aerocom2/pyaerocom_out/colocated_data/GEOS5-freegcm_CTRL2016-PD'
    basedir = pya.const.OUTPUTDIR + 'colocated_data'
    reader = ReadColocatedData(basedir)
    
    reader.compute_statistics_table(var_obs_combinations=[['od550aer', 'MISRV31'],
                                                          ['od550aer', 'MODIS6.terra']],
            model_year_combinations=[['ECHAM6.3-HAM2.3_AP3-CTRL2016-PD', 2010],
                                     ['CNRM-AESM2Nud_AP3-CTRL2016-PD', 2010]])
    
    #m = reader.find_meta_unique(ts_type_src='monthly')
    #y = reader.find_meta_unique(ts_type_src='yearly')
    #d = reader.find_meta_unique(ts_type_src='daily')
    #tab = reader.compute_statistics_table_unique('monthly')


    
    
    
        
    
    
