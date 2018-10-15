"""Plotting methods"""

def change_fontsize_colorbar(ax, fontsize=16):
    axes=ax.figure.axes[-1]
    yticks = axes.get_yticklabels()
    axes.set_yticklabels(yticks, fontsize=fontsize)
    lbl = axes.get_ylabel()
    axes.set_ylabel(lbl, fontsize=fontsize)
    return ax

def update_labels(ax, PLOT_XLABELS, PLOT_YLABELS, fontsize=16, xrotation=45, yrotation=45):
    xlbls = ax.get_xticklabels() #get the default x-labels
    xlbls_new = []
    for lbl in xlbls: #iterate over all xlabels
        lbl = lbl.get_text() 
        if lbl in PLOT_XLABELS: #replace, if defined above
            xlbls_new.append(PLOT_XLABELS[lbl]) 
        else: # use original label and print warning
            print('Label {} not defined above, check PLOT_XLABELS'.format(lbl))
            xlbls_new.append(lbl)
    ylbls = ax.get_yticklabels() #get the default x-labels
    ylbls_new = []
    for lbl in ylbls: #iterate over all xlabels
        lbl = lbl.get_text() 
        if lbl in PLOT_YLABELS: #replace, if defined above
            ylbls_new.append(PLOT_YLABELS[lbl]) 
        else: # use original label and print warning
            print('Label {} not defined above, check PLOT_XLABELS'.format(lbl))
            ylbls_new.append(lbl)
    
    ax.set_xticklabels(xlbls_new, rotation=xrotation, fontsize=fontsize, ha='right')       
    ax.set_yticklabels(ylbls_new, rotation=yrotation, fontsize=fontsize, va='top')  
    return ax


