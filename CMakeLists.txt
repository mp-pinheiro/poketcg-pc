cmake_minimum_required(VERSION 3.20)
project(poketcg_pc C)

set(CMAKE_C_STANDARD 11)          # static_assert in the generated layout headers
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Debug CACHE STRING "" FORCE)
endif()

# The pret/poketcg disassembly is a build-time input, never a submodule or a
# committed artifact. `just bootstrap` clones and builds it.
set(POKETCG_DISASM "${CMAKE_SOURCE_DIR}/poketcg" CACHE PATH "pret/poketcg checkout")
set(POKETCG_DATA_PACK "" CACHE FILEPATH "sparse production data pack")
set(POKETCG_SYM "${POKETCG_DISASM}/poketcg.sym")
if(NOT EXISTS "${POKETCG_SYM}")
  message(FATAL_ERROR "missing ${POKETCG_SYM}; run `just bootstrap` (or set -DPOKETCG_DISASM=...)")
endif()

find_package(Threads REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(GEN_DIR "${CMAKE_SOURCE_DIR}/include/generated")
set(GEN_HEADERS "${GEN_DIR}/wram.h" "${GEN_DIR}/hram.h" "${GEN_DIR}/sram.h")
add_custom_command(
  OUTPUT ${GEN_HEADERS}
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_layout.py"
          --sym "${POKETCG_SYM}" --out "${GEN_DIR}"
  DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_layout.py" "${POKETCG_SYM}"
  COMMENT "gen_layout: poketcg.sym -> include/generated"
  VERBATIM)
add_custom_target(gen_layout DEPENDS ${GEN_HEADERS})

# Concurrent ports each build a private subset so one agent's compile error cannot
# red-light the other seven. Empty (the default) builds every ported file.
set(PORT_FILES "" CACHE STRING "semicolon-separated pret basenames to build; empty = all")

file(GLOB HOME_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/home/*.c")
file(GLOB PROBE_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/probe/*.c")

set(EFFECT_DISPATCH_SOURCE "${CMAKE_BINARY_DIR}/effect_dispatch_generated.c")
add_custom_command(
  OUTPUT "${EFFECT_DISPATCH_SOURCE}"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_effect_dispatch.py"
          --probe "${CMAKE_SOURCE_DIR}/src/probe/effect_functions.c"
          --inventory "${CMAKE_SOURCE_DIR}/site/data/inventory.json"
          --output "${EFFECT_DISPATCH_SOURCE}"
  DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_effect_dispatch.py"
          "${CMAKE_SOURCE_DIR}/src/probe/effect_functions.c"
          "${CMAKE_SOURCE_DIR}/site/data/inventory.json"
  COMMENT "gen_effect_dispatch: probe adapters -> production address table"
  VERBATIM)

set(SCRIPT_DISPATCH_SOURCE "${CMAKE_BINARY_DIR}/script_dispatch_generated.c")
add_custom_command(
  OUTPUT "${SCRIPT_DISPATCH_SOURCE}"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_script_dispatch.py"
          --probe "${CMAKE_SOURCE_DIR}/src/probe/scripting.c"
          --table "${CMAKE_SOURCE_DIR}/poketcg/src/data/script_table.asm"
          --output "${SCRIPT_DISPATCH_SOURCE}"
  DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_script_dispatch.py"
          "${CMAKE_SOURCE_DIR}/src/probe/scripting.c"
          "${CMAKE_SOURCE_DIR}/poketcg/src/data/script_table.asm"
  COMMENT "gen_script_dispatch: scripting adapters -> opcode table"
  VERBATIM)

# The table classifies a target by whether src/home declares it, so a new
# declaration has to reconfigure it.
file(GLOB HOME_HEADERS CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/home/*.h")
set(SCRIPT_ENTRY_SOURCE "${CMAKE_BINARY_DIR}/script_entry_dispatch_generated.c")
add_custom_command(
  OUTPUT "${SCRIPT_ENTRY_SOURCE}"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_script_entry_dispatch.py"
          --sym "${CMAKE_SOURCE_DIR}/poketcg/poketcg.sym"
          --rom "${CMAKE_SOURCE_DIR}/poketcg/poketcg.gbc"
          --home "${CMAKE_SOURCE_DIR}/src/home"
          --map-scripts "${CMAKE_SOURCE_DIR}/poketcg/src/data/map_scripts.asm"
          --npc-map-data "${CMAKE_SOURCE_DIR}/poketcg/src/data/npc_map_data.asm"
          --output "${SCRIPT_ENTRY_SOURCE}"
  DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_script_entry_dispatch.py"
          "${CMAKE_SOURCE_DIR}/poketcg/poketcg.sym"
          "${CMAKE_SOURCE_DIR}/poketcg/src/data/map_scripts.asm"
          "${CMAKE_SOURCE_DIR}/poketcg/src/data/npc_map_data.asm"
          ${HOME_HEADERS}
  COMMENT "gen_script_entry_dispatch: poketcg.sym + rom -> script entry table"
  VERBATIM)
if(NOT PORT_FILES)
  list(APPEND HOME_SOURCES "${SCRIPT_ENTRY_SOURCE}")
endif()
if(NOT PORT_FILES)
  list(APPEND HOME_SOURCES "${SCRIPT_DISPATCH_SOURCE}")
endif()
if(NOT PORT_FILES)
  list(APPEND HOME_SOURCES "${EFFECT_DISPATCH_SOURCE}")
endif()

if(PORT_FILES)
  set(KEEP ${PORT_FILES} switch_rom switch_sram)
  set(_home "")
  foreach(src ${HOME_SOURCES})
    get_filename_component(n "${src}" NAME_WE)
    if(n IN_LIST KEEP)
      list(APPEND _home "${src}")
    endif()
  endforeach()
  set(_probe "")
  foreach(src ${PROBE_SOURCES})
    get_filename_component(n "${src}" NAME_WE)
    if(n IN_LIST KEEP)
      list(APPEND _probe "${src}")
    endif()
  endforeach()
  set(HOME_SOURCES ${_home})
  set(PROBE_SOURCES ${_probe})
  message(STATUS "PORT_FILES subset build: ${PORT_FILES}")
endif()

set(BANK_GUARD_SOURCE "${CMAKE_BINARY_DIR}/bank_guard_generated.c")
add_custom_command(
  OUTPUT "${BANK_GUARD_SOURCE}"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_bank_guard.py"
          --sym "${CMAKE_SOURCE_DIR}/poketcg/poketcg.sym"
          --asm-root "${CMAKE_SOURCE_DIR}/poketcg/src"
          --home "${CMAKE_SOURCE_DIR}/src/home"
          --output "${BANK_GUARD_SOURCE}"
  DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_bank_guard.py"
          "${CMAKE_SOURCE_DIR}/poketcg/poketcg.sym"
          ${HOME_HEADERS}
  COMMENT "gen_bank_guard: farcall targets -> required bank table"
  VERBATIM)

set(GBMEM_SOURCES src/mem.c src/ppu.c src/runtime_events.c src/trace.c
                  src/bank_guard.c ${HOME_SOURCES})
if(NOT PORT_FILES)
  list(APPEND GBMEM_SOURCES "${BANK_GUARD_SOURCE}")
endif()

add_library(gbmem STATIC ${GBMEM_SOURCES})
add_dependencies(gbmem gen_layout)
target_include_directories(gbmem PUBLIC "${CMAKE_SOURCE_DIR}/src" "${CMAKE_SOURCE_DIR}/include")
target_compile_options(gbmem PRIVATE -Wall -Wextra)

# Entry/exit instrumentation carries `farcall`'s bank switch for every target in
# the generated table (src/bank_guard.c), so it is on in every build. mem.c and
# ppu.c are excluded because instrumenting gb_read8/gb_write8 inflates the
# record count by two orders of magnitude without naming a single routine.
target_compile_options(gbmem PRIVATE
  -finstrument-functions
  -finstrument-functions-exclude-file-list=mem.c,ppu.c,runtime_events.c,trace.c,bank_guard.c,bank_guard_generated.c)

# Frame-tagged function-entry recording for the bilateral call-count diff
# against the reference stream, and the producer for the CFG audit's edges.
option(POKETCG_TRACE "record function entries in the ported routines" OFF)
if(POKETCG_TRACE)
  target_compile_definitions(gbmem PUBLIC POKETCG_TRACE=1)
  message(STATUS "function-entry recording: on")
endif()

# One adapter translation unit per pret source file, each exporting
# `const ProbeEntry probe_entries_<basename>[]`. Generating the group list from
# the glob keeps concurrent ports from contending over a shared registry file.
set(PROBE_GROUPS "// generated by CMake from the src/probe glob\n")
foreach(src ${PROBE_SOURCES})
  get_filename_component(group "${src}" NAME_WE)
  string(APPEND PROBE_GROUPS "PROBE_GROUP(${group})\n")
endforeach()
file(GENERATE OUTPUT "${CMAKE_BINARY_DIR}/probe_groups.h" CONTENT "${PROBE_GROUPS}")

add_executable(poketcg_probe src/probe.c src/probe_table.c ${PROBE_SOURCES})
target_include_directories(poketcg_probe PRIVATE "${CMAKE_BINARY_DIR}")
target_link_libraries(poketcg_probe PRIVATE gbmem)
target_compile_options(poketcg_probe PRIVATE -Wall -Wextra)
# A case may stop the run at a named routine's entry rather than at a return
# (src/trace.h trace_set_stop), so the probe resolves that name with dlsym and
# needs its own routine symbols in the dynamic table.
set_target_properties(poketcg_probe PROPERTIES ENABLE_EXPORTS ON)


include(CheckCSourceCompiles)
find_package(SDL2 QUIET)
if(NOT SDL2_FOUND)
	find_package(PkgConfig QUIET)
	if(PkgConfig_FOUND)
		pkg_check_modules(SDL2 QUIET sdl2)
	endif()
endif()

# SDL2 can be "found" (sdl2-config and the .so present) while its headers are
# unbuildable -- Debian's SDL_config.h indirects to a per-arch _real_SDL_config.h that
# a mismatched multiarch install omits. So probe by actually compiling AND linking
# against the discovered flags; presence alone is not evidence.
set(POKETCG_SDL_USABLE OFF)
if(SDL2_FOUND OR SDL2_LIBRARIES OR SDL2_LIBRARY)
	if(TARGET SDL2::SDL2)
		set(CMAKE_REQUIRED_LIBRARIES SDL2::SDL2)
	else()
		set(CMAKE_REQUIRED_INCLUDES ${SDL2_INCLUDE_DIRS} ${SDL2_INCLUDE_DIR})
		set(CMAKE_REQUIRED_LINK_OPTIONS ${SDL2_LDFLAGS_OTHER})
		set(CMAKE_REQUIRED_LIBRARIES ${SDL2_LIBRARIES} ${SDL2_LIBRARY})
	endif()
	check_c_source_compiles("#include <SDL2/SDL.h>\nint main(void) { return SDL_Init(SDL_INIT_VIDEO); }" POKETCG_SDL_USABLE_PROBE)
	unset(CMAKE_REQUIRED_INCLUDES)
	unset(CMAKE_REQUIRED_LINK_OPTIONS)
	unset(CMAKE_REQUIRED_LIBRARIES)
	if(POKETCG_SDL_USABLE_PROBE)
		set(POKETCG_SDL_USABLE ON)
	endif()
endif()
if(POKETCG_SDL_USABLE)
	message(STATUS "SDL2 backend: compiled in")
else()
	message(STATUS "SDL2 backend: compiled out (headers unavailable or unusable)")
endif()

set(POKETCG_SHELL_SOURCES src/main.c src/checkpoint.c src/digest.c src/persistence.c src/runtime.c src/shell.c src/state_dump.c)
add_executable(poketcg ${POKETCG_SHELL_SOURCES})
target_include_directories(poketcg PRIVATE "${CMAKE_SOURCE_DIR}/src")
target_link_libraries(poketcg PRIVATE Threads::Threads)
target_link_libraries(poketcg PRIVATE gbmem)
target_compile_options(poketcg PRIVATE -Wall -Wextra)
if(POKETCG_DATA_PACK)
	target_compile_definitions(poketcg PRIVATE POKETCG_DATA_PACK_PATH="${POKETCG_DATA_PACK}")
endif()
if(POKETCG_SDL_USABLE)
	target_compile_definitions(poketcg PRIVATE POKETCG_HAVE_SDL=1)
	if(TARGET SDL2::SDL2)
		target_link_libraries(poketcg PRIVATE SDL2::SDL2)
	else()
		target_include_directories(poketcg PRIVATE ${SDL2_INCLUDE_DIRS})
		target_link_directories(poketcg PRIVATE ${SDL2_LIBRARY_DIRS})
		target_link_libraries(poketcg PRIVATE ${SDL2_LIBRARIES})
	endif()
endif()