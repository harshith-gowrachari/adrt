# Copyright (c) 2022 Karl Otness, Donsub Rim
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


import pytest
import numpy as np
import adrt


@pytest.mark.parametrize("dtype", ["float32", "float64"])
def test_unique_values(dtype):
    size = 8
    orig = np.arange(size**2).reshape((size, size)).astype(dtype)
    inarr = adrt.adrt(orig)
    inv = adrt.iadrt_fmg(inarr, max_iters=50)
    assert inv.dtype == orig.dtype
    assert inv.shape == orig.shape
    assert inv.flags.writeable
    assert np.allclose(inv, orig, atol=1e-3)


def test_rejects_non_integer_max_iters():
    size = 8
    inarr = np.zeros((4, 2 * size - 1, size), dtype="float32")
    with pytest.raises(ValueError):
        _ = adrt.iadrt_fmg(inarr, max_iters=2.0)


def test_rejects_zero_max_iters():
    size = 8
    inarr = np.zeros((4, 2 * size - 1, size), dtype="float32")
    with pytest.raises(ValueError):
        _ = adrt.iadrt_fmg(inarr, max_iters=0)


def test_rejects_batch_dimension():
    size = 8
    inarr = np.zeros((3, 4, 2 * size - 1, size), dtype="float32")
    with pytest.raises(ValueError):
        _ = adrt.iadrt_fmg(inarr, max_iters=50)


def test_stops_quickly_on_zero(monkeypatch):
    size = 16
    inarr = np.zeros((4, 2 * size - 1, size), dtype="float64")
    count = 0
    orig_fn = adrt.core.iadrt_fmg_step

    def counting_inv(a, /):
        nonlocal count
        count += 1
        return orig_fn(a)

    monkeypatch.setattr(adrt.core, "iadrt_fmg_step", counting_inv)
    inv = adrt.iadrt_fmg(inarr, max_iters=50)
    assert count <= 2
    assert np.allclose(inv, 0)
    assert inv.shape == (size, size)
    assert inv.dtype == inarr.dtype


@pytest.mark.parametrize("max_iters", [1, 2, 3, 4])
def test_max_iters_limits_iterations(monkeypatch, max_iters):
    size = 16
    orig = np.arange(size**2).reshape((size, size)).astype("float64")
    inarr = adrt.adrt(orig)
    count = 0
    orig_fn = adrt.core.iadrt_fmg_step

    def counting_inv(a, /):
        nonlocal count
        count += 1
        return orig_fn(a)

    monkeypatch.setattr(adrt.core, "iadrt_fmg_step", counting_inv)
    _ = adrt.iadrt_fmg(inarr, max_iters=max_iters)
    assert count == max_iters
