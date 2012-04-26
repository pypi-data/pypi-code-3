"""BPOD class"""

import numpy as N
from vectorspace import VectorSpace
import util
import parallel as parallel_mod
parallel = parallel_mod.parallel_default_instance
import vectors as V

class BPOD(object):
    """Balanced Proper Orthogonal Decomposition
    
    Kwargs:
        inner_product: Function to take inner products
        
        put_mat: Function to put a matrix out of modred
      	
      	get_mat: Function to get a matrix into modred

        max_vecs_per_node: max number of vectors in memory per node.

        verbosity: 0 prints almost nothing, 1 prints progress and warnings
   
    Computes direct and adjoint modes from direct and adjoint vecs.
    It uses :py:class:`vectorspace.VectorSpace` for low level functions.
    
    Usage::
    
      myBPOD = BPOD(my_inner_product, max_vecs_per_node=500)
      myBPOD.compute_decomp(direct_vec_handles, adjoint_vec_handles)
      myBPOD.compute_direct_modes(range(50), direct_mode_handles)
      myBPOD.compute_adjoint_modes(range(50), adjoint_mode_handles)

    See also :mod:`vectors`.
    """
    def __init__(self, inner_product, 
        put_mat=util.save_array_text, get_mat=util.load_array_text,
        max_vecs_per_node=None, verbosity=1):
        """Constructor """
        # Class that contains all of the low-level vec operations
        # and parallelizes them.
        self.vec_space = VectorSpace(inner_product=inner_product, 
            max_vecs_per_node=max_vecs_per_node, verbosity=verbosity)
        self.get_mat = get_mat
        self.put_mat = put_mat
        self.verbosity = verbosity
        self.L_sing_vecs = None
        self.R_sing_vecs = None
        self.sing_vals = None
        self.direct_vec_handles = None
        self.adjoint_vec_handles = None
        self.direct_vecs = None
        self.adjoint_vecs = None
        self.hankel_mat = None
        
    def sanity_check(self, test_vec_handle):
        """Check user-supplied vector handle.
        
        Args:
            test_vec_handle: a vector handle.
        
        See :py:meth:`vectorspace.VectorSpace.sanity_check`.
        """
        self.vec_space.sanity_check(test_vec_handle)

    def sanity_check_in_memory(self, test_vec):
        """Check user-supplied vector object.
        
        Args:
            test_vec: a vector.
        
        See :py:meth:`vectorspace.VectorSpace.sanity_check_in_memory`.
        """
        self.vec_space.sanity_check_in_memory(test_vec_handle)
    
    
    def get_decomp(self, L_sing_vecs_source, sing_vals_source, 
        R_sing_vecs_source):
        """Gets the decomposition matrices from elsewhere (memory or file)."""
        if self.get_mat is None:
            raise util.UndefinedError('Must specify a get_mat function')
        if parallel.is_rank_zero():
            self.L_sing_vecs = self.get_mat(L_sing_vecs_source)
            self.sing_vals = N.squeeze(N.array(self.get_mat(sing_vals_source)))
            self.R_sing_vecs = self.get_mat(R_sing_vecs_source)
        else:
            self.L_sing_vecs = None
            self.sing_vals = None
            self.R_sing_vecs = None
        if parallel.is_distributed():
            self.L_sing_vecs = parallel.comm.bcast(self.L_sing_vecs,
                root=0)
            self.sing_vals = parallel.comm.bcast(self.sing_vals,
                root=0)
            self.R_sing_vecs = parallel.comm.bcast(self.L_sing_vecs, 
                root=0)
    
    
    def put_hankel_mat(self, hankel_mat_dest):
        """Put Hankel mat"""
        if self.put_mat is None:
            raise util.UndefinedError('put_mat not specified')
        elif parallel.is_rank_zero():
            self.put_mat(self.hankel_mat, hankel_mat_dest)           
        parallel.barrier()
    
    def put_L_sing_vecs(self, dest):
        """Put left singular vectors of SVD, V"""
        if self.put_mat is None:
            raise util.UndefinedError("put_mat not specified")
        elif parallel.is_rank_zero():
            self.put_mat(self.L_sing_vecs, dest)
        parallel.barrier()
        
    def put_R_sing_vecs(self, dest):
        """Put right singular vectors of SVD, U"""
        if self.put_mat is None:
            raise util.UndefinedError("put_mat not specified")
        elif parallel.is_rank_zero():
            self.put_mat(self.R_sing_vecs, dest)
        parallel.barrier()
        
    def put_sing_vals(self, dest):
        """Put singular values of SVD, E"""
        if self.put_mat is None:
            raise util.UndefinedError("put_mat not specified")
        elif parallel.is_rank_zero():
            self.put_mat(self.sing_vals, dest)
        parallel.barrier()
    
    def put_decomp(self, L_sing_vecs_dest, sing_vals_dest, R_sing_vecs_dest):
        """Save the decomposition matrices to file."""
        self.put_L_sing_vecs(L_sing_vecs_dest)
        self.put_R_sing_vecs(R_sing_vecs_dest)
        self.put_sing_vals(sing_vals_dest)
    
    
    def compute_decomp(self, direct_vec_handles, adjoint_vec_handles):
        """Finds Hankel matrix and its SVD.
        
        Args:
            direct_vec_handles: list of handles for direct vecs
            
            adjoint_vec_handles: list of handles for adjoint vecs
        
        Returns:
            L_sing_vecs: matrix of left singular vectors (U in UEV*=H)
        
            sing_vals: 1D array of singular values (E in UEV*=H)
            
            R_sing_vecs: matrix of right singular vectors (V in UEV*=H)
        """
        self.direct_vec_handles = direct_vec_handles
        self.adjoint_vec_handles = adjoint_vec_handles
        self.hankel_mat = self.vec_space.compute_inner_product_mat(
            self.adjoint_vec_handles, self.direct_vec_handles)
        self.compute_SVD()
        return self.L_sing_vecs, self.sing_vals, self.R_sing_vecs
        
    def compute_decomp_in_memory(self, direct_vecs, adjoint_vecs):
        """Finds Hankel matrix and its SVD.
        
        Args:
            direct_vecs: list of direct vecs
            
            adjoint_vecs: list of adjoint vecs
        
        Returns:
            L_sing_vecs: matrix of left singular vectors (U in UEV*=H)
        
            sing_vals: 1D array of singular values (E in UEV*=H)
            
            R_sing_vecs: matrix of right singular vectors (V in UEV*=H)
        
        See :py:meth:`compute_decomp`.
        """
        self.direct_vecs = direct_vecs
        self.adjoint_vecs = adjoint_vecs
        self.hankel_mat = self.vec_space.compute_inner_product_mat_in_memory(
            self.adjoint_vecs, self.direct_vecs)
        self.compute_SVD()
        return self.L_sing_vecs, self.sing_vals, self.R_sing_vecs
        

    def compute_SVD(self):
        """Takes the SVD of the Hankel matrix.
        
        Useful if you already have the Hankel mat and want to skip 
        recomputing it. Instead, set ``self.hankel_mat``, and call this.
        """
        if parallel.is_rank_zero():
            self.L_sing_vecs, self.sing_vals, self.R_sing_vecs = \
                util.svd(self.hankel_mat)
        else:
            self.L_sing_vecs = None
            self.R_sing_vecs = None
            self.sing_vals = None
        if parallel.is_distributed():
            self.L_sing_vecs = parallel.comm.bcast(self.L_sing_vecs,
                root=0)
            self.sing_vals = parallel.comm.bcast(self.sing_vals,
                root=0)
            self.R_sing_vecs = parallel.comm.bcast(self.R_sing_vecs,
                root=0)
    
    
    
    def _compute_direct_build_coeff_mat(self):
        """Computes build coeff matrix for direct modes"""
        #self.R_sing_vecs and self.sing_vals must exist, else UndefinedError.
        if self.R_sing_vecs is None:
            raise util.UndefinedError('Must define self.R_sing_vecs')
        if self.sing_vals is None:
            raise util.UndefinedError('Must define self.sing_vals')
        self.sing_vals = N.squeeze(N.array(self.sing_vals))
        build_coeff_mat = N.dot(self.R_sing_vecs, N.diag(self.sing_vals**-0.5))
        return build_coeff_mat
        
    def compute_direct_modes_in_memory(self, mode_nums, 
        direct_vecs=None, index_from=0):
        """Computes direct modes and returns them.
        
        Args:
          mode_nums: Mode numbers to compute. 
              Examples are ``range(10)`` or ``[3, 1, 6, 8]``. 
              
        Kwargs:
          direct_vecs: list of direct vecs. 
              Optional if already given when calling 
              :py:meth:`compute_decomp_in_memory`.

          index_from: Index modes starting from 0, 1, or other.

        Returns:
            list of modes
            
        In parallel, each MPI worker is returned a complete list of modes.
        See :py:meth:`compute_direct_modes`.
        """
        if direct_vecs is not None:
            self.direct_vecs = util.make_list(direct_vecs)
            direct_vec_handles = [V.InMemoryVecHandle(v) for v in direct_vecs]
        if self.direct_vecs is None:
            raise util.UndefinedError('direct_vecs not specified')
        build_coeff_mat = self._compute_direct_build_coeff_mat()
        return self.vec_space.compute_modes_in_memory(mode_nums, 
            self.direct_vecs, build_coeff_mat, index_from=index_from)
            
    def compute_direct_modes(self, mode_nums, mode_handles,
        direct_vec_handles=None, index_from=0):
        """Computes direct modes and calls ``mode_handle.put`` on them.
        
        Args:
          mode_nums: Mode numbers to compute. 
              Examples are ``range(10)`` or ``[3, 1, 6, 8]``. 
              
          mode_handles: list of handles for modes.
          
        Kwargs:
          direct_vec_handles: list of handles for direct vecs. 
              Optional if already given when calling :py:meth:`compute_decomp`.

          index_from: Index modes starting from 0, 1, or other.
        """
        if direct_vec_handles is not None:
            self.direct_vec_handles = util.make_list(direct_vec_handles)
        if self.direct_vec_handles is None:
            raise util.UndefinedError('direct_vec_handles not specified')
        build_coeff_mat = self._compute_direct_build_coeff_mat()
        self.vec_space.compute_modes(mode_nums, mode_handles, 
            self.direct_vec_handles, build_coeff_mat, index_from=index_from)
        
        
    
    def _compute_adjoint_build_coeff_mat(self):
        """Computes build coeff matrix for direct modes."""
        #self.L_sing_vecs and self.sing_vals must exist, else UndefinedError.
        
        if self.L_sing_vecs is None:
            raise util.UndefinedError('Must define self.L_sing_vecs')
        if self.sing_vals is None:
            raise util.UndefinedError('Must define self.sing_vals')
        self.sing_vals = N.squeeze(N.array(self.sing_vals))
        build_coeff_mat = N.dot(self.L_sing_vecs, N.diag(self.sing_vals**-0.5))
        return build_coeff_mat      
    
    def compute_adjoint_modes_in_memory(self, mode_nums, 
        adjoint_vecs=None, index_from=0):
        """Computes adjoint modes, calls ``mode_handle.put`` on them.
        
        Args:
          mode_nums: Mode numbers to compute. 
              Examples are ``range(10)`` or ``[3, 1, 6, 8]``. 
              
        Kwargs:
          adjoint_vecs: list of adjoint vecs. 
              Optional if already given when calling 
              :py:meth:`compute_decomp_in_memory`.

          index_from: Index modes starting from 0, 1, or other.
        
        Returns:
            list of modes
            
        In parallel, each MPI worker is returned a complete list of modes
        See :py:meth:`compute_adjoint_modes` for details.
        """
        if adjoint_vecs is not None:
            self.adjoint_vecs = util.make_list(adjoint_vecs)
            adjoint_vec_handles = [V.InMemoryVecHandle(v) for v in adjoint_vecs]
        if self.adjoint_vecs is None:
            raise util.UndefinedError('adjoint_vecs not specified')
        build_coeff_mat = self._compute_adjoint_build_coeff_mat()
        return self.vec_space.compute_modes_in_memory(mode_nums, 
            self.adjoint_vecs, build_coeff_mat, index_from=index_from)
            
    def compute_adjoint_modes(self, mode_nums, mode_handles,
        adjoint_vec_handles=None, index_from=0):
        """Computes adjoint modes, calls ``mode_handle.put`` on them.
        
        Args:
          mode_nums: Mode numbers to compute. 
              Examples are ``range(10)`` or ``[3, 1, 6, 8]``. 
              
          mode_handles: list of handles for modes.
          
        Kwargs:
          adjoint_vec_handles: list of handles for adjoint vecs. 
              Optional if already given when calling :py:meth:`compute_decomp`.

          index_from: Index modes starting from 0, 1, or other.
        """
        if adjoint_vec_handles is not None:
            self.adjoint_vec_handles = util.make_list(adjoint_vec_handles)
        if self.adjoint_vec_handles is None:
            raise util.UndefinedError('adjoint_vec_handles not specified')
        build_coeff_mat = self._compute_adjoint_build_coeff_mat()
        self.vec_space.compute_modes(mode_nums, mode_handles, 
            self.adjoint_vec_handles, build_coeff_mat, index_from=index_from)
    
