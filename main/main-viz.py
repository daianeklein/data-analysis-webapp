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
import visualization
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
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ], className='drag-and-drop-text'),
        multiple=True),

    html.Div(id='output-div'),
    html.Div(id='output-datatable')

], width = {'size' : 5}, id='first-box-drag-and-drop'),


])
])
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        html.H5(filename),
        html.Button(id='submit-button', children = 'Create Graph'),

        dash_table.DataTable(
            data = df.to_dict('records'),
            columns = [{'name': i, 'id': i} for i in df.columns],
            page_size = 10,

                style_data={
            'color' : 'grey',
            'backgroundColor' : 'transparent',
            'textAlign': 'center'
            },

            virtualization=True,
            fixed_rows={'headers': True},
            style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
            style_table={'height': 400}
        ),
        dcc.Store(id='stored-data', data = df.to_dict('records'))
    ])


@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              State('stored-data','data'))
            #   State('xaxis-data','value'),
            #   State('yaxis-data', 'value'))
def make_graphs(n, data):
    if n is None:
        return dash.no_update
    else:
        plot_final_visualization()
        


if __name__ == '__main__':
    app.run_server(debug=True)