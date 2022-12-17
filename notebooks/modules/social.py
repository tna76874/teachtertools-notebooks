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

    def read_names(self):
        self.names = pd.read_csv('namen.csv')

    def make_soziogramm(self, save=True, format='pdf'):
        self.read_names()
        
        pairs = list()
        personen = list()
        for i in self.names.index:
            n = [k for k in self.names.loc[i,:].values if pd.notnull(k)]
            personen += n
            pairs += [tuple(set([n[0],k])) for k in n[1:]]
        pairs = {x:pairs.count(x) for x in pairs}
        personen = list(set(personen))
        print("In der Klasse sind {:} Personen.".format(len(personen)))

        G = nx.Graph()
        G.add_nodes_from(personen)
        for k,v in pairs.items():
            try: G.add_edge(k[0], k[1], weight=v)
            except: pass
        pos = nx.spring_layout(G)

        fig, ax = plt.subplots(1,1,figsize=(11.69,8.27))
        nx.draw_networkx(G, pos, with_labels=True,ax=ax, font_color='red',node_size=100, node_color="white", node_shape="s", alpha=1, linewidths=30)
        ax.set_aspect('equal')
        plt.box(False)
        
        if save: fig.savefig("soziogramm."+format)

        cons = { k:len(G.edges(k)) for k in personen }
        pd.DataFrame({'namen':cons.keys(), 'verbindungen':cons.values()}).sort_values('verbindungen',ascending=False).reset_index(drop=True)