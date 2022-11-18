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
import classes as cl
import utilities as u
from numpy import mean   
from time import time_ns

df = cl.DataFiles()
delivered = df.create_dataframes('Delivered')
failed = df.create_dataframes('Failed')

def plot_final_visualization_plotly(dataframe1, dataframe2):

    fig = make_subplots(rows=1, cols=2)
    u.create_jitter_chart(dataframe1, 'pricepoint_sum', 'total_score')

    fig.add_trace(go.Scatter(x = dataframe1['pricepoint_sum_jitter'], y = dataframe1['total_score_jitter'],
    mode = 'markers', marker_color=dataframe1['cluster']), row = 1, col = 2)


    fig.add_trace(go.Histogram(x=dataframe1['total_score']), row = 1, col= 1)
    fig.add_trace(go.Histogram(x=dataframe2['total_score']), row = 1, col = 1)
    fig.update_layout(title='Population')

    
    fig.update_coloraxes(showscale=False)

    #overlay both histograms
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    #return fig
    fig.show()

#plot_final_visualization(failed,delivered)


