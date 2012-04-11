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
         DO NOT MODIFY THIS FILE, MODIFY include/pearlnecklace.h
         AND RE-RUN THE GENERATOR SCRIPT

"""

from sans.models.BaseComponent import BaseComponent
from sans.models.sans_extension.c_models import CPearlNecklaceModel
import copy    

def create_PearlNecklaceModel():
    obj = PearlNecklaceModel()
    #CPearlNecklaceModel.__init__(obj) is called by PearlNecklaceModel constructor
    return obj

class PearlNecklaceModel(CPearlNecklaceModel, BaseComponent):
    """ 
    Class that evaluates a PearlNecklaceModel model. 
    This file was auto-generated from include/pearlnecklace.h.
    Refer to that file and the structure it contains
    for details of the model.
    List of default parameters:
         scale           = 1.0 
         radius          = 80.0 [A]
         edge_separation = 350.0 [A]
         thick_string    = 2.5 [A]
         num_pearls      = 3.0 
         sld_pearl       = 1e-06 [1/A^(2)]
         sld_string      = 1e-06 [1/A^(2)]
         sld_solv        = 6.3e-06 [1/A^(2)]
         background      = 0.0 
         scale           = 1.0 
         radius          = 80.0 [A]
         edge_separation = 350.0 [A]
         thick_string    = 2.5 [A]
         num_pearls      = 3.0 
         sld_pearl       = 1e-06 [1/A^(2)]
         sld_string      = 1e-06 [1/A^(2)]
         sld_solv        = 6.3e-06 [1/A^(2)]
         background      = 0.0 

    """
        
    def __init__(self):
        """ Initialization """
        
        # Initialize BaseComponent first, then sphere
        BaseComponent.__init__(self)
        #apply(CPearlNecklaceModel.__init__, (self,)) 
        CPearlNecklaceModel.__init__(self)
        
        ## Name of the model
        self.name = "PearlNecklaceModel"
        ## Model description
        self.description ="""Calculate form factor for Pearl Necklace Model
		[Macromol. Symp. 2004, 211, 25-42]
		Parameters:
		background:background
		scale: scale factor
		sld_pearl: the SLD of the pearl spheres
		sld_string: the SLD of the strings
		sld_solv: the SLD of the solvent
		num_pearls: number of the pearls
		radius: the radius of a pearl
		edge_separation: the length of string segment; surface to surface
		thick_string: thickness (ie, diameter) of the string"""
       
        ## Parameter details [units, min, max]
        self.details = {}
        self.details['scale'] = ['', None, None]
        self.details['radius'] = ['[A]', None, None]
        self.details['edge_separation'] = ['[A]', None, None]
        self.details['thick_string'] = ['[A]', None, None]
        self.details['num_pearls'] = ['', None, None]
        self.details['sld_pearl'] = ['[1/A^(2)]', None, None]
        self.details['sld_string'] = ['[1/A^(2)]', None, None]
        self.details['sld_solv'] = ['[1/A^(2)]', None, None]
        self.details['background'] = ['', None, None]
        self.details['scale'] = ['', None, None]
        self.details['radius'] = ['[A]', None, None]
        self.details['edge_separation'] = ['[A]', None, None]
        self.details['thick_string'] = ['[A]', None, None]
        self.details['num_pearls'] = ['', None, None]
        self.details['sld_pearl'] = ['[1/A^(2)]', None, None]
        self.details['sld_string'] = ['[1/A^(2)]', None, None]
        self.details['sld_solv'] = ['[1/A^(2)]', None, None]
        self.details['background'] = ['', None, None]

        ## fittable parameters
        self.fixed=['radius.width', 'edge_separation.width']
        
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
        return (create_PearlNecklaceModel,tuple(), state, None, None)
        
    def clone(self):
        """ Return a identical copy of self """
        return self._clone(PearlNecklaceModel())   
       	
   
    def run(self, x=0.0):
        """ 
        Evaluate the model
        
        :param x: input q, or [q,phi]
        
        :return: scattering function P(q)
        
        """
        
        return CPearlNecklaceModel.run(self, x)
   
    def runXY(self, x=0.0):
        """ 
        Evaluate the model in cartesian coordinates
        
        :param x: input q, or [qx, qy]
        
        :return: scattering function P(q)
        
        """
        
        return CPearlNecklaceModel.runXY(self, x)
        
    def evalDistribution(self, x=[]):
        """ 
        Evaluate the model in cartesian coordinates
        
        :param x: input q[], or [qx[], qy[]]
        
        :return: scattering function P(q[])
        
        """
        return CPearlNecklaceModel.evalDistribution(self, x)
        
    def calculate_ER(self):
        """ 
        Calculate the effective radius for P(q)*S(q)
        
        :return: the value of the effective radius
        
        """       
        return CPearlNecklaceModel.calculate_ER(self)
        
    def calculate_VR(self):
        """ 
        Calculate the volf ratio for P(q)*S(q)
        
        :return: the value of the volf ratio
        
        """       
        return CPearlNecklaceModel.calculate_VR(self)
              
    def set_dispersion(self, parameter, dispersion):
        """
        Set the dispersion object for a model parameter
        
        :param parameter: name of the parameter [string]
        :param dispersion: dispersion object of type DispersionModel
        
        """
        return CPearlNecklaceModel.set_dispersion(self, parameter, dispersion.cdisp)
        
   
# End of file
