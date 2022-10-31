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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div([
        html.H5('Upload data'),
        html.Button(id = 'submit-button', children = 'Create Chart')
    ]),
    html.Div(id='output-data-upload'),

    html.Div(
        id = 'div-chart'
    )
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
        html.H6(datetime.datetime.fromtimestamp(date)),


        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=10
        ),

        dcc.Store(id='stored-data', data=df.to_dict('records')),
        

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(Output('div-chart', 'children'),
             Input('submit-button', 'n_clicks'),
             State('stored-data', 'data'))

def crate_chart(n, data):
    if n is None:
        return dash.no_update
    else:
        bar_fig = px.bar(data, x='phone_operator', y='os_version')
        return dcc.Graph(figure=bar_fig)




if __name__ == '__main__':
    app.run_server(debug=True)
