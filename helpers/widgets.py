#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 08:19:06 2018

@author: jonasg
"""
import pyaerocom as pya
import ipywidgets as ipw
from collections import OrderedDict as od
from ipywidgets.widgets.interaction import show_inline_matplotlib_plots
import os

class PlotScatter(object):
    def __init__(self, file_list, figsize=None):
        
        if figsize is None:
            figsize = (12, 6)
        self.figsize = figsize
        
        
        self.files = od()
        for fp in file_list:
            self.files[os.path.basename(fp)] = fp
        
        self._f = list(self.files.keys())
        self.dropdown_left = ipw.Dropdown(options=self._f,
                                          value=self._f[0])
        
        self.dropdown_right = ipw.Dropdown(options=self._f,
                                           value=self._f[0])
        
        self.dropdown_left.observe(self.on_change_left)
        self.dropdown_right.observe(self.on_change_right)
        
        self.data = pya.CollocatedData()
        
        self.output_left = ipw.Output()
        self.output_right = ipw.Output()
        
        layout_left = ipw.VBox([self.dropdown_left, 
                                self.output_left])
        
        layout_right = ipw.VBox([self.dropdown_right, 
                                 self.output_right])
    
        self.layout = ipw.HBox([layout_left, layout_right])
        
        self.plot_scatter_left(file_list[0])
        self.plot_scatter_right(file_list[1])
        
    def plot_scatter_left(self, filepath):
        self.output_left.clear_output()
        with self.output_left:
            self.data.read_netcdf(filepath).plot_scatter(figsize=self.figsize)
            show_inline_matplotlib_plots()
    
    def plot_scatter_right(self, filepath):
        self.output_right.clear_output()
        with self.output_right:
            self.data.read_netcdf(filepath).plot_scatter(figsize=self.figsize)
            show_inline_matplotlib_plots()        
            
    def on_change_left(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            
            f = str(self.dropdown_left.value)
            #time.sleep(1) 
            self.plot_scatter_left(self.files[f])
            
    def on_change_right(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            
            f = str(self.dropdown_right.value)
            #time.sleep(1) 
            self.plot_scatter_right(self.files[f])
            
    def __call__(self):
        return self.layout
        
        
