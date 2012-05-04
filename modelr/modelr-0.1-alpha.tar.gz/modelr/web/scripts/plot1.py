#!/usr/bin/env python
'''
Created on Apr 30, 2012

@author: sean
'''

import matplotlib.mlab as mlab
import matplotlib
from matplotlib.pyplot import figure, show
import numpy as np
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
import tempfile
from os import unlink
from modelr.urlargparse import URLArgumentParser

short_description = 'This is cool'

def create_parser():
    parser = URLArgumentParser('This is the default script')
    parser.add_argument('sinval', required=True, type=float, help='The number of ossilations')
    parser.add_argument('stretch', default=4, type=float, help='The number of ossilations of y2')
    return parser

def run_script(args):
     
    matplotlib.interactive(False)
    
    x = np.arange(0.0, 2, 0.01)
    y1 = np.sin(args.sinval * np.pi * x)
    y2 = 1.2 * np.sin(args.stretch * np.pi * x)
    
    fig = figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312, sharex=ax1)
    ax3 = fig.add_subplot(313, sharex=ax1)
    
    ax1.fill_between(x, 0, y1)
    ax1.set_ylabel('between y1 and 0')
    
    ax2.fill_between(x, y1, 1)
    ax2.set_ylabel('between y1 and 1')
    
    ax3.fill_between(x, y1, y2)
    ax3.set_ylabel('between y1 and y2')
    ax3.set_xlabel('x')
    
#    # now fill between y1 and y2 where a logical condition is met.  Note
#    # this is different than calling
#    #   fill_between(x[where], y1[where],y2[where]
#    # because of edge effects over multiple contiguous regions.
#    fig = figure()
#    ax = fig.add_subplot(211)
#    ax.plot(x, y1, x, y2, color='black')
#    ax.fill_between(x, y1, y2, where=y2>=y1, facecolor='green', interpolate=True)
#    ax.fill_between(x, y1, y2, where=y2<=y1, facecolor='red', interpolate=True)
#    ax.set_title('fill between where')
#    
#    # Test support for masked arrays.
#    y2 = np.ma.masked_greater(y2, 1.0)
#    ax1 = fig.add_subplot(212, sharex=ax)
#    ax1.plot(x, y1, x, y2, color='black')
#    ax1.fill_between(x, y1, y2, where=y2>=y1, facecolor='green', interpolate=True)
#    ax1.fill_between(x, y1, y2, where=y2<=y1, facecolor='red', interpolate=True)
#    ax1.set_title('Now regions with y2>1 are masked')
#    
#    # This example illustrates a problem; because of the data
#    # gridding, there are undesired unfilled triangles at the crossover
#    # points.  A brute-force solution would be to interpolate all
#    # arrays to a very fine grid before plotting.
#    
#    # show how to use transforms to create axes spans where a certain condition is satisfied
#    fig = figure()
#    ax = fig.add_subplot(111)
#    y = np.sin(4*np.pi*x)
#    ax.plot(x, y, color='black')
#    
#    # use the data coordinates for the x-axis and the axes coordinates for the y-axis
#    
#    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
#    theta = 0.9
#    ax.axhline(theta, color='green', lw=2, alpha=0.5)
#    ax.axhline(-theta, color='red', lw=2, alpha=0.5)
#    ax.fill_between(x, 0, 1, where=y>theta, facecolor='green', alpha=0.5, transform=trans)
#    ax.fill_between(x, 0, 1, where=y<-theta, facecolor='red', alpha=0.5, transform=trans)
    
    
#    matplotlib.
    fig_path = tempfile.mktemp('.jpeg')
    plt.savefig(fig_path)
    
    with open(fig_path, 'rb') as fd:
        data = fd.read()
        
    unlink(fig_path)
        
    return data

def main():
    run_script(None)

if __name__ == '__main__':
    main()
