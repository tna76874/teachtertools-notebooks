#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lmh
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from itertools import combinations,chain

class soziogramm(object):
    def __init__(self,**kwargs):
        self.config = {}
        self.config.update(kwargs)
        
        self.names = None
        
        self.G = None
        self.fig = None
        self.cons = None
        self.clique = None

    def read_names(self):
        self.names = pd.read_csv('namen.csv', header=None)
    
    def save(self, format='pdf'):
        self.fig.savefig("soziogramm."+format)
        
    def get_clique(self):
        circles = { k : set(self.G.neighbors(k[0])).intersection(set(self.G.neighbors(k[1]))) for k in combinations(self.G.nodes,2) }
        circles = { tuple(set(list(circles[k[0]]) + list(circles[k[1]]))):tuple(k[0]) for k in combinations(circles.keys(),2) if ((circles[k[0]]==circles[k[1]]) & (len(circles[k[0]])>=2)) }
        circles = list(set([ tuple(set(list(k)+list(v))) for k,v in circles.items()]))
        self.clique = circles
        print("Cliquen:")
        _ = [print(", ".join(list(k))) for k in circles]
        
    def make_soziogramm(self, save=False, format='pdf', directed=False):
        self.read_names()
        
        pairs = list()
        personen = list()
        for i in self.names.index:
            n = [k for k in self.names.loc[i,:].values if pd.notnull(k)]
            personen += n
            pairs += [tuple([k,n[0]]) for k in n[1:]]
        weights = [ tuple(sorted(list(k))) for k in pairs]
        weights = {x:weights.count(x) for x in weights}
        personen = list(set(personen))
        print("In der Klasse sind {:} Personen.".format(len(personen)))

        if directed:
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()
        
        self.G.add_nodes_from(personen)
        edgelist = list()
        edge_color = list()
        edge_style = list()
        for k in pairs:
            edgeweight=weights[tuple(sorted(list(k)))]
            if (edgeweight>=2) & directed:
                edge_color+=['r']
                edge_style+=['-']
                edgelist += [tuple(k)]
                self.G.add_edge(k[0], k[1], weight=edgeweight)
            if (edgeweight>=2) & (not directed):
                edge_color+=['k']
                edge_style+=['-']
                edgelist += [tuple(k)]
                self.G.add_edge(k[0], k[1], weight=edgeweight)
            elif (edgeweight<2) & directed:
                edge_color+=['k']
                edge_style+=[':']
                edgelist += [tuple(k)]
                self.G.add_edge(k[0], k[1], weight=edgeweight)
            
        pos = nx.spring_layout(self.G)

        self.fig, ax = plt.subplots(1,1,figsize=(11.69*2,8.27*2))
        nx.draw_networkx(self.G, pos,
                         with_labels=True,
                         ax=ax,
                         font_color='red',
                         node_size=1000,
                         node_color="white",
                         node_shape="s",
                         alpha=1,
                         width=1,
                         edgelist=edgelist,
                         style=edge_style,
                         edge_color=edge_color,
                        )
        
        
        ax.set_aspect('equal')
        plt.box(False)

        if save: self.save(format=format)

        if directed:
            cons_out = { k:len(self.G.out_edges(k)) for k in personen }
            cons_in = { k:len(self.G.in_edges(k)) for k in personen }
            cons_out = pd.DataFrame({'name':cons_out.keys(), 'in':cons_out.values()})
            cons_in = pd.DataFrame({'name':cons_in.keys(), 'out':cons_in.values()})
            cons = pd.merge(cons_in,cons_out,on='name')
            cons['in-out'] = cons['in']-cons['out']
            self.cons = cons.sort_values(['in-out'],ascending=[False]).reset_index(drop=True)