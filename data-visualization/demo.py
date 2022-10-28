import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc


import pandas as pd

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
    html.Div(id='output-data-upload'),

], width = {'size' : 5}, id='first-box-drag-and-drop'),

# second drag and drop
        dbc.Col([
        dcc.Upload(
        id='upload-second-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ], className='drag-and-drop-text'),
        multiple=True
    ),
    html.Div(id='second-output-data-upload'),

], width = {'size' : 5}, id='second-box-drag-and-drop')

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
        html.H5(filename, className = 'file-name-uploaded'),

        html.Div([
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],

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

        ], id= 'first-table-output'),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content', className='raw-content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # },className='raw-content')
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

@app.callback(Output('second-output-data-upload', 'children'),
              Input('upload-second-data', 'contents'),
              State('upload-second-data', 'filename'),
              State('upload-second-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)
