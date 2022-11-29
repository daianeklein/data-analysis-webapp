import os
from time import time_ns

import dash
import matplotlib
import matplotlib as mpl

matplotlib.use("agg")

import numpy as np

from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Button(
            "Generate plot",
            id="generate-plot",
            style={
                "margin": "10% 40% 10% 40%",
                "width": "20%",
                "fontSize": "1.1rem",
            },
        ),
        dcc.Download(id="download-image"),
    ]
)


def draw_figure():
    fig = Figure()
    ax = fig.add_subplot(111)

    # Random dist plot
    scaled_y = np.random.randint(20, 30)
    random_data = np.random.poisson(scaled_y, 100)
    ax.hist(random_data, bins=12, fc=(0, 0, 0, 0), lw=0.75, ec="b")

    # Axes label properties
    ax.set_title("Figure Title", size=26)
    ax.set_xlabel("X Label", size=14)
    ax.set_ylabel("Y Label", size=14)

    # NOTE:
    # Save figure ~
    # * BUT DO NOT USE PYLAB *
    #   Write figure to output file (png|pdf).

    # Make the PNG
    canvas = FigureCanvasAgg(fig)
    # The size * the dpi gives the final image size
    #   a4"x4" image * 80 dpi ==> 320x320 pixel image
    fig_path = f"rand-poiss-hist_{time_ns()}.png"
    canvas.print_figure(fig_path, dpi=150, bbox_inches="tight")
    return fig_path


@app.callback(
    Output("download-image", "data"),
    Input("generate-plot", "n_clicks"),
    prevent_initial_call=True,
)
def generate_downloadable_figure(n_clicks):
    if n_clicks > 1:
        fig_path = draw_figure()
        return dcc.send_file(fig_path)


if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=True, host="0.0.0.0")
