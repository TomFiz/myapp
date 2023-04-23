#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bokeh
from math import pi


def get_res(s,year,taux,seuil):
    if s == "Scrutin majoritaire" : 
        scrutin = "propdep"
        taux = 0
        seuil = 0
    elif s == "Scrutin proportionnel départemental" : scrutin = "propdep"
    elif s == "Scrutin proportionnel national" : scrutin = "propnatio"
    else : scrutin = "propregio"
    return pd.read_excel("C:/Users/TomFi/Desktop/Cours/PSC/Affichage_res/"+scrutin+"/"+ scrutin+"_"+str(year)+".xlsx",sheet_name = scrutin+"_"+str(year)+"_"+str(seuil)+ "_"+str(taux))



from os.path import dirname, join
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure,show
from bokeh.transform import cumsum


# Create Input controls
year_elections = [1958,1962,1967,1968,1973,1978,1981,1988,1993,1997,2002,2007,2012,2017,2022]
year_slider = Slider(title="Année", value=2022, start=1958, end=2022, step=1)
taux_slider = Slider(title="Taux de proportionnelle", start=0, end=100, value=0, step=5)
seuil_slider = Slider(title="Seuil de proportionnelle", start=0, end=20, value=0, step=1)
scrutin_select = Select(title="Mode de scrutin", value="All",
               options=["Scrutin majoritaire","Scrutin proportionnel départemental","Scrutin proportionnel régional","Scrutin proportionnel national"])

desc = Div(text="""Visualisation interactive des résultats des élections législatives françaises selon le mode de scrutin""",width=1300, height=50)
data = get_res("Scrutin majoritaire",2022,0,0)
data = data[data['Sièges']>0]
data['angle'] = data['Sièges']/data['Sièges'].sum() * pi
data = data.rename({"Sièges" : "sieges"}, axis = "columns")
source = ColumnDataSource(dict(data))
TOOLTIPS = [("Nuance","@Nuance"),("Nombre de sièges","@sieges")]
p = figure(height=1000, width = 1000, title="Répartition des sièges à l'Assemblée Nationale", toolbar_location=None,
           tools="hover", tooltips=TOOLTIPS, x_range=(-1.2, 1.2), y_range=(0.8,2.2))
p.annular_wedge(x=0, y=1, outer_radius=1,inner_radius = 0.35,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        fill_color="Couleur", line_color="black", legend_field='Nuance', source=source)
p.legend.title = "Nuances"
p.legend.title_text_font_size = '20pt'
p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None



def update(attr,old,new):
    annee = year_slider.value
    taux = taux_slider.value
    seuil = seuil_slider.value
    scrutin = scrutin_select.value
    while annee not in year_elections :
        annee += -1
    df = get_res(scrutin,annee,taux,seuil)
    df = df[df['Sièges']>0]
    df = df[df['Sièges']>0]
    df['angle'] = df['Sièges']/df['Sièges'].sum() * pi
    df = df.rename({"Sièges" : "sieges"}, axis = "columns")
    source.data = df


controls = [scrutin_select,year_slider,taux_slider,seuil_slider]
for control in controls:
    control.on_change('value', update)

inputs = column(*controls, width=300, height=700)

layout = column(desc, row(inputs, p),height = 750, width = 1400, sizing_mode = 'stretch_width')

curdoc().add_root(layout)
curdoc().title = "Résultats des élections legislatives"

