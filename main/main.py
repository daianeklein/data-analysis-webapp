import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from numpy import mean

import classes as cl
import utilities as u
#import visualization
import visualization_plotly

if __name__ == '__main__':    
    df = cl.DataFiles()
    delivered = df.create_dataframes('Delivered')
    failed = df.create_dataframes('Failed')
    
    visualization_plotly.plot_final_visualization_plotly(failed,delivered)
    