# vim:set ff=unix expandtab ts=4 sw=4:
import numpy as np
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# scatter plots
xhist_fs = 16
yhist_fs = 16

#bin plots
def cc(arg,alpha=None):
    if not(alpha):
        alpha=0.9
    return colorConverter.to_rgba(arg, alpha)

content_facecolors=[cc("black",alpha=0.1)]*5
deathrate_facecolors=[cc("red",alpha=0.1)]*5
loss_facecolors=deathrate_facecolors
gain_facecolors=[cc("green",alpha=0.1)]*5

def add_xhist_data_to_scatter(plot_ax, data, label, fontsize, show_grid = True):
    # add top x-axis with histogram data

    # add second x-axis at the top
    ax = plot_ax.twiny()
    ax.set_position(plot_ax.get_position())
    ax.set_xlim(plot_ax.get_xlim())

    # prepare data
    bins = [i for i in range(min(data),max(data)+2,1)]
    hisx = np.histogram(data,bins=bins)

    # set ticks and labels
    x2_ticks = [hisx[1][i] for i in range(len(hisx[0])) if hisx[0][i] != 0]
    x2_ticklabels = [hisx[0][i] for i in range(len(hisx[0])) if hisx[0][i] != 0]
    ax.set_xticks(x2_ticks)
    ax.set_xticklabels(x2_ticklabels, fontsize=fontsize)

    ax.set_xlabel(label, fontsize=fontsize)
    ax.grid(show_grid)

class SinglePlotFigureHandler:
    def __init__(self,figure_filename):
        self.figure_filename=figure_filename

    def __enter__(self):
        self.fig=plt.figure()
        ax=self.fig.add_subplot(1,1,1,projection="3d")
        return(ax)
        
    def __exit__(self,type,value,traceback):    
        self.fig.savefig(self.figure_filename)
        plt.close(self.fig.number)
