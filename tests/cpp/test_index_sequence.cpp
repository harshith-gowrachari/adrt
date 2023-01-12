/*
 * Copyright Karl Otness, Donsub Rim
 *
 * SPDX-License-Identifier: BSD-3-Clause
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

#include <type_traits>
#include "catch2/catch.hpp"
#include "adrt_cdefs_common.hpp"

TEST_CASE("make_index_sequence produces correct sequences", "[common][index_sequence][make_index_sequence]") {
    STATIC_REQUIRE(std::is_same<adrt::_common::make_index_sequence<0>, adrt::_common::index_sequence<>>::value);
    STATIC_REQUIRE(std::is_same<adrt::_common::make_index_sequence<1>, adrt::_common::index_sequence<0>>::value);
    STATIC_REQUIRE(std::is_same<adrt::_common::make_index_sequence<2>, adrt::_common::index_sequence<0, 1>>::value);
    STATIC_REQUIRE(std::is_same<adrt::_common::make_index_sequence<3>, adrt::_common::index_sequence<0, 1, 2>>::value);
    STATIC_REQUIRE(std::is_same<adrt::_common::make_index_sequence<4>, adrt::_common::index_sequence<0, 1, 2, 3>>::value);
}
