import os
from time import time_ns
from turtle import color

import dash
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("agg")

import numpy as np

from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from matplotlib.backends.backend_agg import FigureCanvasAgg
import plotly.graph_objects as go

from matplotlib.figure import Figure
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd

import seaborn as sns
import numpy as np
import utilities as u
##import classes as cl


def plot_final_visualization(data, x_data, y_data):

    fig = make_subplots(rows=1, cols=2)
    px.bar(data, x=x_data, y=y_data)
    # u.create_jitter_chart(data, 'pricepoint_sum', 'total_score')

    #fig.add_trace(go.Scatter(x = x_data, y = y_data), row = 1, col = 2)
    # mode = 'markers', marker_color=data['cluster']), row = 1, col = 2)


    # fig.add_trace(go.Histogram(x=data['total_score']), row = 1, col= 1)
    # fig.add_trace(go.Histogram(x=data['total_score']), row = 1, col = 1)
    # fig.update_layout(title='Test')

    
    # fig.update_coloraxes(showscale=False)

    # #overlay both histograms
    # fig.update_layout(barmode='overlay')
    # fig.update_traces(opacity=0.75)
    return fig
    #fig.show()


#plot_final_visualization(failed)

