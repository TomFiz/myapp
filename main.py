#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bokeh
from math import pi

#Extract result
def get_res(s,year,taux,seuil):
    if s == "Scrutin majoritaire" : scrutin = "majoritaire"
    elif s == "Scrutin proportionnel départemental" : scrutin = "propdep"
    elif s == "Scrutin proportionnel national" : scrutin = "propnatio"
    else : scrutin = "propregio"
    return pd.read_excel(scrutin+"_"+str(year)+".xlsx",sheet_name = scrutin+"_"+str(year)+"_"+str(seuil)+"_"+str(taux))


from os.path import dirname, join
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure,show
from bokeh.transform import cumsum


# Create Input controls
year_slider = Slider(title="Année", value=2022, start=1958, end=2022, step=1)
taux_slider = Slider(title="Taux de proportionnelle", start=0, end=100, value=0, step=5)
seuil_slider = Slider(title="Seuil de proportionnelle", start=0, end=20, value=0, step=1)
scrutin_select = Select(title="Mode de scrutin", value="All",
               options=["Scrutin majoritaire","Scrutin proportionnel départemental","Scrutin proportionnel national","Scrutin proportionnel régional"])

desc = Div(text="""Visualisation interactive des résultats des élections législatives françaises selon le mode de scrutin""",width=200, height=100)
data = get_res("Scrutin proportionnel regional",2022,0,0)
data = data[data['Sièges']>0]
data['angle'] = data['Sièges']/data['Sièges'].sum() * pi
p = figure(height=800, title="Répartition des sièges à l'Assemblée Nationale", toolbar_location=None,
           tools="hover", tooltips="@Nuance: @Sièges", x_range=(-0.5, 1.0))
p.wedge(x=0, y=1, radius=1,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color="Couleur", legend_field='Nuance', source=data)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None


def update():
    annee = year_slider.value
    taux = taux_slider.value
    seuil = seuil_slider.value
    scrutin = scrutin_select.value
    
    data = get_res(scrutin,annee,taux,seuil)
    data = data[data['Sièges']>0]


controls = [scrutin_select,year_slider,taux_slider,seuil_slider]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320, height=800)

layout = column(desc, row(inputs, p, sizing_mode='scale_height'), sizing_mode="scale_height",height = 800)

update()  # initial load of the data

curdoc().add_root(layout)
curdoc().title = "Résultats des élections legislatives"

