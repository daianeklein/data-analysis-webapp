import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import dash_table
import plotly.express as px

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY],
                meta_tags = [{'name' : 'viewport',
                              'content' : 'width=dice_width, initial-scale=1.0'}])

app.layout = dbc.Container([
        html.P(' '),
        html.Div(id = 'first-line-separator'),
        html.Div([
            html.H2('Customer Analysis and Segmentation', className = 'general-title'),
            html.H5('This is a subtitle - Describe the the aim of the analysis and the dashboard')
            ], className = 'div-header-config'),

        #first drag and drop box
        dbc.Row([
            dbc.Col([
                html.P('Upload the user dataset'),
                dcc.Upload(
                    id = 'uploaded-data-first',
                    children=html.Div([
                        'Drag and Drop your file'
                    ], id = 'drag-and-drop-text'), multiple = False),

                    html.Div(id = 'output-div-first'),
                    html.Div(id = 'output-datatable-first')
            ], width = {'size' : 5}, id='first-box-drag-and-drop'),

            #second drag and drop box
            dbc.Col([            
            html.P('Upload the transaction dataset'),
            dcc.Upload(
                id = 'uploaded-data-second',
                children=html.Div([
                    'Drag and Drop your file'
                    ], id = 'drag-and-drop-text-2nd'), multiple = False),

                    html.Div(id = 'output-div-second'),
                    html.Div(id = 'output-datatable-second'),
                ], width = {'size' : 5}, id = 'second-box-drag-and-drop')
        ]) #closing row 

]) #closing container

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
        html.H5(filename, id = 'file-uploaded-name'),
        html.Button(id="first-submit-button", children="Create Graph"),
        html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
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
@app.callback(Output('output-datatable-first', 'children'),
              Input('uploaded-data-first', 'contents'),
              State('uploaded-data-first', 'filename'),
              State('uploaded-data-first', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(Output('output-div-first', 'children'),
              Input('first-submit-button','n_clicks'),
              State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'))
def make_graphs(n, data, x_data, y_data):
    if n is None:
        return dash.no_update
    else:
        bar_fig = px.bar(data, x=x_data, y=y_data)
        # print(data)
        return dcc.Graph(figure=bar_fig)

if __name__ == '__main__':
    app.run_server(debug=True)

