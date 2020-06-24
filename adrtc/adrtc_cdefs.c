/*
 * Copyright (C) 2020 by the ADRT Development Team
 * All right reserved
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#define PY_SSIZE_T_CLEAN
#define PY_LIMITED_API 0x03040000
#include "Python.h"

static PyMethodDef adrtc_cdefs_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef adrtc_cdefs_module = {
    PyModuleDef_HEAD_INIT,
    "_adrtc_cdefs",
    "C routines for ADRTC. These should not be called directly by module users.",
    0,
    adrtc_cdefs_methods,
    NULL,
    // GC hooks below, unused
    NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__adrtc_cdefs(void)
{
    PyObject *module = PyModule_Create(&adrtc_cdefs_module);
    if (!module) {
        return NULL;
    }
    return module;
}
