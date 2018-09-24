#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper methods used in notebooks
"""
def _dataframe_highlight_4d_no_altitude_dim(x, bg_color='#ffcccc'):
    #copy df to new - original data are not changed
    df = x.copy()
    #set by condition
    m1 = df['Dim'] == 4
    m2 = 'altitude' not in df['Dim names']
    mask = m1 * m2
    df.loc[mask, :] = 'background-color: {}'.format(bg_color)
    df.loc[~mask,:] = 'background-color: ""'
    return df   