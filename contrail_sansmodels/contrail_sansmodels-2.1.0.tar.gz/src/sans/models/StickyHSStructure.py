#!/usr/bin/env python

##############################################################################
#	This software was developed by the University of Tennessee as part of the
#	Distributed Data Analysis of Neutron Scattering Experiments (DANSE)
#	project funded by the US National Science Foundation.
#
#	If you use DANSE applications to do scientific research that leads to
#	publication, we ask that you acknowledge the use of the software with the
#	following sentence:
#
#	"This work benefited from DANSE software developed under NSF award DMR-0520547."
#
#	copyright 2008, University of Tennessee
##############################################################################


""" 
Provide functionality for a C extension model

:WARNING: THIS FILE WAS GENERATED BY WRAPPERGENERATOR.PY
         DO NOT MODIFY THIS FILE, MODIFY include/StickyHS.h
         AND RE-RUN THE GENERATOR SCRIPT

"""

from sans.models.BaseComponent import BaseComponent
from sans.models.sans_extension.c_models import CStickyHSStructure
import copy    

def create_StickyHSStructure():
    obj = StickyHSStructure()
    #CStickyHSStructure.__init__(obj) is called by StickyHSStructure constructor
    return obj

class StickyHSStructure(CStickyHSStructure, BaseComponent):
    """ 
    Class that evaluates a StickyHSStructure model. 
    This file was auto-generated from include/StickyHS.h.
    Refer to that file and the structure it contains
    for details of the model.
    List of default parameters:
         effect_radius   = 50.0 [A]
         volfraction     = 0.1 
         perturb         = 0.05 
         stickiness      = 0.2 

    """
        
    def __init__(self):
        """ Initialization """
        
        # Initialize BaseComponent first, then sphere
        BaseComponent.__init__(self)
        #apply(CStickyHSStructure.__init__, (self,)) 
        CStickyHSStructure.__init__(self)
        
        ## Name of the model
        self.name = "StickyHSStructure"
        ## Model description
        self.description =""" Structure Factor for interacting particles:                               .
		
		The interaction potential is
		
		U(r)= inf , r < 2R
		= -Uo  , 2R < r < 2R + w
		= 0   , r >= 2R +w
		
		R: effective radius of the hardsphere
		stickiness = [exp(Uo/kT)]/(12*perturb)
		perturb = w/(w+ 2R) , 0.01 =< w <= 0.1
		w: The width of the square well ,w > 0
		v: The volume fraction , v > 0
		
		Ref: Menon, S. V. G.,et.al., J. Chem.
		Phys., 1991, 95(12), 9186-9190."""
       
        ## Parameter details [units, min, max]
        self.details = {}
        self.details['effect_radius'] = ['[A]', None, None]
        self.details['volfraction'] = ['', None, None]
        self.details['perturb'] = ['', None, None]
        self.details['stickiness'] = ['', None, None]

        ## fittable parameters
        self.fixed=['effect_radius.width']
        
        ## non-fittable parameters
        self.non_fittable = []
        
        ## parameters with orientation
        self.orientation_params = []

    def __setstate__(self, state):
        """
        restore the state of a model from pickle
        """
        self.__dict__, self.params, self.dispersion = state
        
    def __reduce_ex__(self, proto):
        """
        Overwrite the __reduce_ex__ of PyTypeObject *type call in the init of 
        c model.
        """
        state = (self.__dict__, self.params, self.dispersion)
        return (create_StickyHSStructure,tuple(), state, None, None)
        
    def clone(self):
        """ Return a identical copy of self """
        return self._clone(StickyHSStructure())   
       	
   
    def run(self, x=0.0):
        """ 
        Evaluate the model
        
        :param x: input q, or [q,phi]
        
        :return: scattering function P(q)
        
        """
        
        return CStickyHSStructure.run(self, x)
   
    def runXY(self, x=0.0):
        """ 
        Evaluate the model in cartesian coordinates
        
        :param x: input q, or [qx, qy]
        
        :return: scattering function P(q)
        
        """
        
        return CStickyHSStructure.runXY(self, x)
        
    def evalDistribution(self, x=[]):
        """ 
        Evaluate the model in cartesian coordinates
        
        :param x: input q[], or [qx[], qy[]]
        
        :return: scattering function P(q[])
        
        """
        return CStickyHSStructure.evalDistribution(self, x)
        
    def calculate_ER(self):
        """ 
        Calculate the effective radius for P(q)*S(q)
        
        :return: the value of the effective radius
        
        """       
        return CStickyHSStructure.calculate_ER(self)
        
    def calculate_VR(self):
        """ 
        Calculate the volf ratio for P(q)*S(q)
        
        :return: the value of the volf ratio
        
        """       
        return CStickyHSStructure.calculate_VR(self)
              
    def set_dispersion(self, parameter, dispersion):
        """
        Set the dispersion object for a model parameter
        
        :param parameter: name of the parameter [string]
        :param dispersion: dispersion object of type DispersionModel
        
        """
        return CStickyHSStructure.set_dispersion(self, parameter, dispersion.cdisp)
        
   
# End of file
