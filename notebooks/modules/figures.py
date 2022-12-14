#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lmh
"""
import matplotlib.pyplot as plt
import numpy as np
from sympy.utilities.lambdify import lambdify, implemented_function, lambdastr
import sympy as sp
sf = sp.sympify

class plotfig(object):
    def __init__(self,**kwargs):
        self.fig = None
        self.ax = None
        self.initfig(**kwargs)
        
    def initfig(self,h=1,v=1,size=1.5,sharex=True,sharey=True,wspace = 0.2,hspace = 0.2,figsize=[6,2]):
        self.fig, self.ax = plt.subplots(v,h,sharey=sharey,sharex=sharex,figsize=tuple(np.array(figsize)*size))
        self.fig.subplots_adjust(wspace = wspace,hspace = hspace)
        try: self.ax = list(self.ax.flatten())
        except: self.ax = [self.ax]
        
    def plot(self,x,y,idx=0,ax=None,xl=None,yl=None,title=None,args={}):
        if isinstance(ax,type(None)): ax = self.ax[idx]

        plotstyle = {
                    'color'     : 'black',
                    'marker'    : 'x',
                    'linestyle' : 'None',
#                    'linewidth' : 1,
                    'markersize': 5,
                    'clip_on'   : True,
                    }
        plotstyle.update(args)
        ax.plot(x.m,y.m,**plotstyle)
        if xl != None:
            ax.set_xlabel(u'%s in %s'%(xl,"{:~P}".format(x.u)))
        if yl != None:
            ax.set_ylabel(u'%s in %s'%(yl,"{:~P}".format(y.u)))
        if title!=None:
            ax.set_title(title)
            
    def scheme_scale(self,ax,margin=0.5):
        ax.axis(False)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ax.set_xlim(xmin-margin, xmax+margin)
        ax.set_ylim(ymin-margin, ymax+margin)
        
    def grid(self,grain: list = [1,0.1,1,0.1], idx='all',ax=None,):
        """
        grain: [X-Major, Y-Major, X-Minor, Y-Minor]
        """
        axes = self.get_ax(ax=ax,idx=idx)
        for ax in axes:
            if grain[0]!= None:
                ax.xaxis.set_major_locator(plt.MultipleLocator(grain[0]))
            if grain[2]!= None:
                ax.yaxis.set_major_locator(plt.MultipleLocator(grain[2]))
            if grain[1]!= None:
                ax.xaxis.set_minor_locator(plt.MultipleLocator(grain[1]))
            if grain[3]!= None:
                ax.yaxis.set_minor_locator(plt.MultipleLocator(grain[3]))
            ax.grid(True,which='both')

    def get_ax(self,ax=None,idx='all'):
        if isinstance(idx,str):
            if idx=='all':
                axes = self.ax
                
        if isinstance(ax,type(None)) & isinstance(idx,int):
            axes = [ self.ax[idx] ]  
        
        return axes

    def arrowed_spines(self,ax=None,idx='all',equal=False, delta=0.2):
        axes = self.get_ax(ax=ax,idx=idx)
        for ax in axes: self.arrowed_spines_for_ax(ax,delta=delta)
        
        if equal: _ = [ ax.set_aspect('equal') for ax in axes ]
            
            
    def arrowed_spines_for_ax(self, ax,delta=0.2):
        # https://matplotlib.org/stable/gallery/spines/centered_spines_with_arrows.html
        # Move the left and bottom spines to x = 0 and y = 0, respectively.
        ax.spines[["left", "bottom"]].set_position(("data", 0))
        # Hide the top and right spines.
        ax.spines[["top", "right"]].set_visible(False)

        # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
        # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
        # respectively) and the other one (1) is an axes coordinate (i.e., at the very
        # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
        # actually spills out of the axes.
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        # hide 0 ticks not to overlap with axis
        ax.xaxis.get_major_ticks()[1].label1.set_visible(False)
        ax.yaxis.get_major_ticks()[1].label1.set_visible(False)
        
        # Annotate x and y
        xmin, xmax = ax.get_xlim() 
        ymin, ymax = ax.get_ylim()
        
        ax.annotate('x', xy=(1,0), xytext=(xmax+delta, 0), transform=ax.transAxes, ha='center', va='center')
        ax.annotate('y', xy=(0,1), xytext=(0, ymax+delta), transform=ax.transAxes, ha='center', va='center')

    def save(self,savename: str='plot', **kwargs):
        cvars =         {
                        'bbox_inches'   : 'tight',
                        'pad_inches'    : 0,
                        'dpi'           : 400,
                        'format'      : 'pdf',
                        }
        cvars.update(kwargs)
        
        self.fig.savefig(savename+'.'+cvars['format'], **cvars)