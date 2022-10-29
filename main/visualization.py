import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import classes as cl
import utilities as u
from numpy import mean   
   
def plot_final_visualization(dataframe1, dataframe2):
    '''
    This function creates the final visualization of the project. 
    '''
#   visualization
    u.create_jitter_chart(dataframe1, 'pricepoint_sum', 'total_score')
    m1 = dataframe1['total_score'].mean()
    m2 = dataframe2['total_score'].mean()

    fig3 = plt.figure(constrained_layout=True);
    fig3 = plt.figure(figsize=(15,10));

    gs = fig3.add_gridspec(2, 3) ## number of charts
    fig3.add_subplot(gs[1, :]) ##chart 1

    #Histplot - delivered and failed comparison
    ax1 = sns.histplot(data = dataframe1['total_score'], color = 'teal', label = 'failed')
    med1 = plt.vlines(x=m1, linewidth=2, color='#d62728', ymin=0, ymax=1200, linestyle='--', 
                     label = 'Median Failed') # median line 

    ax = sns.histplot(data = dataframe2['total_score'], color = 'midnightblue', label = 'delivered')
    med2 = plt.vlines(x=m2, linewidth=2, color='orange', ymin=0, ymax=1200, linestyle='--', 
                     label = 'Median Delivered') #median line

    u.set_chart_config('Total Score: Delivered x Failed', 'Total Score', ' ')
    plt.xticks(color = 'grey', fontsize = 8);
    plt.yticks(color = 'grey', fontsize = 8);
    plt.legend();

    # scatterplot - clusters
    fig3.add_subplot(gs[0, :-1])
    ax1 = sns.scatterplot(data = dataframe1, x='pricepoint_sum_jitter', y = 'total_score_jitter', hue = 'cluster',
                    palette = {0 : 'midnightblue', 1 : 'mediumseagreen', 2 : 'darkturquoise'})
    u.set_chart_config('Cluster visualization - Failed Attempts', '', '')
    plt.xticks(color = 'white');
    plt.yticks(color = 'white');


    #barplot - groups created by K-means
    fig3.add_subplot(gs[0, 2])
    order = dataframe1.groupby('cluster')['total_score'].mean().sort_values(ascending = False).index
    ax3 = sns.barplot(data = dataframe1, x = 'cluster', y = 'total_score',  estimator=mean,  order = order,
                    palette = {0 : 'midnightblue', 1 : 'mediumseagreen', 2 : 'darkturquoise'}, ci= False)

    u.set_chart_config('Mean of Total Score by Cluster\nFailed Attempts', 'Cluster', '')
    
    plt.savefig('data-analysis-cluster.png')

     # Make the PNG
    # canvas = FigureCanvasAgg(fig)
    # # The size * the dpi gives the final image size
    # #   a4"x4" image * 80 dpi ==> 320x320 pixel image
    # fig_path = f"rand-poiss-hist_{time_ns()}.png"
    # canvas.print_figure(fig_path, dpi=150, bbox_inches="tight")
    # return fig_path

    #plt.show();
