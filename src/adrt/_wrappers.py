# Copyright (c) 2020, 2021 Karl Otness, Donsub Rim
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import numpy as np
from . import _adrt_cdefs


def _set_module(module):
    r"""Override ``__module__`` on functions for documentation.

    This is an internal function. Users should not call it. This
    changes the way :func:`help` describes the function. Without this,
    functions in this module are listed as being in ``adrt._wrappers``
    rather than the module that users observe them in. NumPy does this
    for many of their functions which are defined in submodules but
    appear at the top level.
    """

    def decorate(func):
        if module is not None:
            func.__module__ = module
        return func

    return decorate


def _normalize_array(a):
    r"""Ensure provided arrays are in a suitable layout.

    This is an internal function. Users should not call it. Make sure
    that arrays being passed to the extension module have the expected
    memory layout.
    """
    if not isinstance(a, np.ndarray):
        # Explicitly fail if not ndarray (or subclass).
        # Users otherwise may get a confusing error related to the dtype attribute.
        raise TypeError("Provided array must be an instance of numpy.ndarray")
    native_dtype = a.dtype.newbyteorder("=")
    return np.require(a, dtype=native_dtype, requirements=["C_CONTIGUOUS", "ALIGNED"])


@_set_module("adrt")
def adrt(a):
    r"""The Approximate Discrete Radon Transform (ADRT).

    Computes the ADRT of the provided array, `a`. The array `a` may
    have either two or three dimensions. If it has three dimensions,
    the first dimension, is treated as a batch and the ADRT is
    computed for each layer independently. The dimensions of the layer
    data must have equal size N, where N is a power of two. The input
    shape is ``(B?, N, N)``.

    If padding is needed for the input array, consider
    :func:`numpy.pad`.

    The returned array will have a shape of either three or four
    dimensions. The optional fourth dimension has the same size as the
    batch dimension of `a`, if present. The output is divided into
    four quadrants each representing a range of angles. The third and
    fourth axes index into Radon transform displacements and angles,
    respectively. The output has shape: ``(B?, 4, 2 * N - 1, N)``.

    For more information on the construction of the quadrants and the
    contents of this array see: :ref:`adrt-description`.

    Parameters
    ----------
    a : numpy.ndarray of float
        The array of data for which the ADRT should be computed.

    Returns
    -------
    numpy.ndarray
        The ADRT of the provided data.

    Notes
    -----
    The transform implemented here is an approximation to the Radon
    transform and *approximates* the sums along lines with carefully
    chosen angles. Each quadrant slices along a range of :math:`\pi/4`
    radians. For a detailed description of the algorithm see
    :ref:`adrt-description` and refer to the source papers [press06]_,
    [brady98]_.
    """
    return _adrt_cdefs.adrt(_normalize_array(a))


@_set_module("adrt")
def iadrt(a, start=0, end=-1):
    r"""An exact inverse to the ADRT.

    Computes an exact inverse to the ADRT, but only works for exact
    ADRT outputs. The array `a` may have either three or four
    dimensions. If present, the first dimension is a batch dimension.
    The remaining dimensions are the quadrants, and ADRT data. The
    array `a` must have shape ``(B?, 2 * N - 1, N)``, where N is a
    power of two.

    The returned array has the dimension as the ADRT, ``(B?, 2 * N - 1, N)``
    If the input was the ADRT, the exact inverse can be extracted
    by using :func:`adrt.utils.truncate`.

    Parameters
    ----------
    a : numpy.ndarray of float
        An array storing the output of the forward ADRT.

    start : int, optional
        Set ADRT level expected for input

    end : int, optional
        Set ADRT level for output

    Returns
    -------
    numpy.ndarray
        The original ADRT input which produced `a`.

    Warning
    -------
    This inverse is exact *only* if `a` is an exact output of the
    forward ADRT. In other cases this inverse is not appropriate.

    For an alternative, see the :ref:`cginverse` example.

    Notes
    -----
    The inverse here only uses values stored in one of the quadrants.
    For details of the algorithm see :ref:`iadrt-description` or the
    source paper [rim20]_.
    """
    return _adrt_cdefs.iadrt(_normalize_array(a), start, end)


@_set_module("adrt")
def bdrt(a, start=0, end=-1):
    r"""Backprojection for the ADRT.

    Parameters
    ----------
    a : numpy.ndarray of float
        An array storing the output of the forward ADRT.

    start : int, optional
        Set ADRT level expected for input

    end : int, optional
        Set ADRT level for output

    Returns
    -------
    numpy.ndarray
        The backprojection of array `a`.

    Notes
    -----
    For more details on the backprojection implemented here see the
    source paper [press06]_.
    """
    return _adrt_cdefs.bdrt(_normalize_array(a), start, end)


@_set_module("adrt.core")
def num_iters(n):
    r"""Number of adrt iterations needed for an image of size n.

    Many of the algorithms in this package are iterative. For an image
    of size :math:`n \times n` (powers of two), the core loop must be
    run :math:`\log_2(n)` times. This function computes the number of
    iterations necessary and is equivalent to
    :math:`\lceil{\log_2(n)}\rceil`.

    Parameters
    ----------
    n : int
        The integer size of the image array which is to be processed.

    Returns
    -------
    int
        The number of iterations needed to fully process the image of
        size ``n``.
    """
    return _adrt_cdefs.num_iters(n)
