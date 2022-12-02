# Libraries
import pandas as pd
import dash
from dash import html, dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Data
test_data = pd.DataFrame([[1,2],[3,4]], columns=['Col1', 'Col2'])
saved_test_data = None

# App
app = dash.Dash(__name__)

app.layout = html.Div(children=[dash_table.DataTable(columns = [{"name": i, "id": i} for i in test_data.columns],
                                                     data = test_data.to_dict('records'),
                                                     id = 'test_data_table',
                                                     editable=True,
                                                     ),
                                html.Button('Save data', id='save_test_data', n_clicks=0),
                                dcc.Store(id = 'test_data_store'),
                                dash_table.DataTable(id = 'check_table', data=saved_test_data),
                                ],
                      style={'width': '50%', 'display': 'inline-block', 'padding-left':'25%', 'padding-right':'25%'}
                      )

# Callbacks
@app.callback(Output('test_data_store', 'data'),
              [Input('save_test_data', 'n_clicks'), Input('test_data_table', 'data')])
def save_test_data(n, data):
    if n == 0:
        saved_test_data = None
    else:
        saved_test_data = data
    return saved_test_data

@app.callback(Output('check_table', 'data'),
              Input('test_data_store', 'data'))
def restore_saved_test_data(data):
    return data

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)