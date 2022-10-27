app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                meta_tags = [{'name' : 'viewport',
                              'content' : 'width=dice_width, initial-scale=1.0'}])


app.layout = dbc.Container([
    html.P(' '),
    html.Div(id = 'first-line-separator'),   
    html.Div([
            html.H2('ACIDENTES RODOVIÁRIOS', className = 'text-general'),
            html.H5('2008 à 2021',  className = 'text-general')
            ], className = 'div-config'),
                    
    html.Div([
        html.P('Quantidade de acidentes rodoviários e vítimas registradas no período de 2008 à 2021 e disponibilizados pela Polícia Federal do Brasil',
              id = 'dashboard-sub-title'),
        ],
   ), 
    html.Div(id = 'second-line-separator', style = {'border' : '2px #343a40 solid',
                                                   'margin-bottom' : '10px'}),
    
    #filter section
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H3('Ano da Ocorrência', className = 'text-filter'),
                dcc.RangeSlider(
                                min=2008,
    max=2021,
    step=1,
    marks = {str(i) : i for i in df['year'].unique()},
   value=[i for i in sorted(df['year'].unique())],
                 
                              id='selected_year_slider',
                               className = 'year-slider')],
                width = {'size' : 6}),
            
            dbc.Col([
                html.H3('UF da Ocorrência', className = 'text-filter'),
                dcc.Dropdown(id='dropdown-uf',
                            multi = False,
                             options = [{'label' : x, 'value' : x} for x in sorted(df['uf'].unique())],
                             className = 'dropdown-states')],
            width = {'size' : 2}, className = 'cols-filters'),
            
            dbc.Col([
                html.H3('Vítimas', className = 'text-filter'),
                dcc.RadioItems(id='vitimas-selected',
                             options = [{'label' : 'total', 'value': 'total'},
                                     {'label' : 'ilesos', 'value' : 'ilesos'},
                                     {'label' : 'feridos', 'value' : 'feridos'},
                                     {'label' : 'mortos', 'value' : 'mortos'},
                                    ], value = 'total', className = 'vitimas-col', inputStyle={"margin-right": "20px"})
            ], width = {'size' : 4}, className = 'vitimas-selected')
        ])
    ], className = 'div-config'),
    
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='lineplot', figure = {},
                        )
            ])
        ])
    ])
      
])


@app.callback(
    Output('lineplot', 'figure'),
    [Input('selected_year_slider', 'value'),
    Input('dropdown-uf', 'value'),
    Input('vitimas-selected', 'value')])
def update_line_plot(selected_year_slider, uf_selected, vitimas):
    aux = df[(df['year'].isin(selected_year_slider)) & (df['uf'].isin([uf_selected]))]
    aux = aux.groupby('year', as_index = False)[vitimas].sum()
    
    fig = px.line(aux, x = 'year', y = vitimas, height = 300, text = vitimas)
    fig.update_layout({
        'plot_bgcolor' : '#2f3031',
         'paper_bgcolor': '#2f3031'},
    margin = dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(type='category',
                    showgrid = False,
                     showline= True,
                     title_text = 'Year',
                     color='#c8c9ca',
                     title_font = {'size' : 10},
                    tickfont=dict(color='#c8c9ca',
                                 size = 8))
    
    fig.update_yaxes(showgrid = False,
                     showticklabels = True,
                     title = None,
                     showline= True,
                     title_text = 'Quantidade',
                     color='#c8c9ca',
                     title_font = {'size' : 10},
                    tickfont=dict(color='#c8c9ca',
                                 size = 8))
    
    fig.update_traces(line_color = '#c8c9ca',
                      line_width=1.5,
                     textfont_size=6.5,
                     textposition='top center',
                    textfont_color = 'grey')

    return fig



if __name__ == '__main__':
    app.run_server()