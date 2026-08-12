cmake_minimum_required(VERSION 3.16)
project(gbref_runner C CXX)
set(GBRT_RUNTIME_DIR "$ENV{HOME}/.local/gbrecomp/gb-recompiled-linux/runtime" CACHE PATH
    "Pinned GB Recompiled runtime source tree")
if(NOT IS_DIRECTORY "${GBRT_RUNTIME_DIR}/include" OR
   NOT EXISTS "${GBRT_RUNTIME_DIR}/include/gbrt.h")
    message(FATAL_ERROR
        "ARTIFACT: GBRT runtime headers missing; expected ${GBRT_RUNTIME_DIR}/include/gbrt.h")
endif()

set(GBRT_BUILD_DIR "${CMAKE_BINARY_DIR}/gbrt-source")
set(GBRT_PATCH "${CMAKE_CURRENT_SOURCE_DIR}/gbrt-mbc5.patch")
find_program(GBRT_PATCH_EXECUTABLE patch)
if(NOT GBRT_PATCH_EXECUTABLE)
    message(FATAL_ERROR "GBRT MBC5 patch requires the patch executable")
endif()
file(SHA256 "${GBRT_PATCH}" GBRT_PATCH_HASH)
file(SHA256 "${GBRT_RUNTIME_DIR}/include/gbrt.h" GBRT_RUNTIME_HASH)
set(GBRT_STAMP_CONTENT "${GBRT_RUNTIME_DIR}|${GBRT_RUNTIME_HASH}|${GBRT_PATCH_HASH}")
set(GBRT_STAMP_FILE "${GBRT_BUILD_DIR}.stamp")
set(GBRT_NEED_COPY TRUE)
if(EXISTS "${GBRT_STAMP_FILE}" AND IS_DIRECTORY "${GBRT_BUILD_DIR}")
    file(READ "${GBRT_STAMP_FILE}" GBRT_STAMP_PREVIOUS)
    if(GBRT_STAMP_PREVIOUS STREQUAL GBRT_STAMP_CONTENT)
        set(GBRT_NEED_COPY FALSE)
    endif()
endif()
if(GBRT_NEED_COPY)
    file(REMOVE_RECURSE "${GBRT_BUILD_DIR}")
    file(COPY "${GBRT_RUNTIME_DIR}/" DESTINATION "${GBRT_BUILD_DIR}")
    execute_process(
        COMMAND "${GBRT_PATCH_EXECUTABLE}" --dry-run --batch --forward -p1
            --input "${GBRT_PATCH}"
        WORKING_DIRECTORY "${GBRT_BUILD_DIR}"
        RESULT_VARIABLE GBRT_PATCH_CHECK_RESULT
        OUTPUT_VARIABLE GBRT_PATCH_CHECK_OUTPUT
        ERROR_VARIABLE GBRT_PATCH_CHECK_ERROR)
    if(NOT GBRT_PATCH_CHECK_RESULT EQUAL 0)
        message(FATAL_ERROR
            "GBRT MBC5 patch check failed: ${GBRT_PATCH_CHECK_ERROR}${GBRT_PATCH_CHECK_OUTPUT}")
    endif()
    execute_process(
        COMMAND "${GBRT_PATCH_EXECUTABLE}" --batch --forward -p1
            --input "${GBRT_PATCH}"
        WORKING_DIRECTORY "${GBRT_BUILD_DIR}"
        RESULT_VARIABLE GBRT_PATCH_RESULT
        OUTPUT_VARIABLE GBRT_PATCH_OUTPUT
        ERROR_VARIABLE GBRT_PATCH_ERROR)
    if(NOT GBRT_PATCH_RESULT EQUAL 0)
        message(FATAL_ERROR
            "GBRT MBC5 patch application failed: ${GBRT_PATCH_ERROR}${GBRT_PATCH_OUTPUT}")
    endif()
    file(WRITE "${GBRT_STAMP_FILE}" "${GBRT_STAMP_CONTENT}")
endif()

set(BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(GBRECOMP_ENABLE_NATIVE_PATCHES OFF CACHE BOOL "" FORCE)
add_subdirectory("${GBRT_BUILD_DIR}" "${CMAKE_BINARY_DIR}/gbrt")

add_executable(gbref_runner runner.c)
target_compile_features(gbref_runner PRIVATE c_std_11)
target_include_directories(gbref_runner PRIVATE "${GBRT_BUILD_DIR}/include")
target_link_libraries(gbref_runner PRIVATE gbrt)

install(TARGETS gbref_runner RUNTIME DESTINATION bin)
