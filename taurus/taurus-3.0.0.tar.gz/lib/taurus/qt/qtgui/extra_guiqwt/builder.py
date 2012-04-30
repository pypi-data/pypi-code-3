#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""Extension of :mod:`guiqwt.builder`"""

__all__=["TaurusPlotItemBuilder", "make"]

__docformat__ = 'restructuredtext'

import guiqwt.builder

from curve import TaurusCurveItem, TaurusTrendItem
from image import TaurusImageItem, TaurusRGBImageItem
from guiqwt.curve import CurveParam
from guiqwt.image import ImageParam
from guiqwt.config import _
from guiqwt.baseplot import BasePlot
import numpy


class TaurusPlotItemBuilder(guiqwt.builder.PlotItemBuilder):
    '''extension of :class:`guiqwt.builder.PlotItemBuilder` to provide tauruscurve and taurusimage items'''
    def __init__(self, *args, **kwargs):
        guiqwt.builder.PlotItemBuilder.__init__(self, *args, **kwargs)
        
    def set_curve_axes(self, *args, **kwargs):
        #ugly hack: I need to redefine this here because it is a private method in PlotItemBuilder
        guiqwt.builder.PlotItemBuilder._PlotItemBuilder__set_curve_axes(self, *args, **kwargs)
        
    def set_image_param(self, *args, **kwargs):
        #ugly hack: I need to redefine this here because it is a private method in PlotItemBuilder
        guiqwt.builder.PlotItemBuilder._PlotItemBuilder__set_image_param(self, *args, **kwargs)
        
    def set_param(self, *args, **kwargs):
        #ugly hack: I need to redefine this here because it is a private method in PlotItemBuilder
        guiqwt.builder.PlotItemBuilder._PlotItemBuilder__set_param(self, *args, **kwargs)
        
    def pcurve(self, x, y, param, xaxis="bottom", yaxis="left"):
        """
        Extension to meth:`guiqwt.builder.PlotItemBuilder.pcurve` to support x
        and y being taurus attribute models instead of arrays, in which case, a
        TaurusCurveItem is returned. This method is called from :meth:`curve`
        
        Usage: pcurve(x, y, param)
        """
        if x is None or numpy.isscalar(x) or numpy.isscalar(y):
            curve = TaurusCurveItem(param)
            curve.setModels(x,y)
            curve.update_params()
            self.set_curve_axes(curve, xaxis, yaxis)
        else:     
            curve = guiqwt.builder.PlotItemBuilder.pcurve(self, x, y, param, xaxis="bottom", yaxis="left")
        return curve
    
    def image(self, taurusmodel=None, **kwargs):
        """
        Extension to meth:`guiqwt.builder.PlotItemBuilder.image` to support passing a 
        'taurusmodel' as a keyword argument instead passing 'data' or 'filename'.
        """
        
        if taurusmodel is None:
            image = guiqwt.builder.PlotItemBuilder.image(self, **kwargs)
        else:
            title = kwargs.get('title', taurusmodel)
            data = kwargs.get('data',None)
            filename = kwargs.get('filename',None)
            alpha_mask = kwargs.get('alpha_mask',None)
            alpha = kwargs.get('alpha',None) 
            background_color = kwargs.get('background_color',None)
            colormap = kwargs.get('colormap',None)
            xdata = kwargs.get('xdata',[None, None])
            ydata = kwargs.get('ydata',[None, None])
            pixel_size = kwargs.get('pixel_size',None)
            interpolation = kwargs.get('interpolation','linear')
            eliminate_outliers = kwargs.get('eliminate_outliers',None)
            xformat = kwargs.get('xformat','%.1f')
            yformat = kwargs.get('yformat','%.1f')
            zformat = kwargs.get('zformat','%.1f')
            forceRGB = kwargs.get('force_rgb', False)
                     
            assert isinstance(xdata, (tuple, list)) and len(xdata) == 2
            assert isinstance(ydata, (tuple, list)) and len(ydata) == 2
            assert filename is None
            assert data is None
            
            param = ImageParam(title=_("Image"), icon='image.png')
            
            if pixel_size is None:
                xmin, xmax = xdata
                ymin, ymax = ydata
            else:
                attr = taurus.Attribute(taurusmodel)
                valueobj = attr.read()
                attrdata = getattr(valueobj, 'value', numpy.zeros((1,1))) 
                xmin, xmax, ymin, ymax = self.compute_bounds(attrdata, pixel_size)
                
            self.set_image_param(param, title, alpha_mask, alpha, interpolation,
                                   background=background_color,
                                   colormap=colormap,
                                   xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                                   xformat=xformat, yformat=yformat,
                                   zformat=zformat)
            if forceRGB:
                image = TaurusRGBImageItem(param)
            else:
                image = TaurusImageItem(param)
            image.setModel(taurusmodel)
            if eliminate_outliers is not None:
                image.set_lut_range(lut_range_threshold(image, 256, eliminate_outliers))
                
        return image
    
    def rgbimage(self, taurusmodel=None, **kwargs):
        if taurusmodel is None:
            image = guiqwt.builder.PlotItemBuilder.rgbimage(self, **kwargs)
        else:
            image = self.image(taurusmodel=taurusmodel, force_rgb=True, **kwargs)
        return image
            
    
    def ttrend(self, model, taurusparam =None, title=u"",
              color=None, linestyle=None, linewidth=None,
              marker=None, markersize=None, markerfacecolor=None,
              markeredgecolor=None, shade=None, fitted=None,
              curvestyle=None, curvetype=None, baseline=None):
        """
        Make a taurus trend item
        
        :return (TaurusTrendItem): 
        """
        curveparam = CurveParam(icon='curve.png')
        if not title:
            title = model
        self.set_param(curveparam, title, color, linestyle, linewidth, marker,
                         markersize, markerfacecolor, markeredgecolor,
                         shade, fitted, curvestyle, curvetype, baseline)
        
        item = TaurusTrendItem(curveparam=curveparam, taurusparam = taurusparam)
        item.setModel(model)
        item.update_params()
        return item
    
    

#"make" is an instance of the builder (this mimics the structure of guiqwt.builder.make)
make = TaurusPlotItemBuilder()
     

        