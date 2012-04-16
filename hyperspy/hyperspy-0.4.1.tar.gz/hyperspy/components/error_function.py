# -*- coding: utf-8 -*-
# Copyright 2007-2011 The Hyperspy developers
#
# This file is part of  Hyperspy.
#
#  Hyperspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  Hyperspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  Hyperspy.  If not, see <http://www.gnu.org/licenses/>.

import math

import numpy as np
from scipy.special import erf

from hyperspy.component import Component

sqrt2pi = np.sqrt(2*np.pi)

class Erf(Component):
    """Error function component
    
    Attributes
    ----------
    A : float
    sigma : float
    origin : float
    """

    def __init__(self):
        Component.__init__(self, ['A','sigma','origin'])        
                
        # Boundaries
        self.A.bmin = 0.
        self.A.bmax = None
        
        self.sigma.bmin = None
        self.sigma.bmax = None


        self.isbackground = False
        self.convolved = True
        
        # Gradients
        self.A.grad = self.grad_A
        self.sigma.grad = self.grad_sigma
        self.origin.grad = self.grad_origin

    def function(self, x):
        A = self.A.value
        sigma = self.sigma.value
        origin = self.origin.value
        return A*erf((x-origin)/math.sqrt(2)/sigma)/2

    def grad_A(self, x):
        A = self.A.value
        sigma = self.sigma.value
        origin = self.origin.value
        return erf((x-origin)/math.sqrt(2)/sigma)/2
    def grad_sigma(self,x):
        A = self.A.value
        sigma = self.sigma.value
        origin = self.origin.value
        return ((origin/(math.sqrt(2)*sigma**2)-x/(math.sqrt(2)*sigma**2))*np.exp(-(x/(math.sqrt(2)*sigma)-origin/(math.sqrt(2)*sigma))**2)*A)/math.sqrt(math.pi)
    def grad_origin(self,x):
        A = self.A.value
        sigma = self.sigma.value
        origin = self.origin.value
        return -(np.exp(-(x/(math.sqrt(2)*sigma)-origin/(math.sqrt(2)*sigma))**2)*A)/(math.sqrt(2)*math.sqrt(math.pi)*sigma)
