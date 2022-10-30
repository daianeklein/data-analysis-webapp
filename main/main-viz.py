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

#import classes as cl
#import utilities as u
#import visualization
#from visualization_plotly import plot_final_visualization


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
        html.Button(id="submit-button-first", children="Create Graph"),
        html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data-first', data=df.to_dict('records')),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output('output-datatable-first', 'children'),
              Input('upload-data-first', 'contents'),
              State('upload-data-first', 'filename'),
              State('upload-data-first', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(Output('output-div-first', 'children'),
             Input('submit-button-first', 'n_clicks'),
             State('stored-data-first', 'data'))
def test(data):
    bar_fig = px.bar(data, x = data['phone_operator'], y = data['os_version'])
    return dcc.Graph(figure = bar_fig)

if __name__ == '__main__':
    app.run_server(debug=True)