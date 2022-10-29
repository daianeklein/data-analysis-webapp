import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import pandas as pd

import numpy as np
from numpy import mean

import classes as cl
import utilities as u
#import visualization
from visualization_plotly import plot_final_visualization


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY],
                meta_tags = [{'name' : 'viewport',
                              'content' : 'width=dice_width, initial-scale=1.0'}])

app.layout = dbc.Container([ 
        html.Div([
        html.P(' '),
        html.Div(id = 'first-line-separator'),
        html.Div([
        html.H2('Customer Analysis and Segmentation', id = 'general-title'),
        html.H5('This is a subtitle - Describe the the aim of the analysis and the dashboard',
                                                            id = 'dashboard-subtitle')
        ], className = 'div-header-config'),

    dbc.Row([
        dbc.Col([
        dcc.Upload(
        id='upload-data-first',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ], className='drag-and-drop-text'),
        multiple=True),

    html.Div(id='output-div-first'),
    html.Div(id='output-datatable-first')

], width = {'size' : 5}, id='box-drag-and-drop-first'),

])
])
])



if __name__ == '__main__':
    app.run_server(debug=True)