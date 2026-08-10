cmake_minimum_required(VERSION 3.16)
project(gbref_runner C CXX)
set(GBRT_RUNTIME_DIR "$ENV{HOME}/.local/gbrecomp/gb-recompiled-linux/runtime" CACHE PATH
    "Pinned GB Recompiled runtime source tree")
if(NOT IS_DIRECTORY "${GBRT_RUNTIME_DIR}/include" OR
   NOT EXISTS "${GBRT_RUNTIME_DIR}/include/gbrt.h")
    message(FATAL_ERROR
        "ARTIFACT: GBRT runtime headers missing; expected ${GBRT_RUNTIME_DIR}/include/gbrt.h")
endif()

set(BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(GBRECOMP_ENABLE_NATIVE_PATCHES OFF CACHE BOOL "" FORCE)
add_subdirectory("${GBRT_RUNTIME_DIR}" "${CMAKE_BINARY_DIR}/gbrt")

add_executable(gbref_runner runner.c)
target_compile_features(gbref_runner PRIVATE c_std_11)
target_include_directories(gbref_runner PRIVATE "${GBRT_RUNTIME_DIR}/include")
target_link_libraries(gbref_runner PRIVATE gbrt)

install(TARGETS gbref_runner RUNTIME DESTINATION bin)
