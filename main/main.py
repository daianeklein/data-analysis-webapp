import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from numpy import mean

import classes as cl
import utilities as u
import visualization


if __name__ == '__main__':    
    df = cl.DataFiles()
    delivered = df.create_dataframes('Delivered')
    failed = df.create_dataframes('Failed')
    
    visualization.plot_final_visualization(failed,delivered)
    