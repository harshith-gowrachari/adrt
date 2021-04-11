/*
 * Copyright (c) 2020, 2021 Karl Otness, Donsub Rim
 * All rights reserved
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

#include "adrt_cdefs_common.hpp"
#include <limits>

namespace {

inline int adrt_num_iters_fallback(size_t shape) {
    // Relies on earlier check that shape != 0
    bool is_power_of_two = adrt_is_pow2(shape);
    int r = 0;
    while(shape != 0) {
        ++r;
        shape >>= 1;
    }
    return r + (is_power_of_two ? 0 : 1) - 1;
}

// Implementation of adrt_num_iters

#if defined(__GNUC__) || defined(__clang__) // GCC intrinsics

inline int adrt_num_iters_impl(size_t shape) {
    // Relies on earlier check that shape != 0
    bool is_power_of_two = adrt_is_pow2(shape);
    if(std::numeric_limits<size_t>::max() <= std::numeric_limits<unsigned int>::max()) {
        unsigned int ushape = static_cast<unsigned int>(shape);
        int lead_zero = __builtin_clz(ushape);
        return (std::numeric_limits<unsigned int>::digits - 1) - lead_zero + (is_power_of_two ? 0 : 1);
    }
    else if(std::numeric_limits<size_t>::max() <= std::numeric_limits<unsigned long>::max()) {
        unsigned long ushape = static_cast<unsigned long>(shape);
        int lead_zero = __builtin_clzl(ushape);
        return (std::numeric_limits<unsigned long>::digits - 1) - lead_zero + (is_power_of_two ? 0 : 1);
    }
    else if(std::numeric_limits<size_t>::max() <= std::numeric_limits<unsigned long long>::max()) {
        unsigned long long ushape = static_cast<unsigned long long>(shape);
        int lead_zero = __builtin_clzll(ushape);
        return (std::numeric_limits<unsigned long long>::digits - 1) - lead_zero + (is_power_of_two ? 0 : 1);
    }
    return adrt_num_iters_fallback(shape);
}

#elif defined(_MSC_VER) // MSVC intrinsics

#include <intrin.h>

inline int adrt_num_iters_impl(size_t shape) {
    // Relies on earlier check that shape != 0
    bool is_power_of_two = adrt_is_pow2(shape);
    if(std::numeric_limits<size_t>::max() <= std::numeric_limits<unsigned long>::max()) {
        unsigned long index;
        unsigned long ushape = static_cast<unsigned long>(shape);
        _BitScanReverse(&index, ushape);
        return index + (is_power_of_two ? 0 : 1);
    }

    #if defined(_M_X64) || defined(_M_ARM64)
    else if(std::numeric_limits<size_t>::max() <= std::numeric_limits<unsigned __int64>::max()) {
        unsigned long index;
        unsigned __int64 ushape = static_cast<unsigned __int64>(shape);
        _BitScanReverse64(&index, ushape);
        return index + (is_power_of_two ? 0 : 1);
    }
    #endif // End: 64bit arch

    return adrt_num_iters_fallback(shape);
}

#else // Fallback only

inline int adrt_num_iters_impl(size_t shape) {
    return adrt_num_iters_fallback(shape);
}

#endif // End platform cases

} // End anonymous namespace
int adrt_num_iters(size_t shape) {
    if(shape <= 1) {
        return 0;
    }
    return adrt_num_iters_impl(shape);
}
