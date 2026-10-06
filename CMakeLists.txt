cmake_minimum_required(VERSION 3.20)
project(poketcg_pc C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "" FORCE)
endif()

set(POKETCG_DISASM "${CMAKE_SOURCE_DIR}/poketcg" CACHE PATH "pret/poketcg checkout")
set(POKETCG_EXTENDED_DISASM "${CMAKE_SOURCE_DIR}/poketcg-extended" CACHE PATH "Extended source checkout")
set(POKETCG_DATA_PACK "" CACHE FILEPATH "vanilla sparse production data pack")
set(POKETCG_DATA_PACK_EXTENDED "" CACHE FILEPATH "Extended sparse production data pack")
set(PORT_FILES "" CACHE STRING "semicolon-separated pret basenames to build; empty = all")
option(POKETCG_ENABLE_EXTENDED "build the Extended profile targets" OFF)
option(POKETCG_ENABLE_LAUNCHER "build the profile chooser" OFF)
option(POKETCG_DEBUG_MENU "enable the host playtest debug menu" OFF)
option(POKETCG_TRACE "record function entries in the ported routines" OFF)

find_package(Threads REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

file(GLOB SHARED_HOME_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/home/*.c")
file(GLOB SHARED_PROBE_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/probe/*.c")
file(GLOB SHARED_HOME_HEADERS CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/home/*.h")

execute_process(
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/profile_path.py" --profile extended removed-basenames
  WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
  OUTPUT_VARIABLE EXTENDED_REMOVED_BASENAMES
  OUTPUT_STRIP_TRAILING_WHITESPACE
  COMMAND_ERROR_IS_FATAL ANY)
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/profiles/profiles.json")

function(profile_sources profile home_out probe_out headers_out profile_root_out)
  set(home ${SHARED_HOME_SOURCES})
  set(probe ${SHARED_PROBE_SOURCES})
  set(headers ${SHARED_HOME_HEADERS})
  set(profile_root "")
  if(profile STREQUAL "extended")
    set(profile_root "${CMAKE_SOURCE_DIR}/src/profiles/extended")
    list(JOIN EXTENDED_REMOVED_BASENAMES "|" removed_pattern)
    list(FILTER home EXCLUDE REGEX "/(${removed_pattern})\\.c$")
    list(FILTER probe EXCLUDE REGEX "/(${removed_pattern})\\.c$")
    list(FILTER headers EXCLUDE REGEX "/(${removed_pattern})\\.h$")
    file(GLOB overlay_home CONFIGURE_DEPENDS "${profile_root}/home/*.c")
    file(GLOB overlay_probe CONFIGURE_DEPENDS "${profile_root}/probe/*.c")
    file(GLOB overlay_headers CONFIGURE_DEPENDS "${profile_root}/home/*.h")
    foreach(overlay ${overlay_home})
      get_filename_component(name "${overlay}" NAME_WE)
      foreach(shared ${home})
        get_filename_component(shared_name "${shared}" NAME_WE)
        if(shared_name STREQUAL name)
          list(REMOVE_ITEM home "${shared}")
        endif()
      endforeach()
      list(APPEND home "${overlay}")
    endforeach()
    foreach(overlay ${overlay_probe})
      get_filename_component(name "${overlay}" NAME_WE)
      foreach(shared ${probe})
        get_filename_component(shared_name "${shared}" NAME_WE)
        if(shared_name STREQUAL name)
          list(REMOVE_ITEM probe "${shared}")
        endif()
      endforeach()
      list(APPEND probe "${overlay}")
    endforeach()
    foreach(overlay ${overlay_headers})
      get_filename_component(name "${overlay}" NAME_WE)
      foreach(shared ${headers})
        get_filename_component(shared_name "${shared}" NAME_WE)
        if(shared_name STREQUAL name)
          list(REMOVE_ITEM headers "${shared}")
        endif()
      endforeach()
      list(APPEND headers "${overlay}")
    endforeach()
  endif()
  set(${home_out} ${home} PARENT_SCOPE)
  set(${probe_out} ${probe} PARENT_SCOPE)
  set(${headers_out} ${headers} PARENT_SCOPE)
  set(${profile_root_out} "${profile_root}" PARENT_SCOPE)
endfunction()

function(add_poketcg_profile profile)
  set(options)
  set(one_value_args DISASM ROM MAP SYM BINARY PROBE DATA_PACK INVENTORY)
  cmake_parse_arguments(PROFILE "" "${one_value_args}" "" ${ARGN})
  if(NOT EXISTS "${PROFILE_SYM}")
    message(FATAL_ERROR "missing ${PROFILE_SYM}; run the profile bootstrap")
  endif()

  profile_sources(${profile} HOME_SOURCES PROBE_SOURCES HOME_HEADERS PROFILE_ROOT)
  set(effect_probe "${CMAKE_SOURCE_DIR}/src/probe/effect_functions.c")
  set(script_probe "${CMAKE_SOURCE_DIR}/src/probe/scripting.c")
  foreach(source ${PROBE_SOURCES})
    get_filename_component(name "${source}" NAME_WE)
    if(name STREQUAL "effect_functions")
      set(effect_probe "${source}")
    elseif(name STREQUAL "scripting")
      set(script_probe "${source}")
    endif()
  endforeach()

  set(profile_build_root "${CMAKE_BINARY_DIR}/generated/${profile}")
  set(profile_generated "${profile_build_root}/generated")
  set(generated_headers
    "${profile_generated}/wram.h"
    "${profile_generated}/hram.h"
    "${profile_generated}/sram.h"
    "${profile_generated}/rom.h"
  )

  add_custom_command(
    OUTPUT ${generated_headers}
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_layout.py"
            --sym "${PROFILE_SYM}" --out "${profile_generated}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_layout.py" "${PROFILE_SYM}"
    COMMENT "gen_layout: ${profile}"
    VERBATIM)
  set(constant_headers
    "${profile_generated}/constants.h"
    "${profile_generated}/text_ids.h"
  )
  file(GLOB profile_constant_sources CONFIGURE_DEPENDS "${PROFILE_DISASM}/src/constants/*.asm")
  add_custom_command(
    OUTPUT ${constant_headers}
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_constants.py"
            --profile "${profile}" --out "${profile_generated}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_constants.py" ${profile_constant_sources}
            "${PROFILE_DISASM}/src/text/text_offsets.asm" "${CMAKE_SOURCE_DIR}/profiles/profiles.json"
    COMMENT "gen_constants: ${profile}"
    VERBATIM)
  set(layout_target "gen_layout_${profile}")
  add_custom_target(${layout_target} DEPENDS ${generated_headers} ${constant_headers})
  if(profile STREQUAL "vanilla")
    add_custom_target(gen_layout DEPENDS ${layout_target})
  endif()

  set(effect_dispatch_source "${profile_build_root}/effect_dispatch_generated.c")
  add_custom_command(
    OUTPUT "${effect_dispatch_source}"
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_effect_dispatch.py"
            --probe "${effect_probe}"
            --inventory "${PROFILE_INVENTORY}"
            --output "${effect_dispatch_source}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_effect_dispatch.py"
            "${effect_probe}"
            "${PROFILE_INVENTORY}"
    COMMENT "gen_effect_dispatch: ${profile}"
    VERBATIM)

  set(script_dispatch_source "${profile_build_root}/script_dispatch_generated.c")
  set(script_table "${PROFILE_DISASM}/src/data/script_table.asm")
  add_custom_command(
    OUTPUT "${script_dispatch_source}"
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_script_dispatch.py"
            --probe "${script_probe}"
            --table "${script_table}"
            --output "${script_dispatch_source}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_script_dispatch.py"
            "${script_probe}"
            "${script_table}"
    COMMENT "gen_script_dispatch: ${profile}"
    VERBATIM)

  file(GLOB SCRIPT_SOURCES CONFIGURE_DEPENDS "${PROFILE_DISASM}/src/scripts/*.asm")
  list(APPEND SCRIPT_SOURCES "${PROFILE_DISASM}/src/engine/overworld/scripting.asm")
  set(script_entry_source "${profile_build_root}/script_entry_dispatch_generated.c")
  add_custom_command(
    OUTPUT "${script_entry_source}"
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_script_entry_dispatch.py"
            --sym "${PROFILE_SYM}"
            --rom "${PROFILE_ROM}"
            --home "${CMAKE_SOURCE_DIR}/src/home"
            --map-scripts "${PROFILE_DISASM}/src/data/map_scripts.asm"
            --npc-map-data "${PROFILE_DISASM}/src/data/npc_map_data.asm"
            --map-objects "${PROFILE_DISASM}/src/data/map_objects.asm"
            --scripts ${SCRIPT_SOURCES}
            --output "${script_entry_source}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_script_entry_dispatch.py"
            "${PROFILE_SYM}"
            "${PROFILE_ROM}"
            "${PROFILE_DISASM}/src/data/map_scripts.asm"
            "${PROFILE_DISASM}/src/data/npc_map_data.asm"
            "${PROFILE_DISASM}/src/data/map_objects.asm"
            ${SCRIPT_SOURCES}
            ${HOME_HEADERS}
    COMMENT "gen_script_entry_dispatch: ${profile}"
    VERBATIM)

  set(bank_guard_source "${profile_build_root}/bank_guard_generated.c")
  add_custom_command(
    OUTPUT "${bank_guard_source}"
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_bank_guard.py"
            --sym "${PROFILE_SYM}"
            --asm-root "${PROFILE_DISASM}/src"
            --home "${CMAKE_SOURCE_DIR}/src/home"
            --output "${bank_guard_source}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_bank_guard.py"
            "${PROFILE_SYM}"
            ${HOME_HEADERS}
    COMMENT "gen_bank_guard: ${profile}"
    VERBATIM)

  if(NOT PORT_FILES)
    list(APPEND HOME_SOURCES "${script_entry_source}" "${script_dispatch_source}" "${effect_dispatch_source}")
  endif()

  if(PORT_FILES)
    set(keep ${PORT_FILES} switch_rom switch_sram)
    set(filtered_home "")
    foreach(source ${HOME_SOURCES})
      get_filename_component(name "${source}" NAME_WE)
      if(name IN_LIST keep)
        list(APPEND filtered_home "${source}")
      endif()
    endforeach()
    set(filtered_probe "")
    foreach(source ${PROBE_SOURCES})
      get_filename_component(name "${source}" NAME_WE)
      if(name IN_LIST keep)
        list(APPEND filtered_probe "${source}")
      endif()
    endforeach()
    set(HOME_SOURCES ${filtered_home})
    set(PROBE_SOURCES ${filtered_probe})
  endif()

  set(gbmem_target "gbmem")
  set(probe_target "poketcg_probe")
  set(shell_target "poketcg")
  if(profile STREQUAL "extended")
    set(gbmem_target "gbmem_extended")
    set(probe_target "poketcg_extended_probe")
    set(shell_target "poketcg-extended")
  endif()

  set(gbmem_sources src/mem.c src/ppu.c src/apu.c src/printer_sink.c src/runtime_events.c src/trace.c
                    src/bank_guard.c src/link.c src/isr.c src/serial_track.c src/widescreen.c ${HOME_SOURCES})
  if(profile STREQUAL "extended")
    list(REMOVE_ITEM gbmem_sources src/link.c src/serial_track.c)
    list(APPEND gbmem_sources "${PROFILE_ROOT}/link.c" "${PROFILE_ROOT}/serial_track.c")
  endif()
  if(POKETCG_DEBUG_MENU)
    list(APPEND gbmem_sources src/debug_cheats.c)
  endif()
  if(NOT PORT_FILES)
    list(APPEND gbmem_sources "${bank_guard_source}")
  endif()
  if(profile STREQUAL "extended")
    add_library(${gbmem_target} STATIC EXCLUDE_FROM_ALL ${gbmem_sources})
  else()
    add_library(${gbmem_target} STATIC ${gbmem_sources})
  endif()
  add_dependencies(${gbmem_target} ${layout_target})
  target_include_directories(${gbmem_target} PUBLIC
    "${profile_build_root}"
    "${PROFILE_ROOT}"
    "${CMAKE_SOURCE_DIR}/src"
    "${CMAKE_SOURCE_DIR}/include")
  target_compile_options(${gbmem_target} PRIVATE -Wall -Wextra)
  if(POKETCG_DEBUG_MENU)
    target_compile_definitions(${gbmem_target} PUBLIC POKETCG_DEBUG_MENU=1)
  endif()
  if(profile STREQUAL "extended")
    target_compile_definitions(${gbmem_target} PUBLIC POKETCG_PROFILE_EXTENDED=1)
  endif()
  target_compile_options(${gbmem_target} PRIVATE
    -finstrument-functions
    -finstrument-functions-exclude-file-list=mem.c,ppu.c,apu.c,printer_sink.c,runtime_events.c,trace.c,bank_guard.c,bank_guard_generated.c,link.c,isr.c,serial_track.c,widescreen.c)
  if(POKETCG_TRACE)
    target_compile_definitions(${gbmem_target} PUBLIC POKETCG_TRACE=1)
  endif()

  set(probe_groups "// generated by CMake from the ${profile} probe glob\n")
  foreach(source ${PROBE_SOURCES})
    get_filename_component(group "${source}" NAME_WE)
    string(APPEND probe_groups "PROBE_GROUP(${group})\n")
  endforeach()
  set(probe_root "${profile_build_root}/probe")
  file(GENERATE OUTPUT "${probe_root}/probe_groups.h" CONTENT "${probe_groups}")
  if(profile STREQUAL "extended")
    add_executable(${probe_target} EXCLUDE_FROM_ALL src/probe.c src/probe_table.c ${PROBE_SOURCES})
  else()
    add_executable(${probe_target} src/probe.c src/probe_table.c ${PROBE_SOURCES})
  endif()
  target_include_directories(${probe_target} PRIVATE "${probe_root}" "${profile_build_root}" "${PROFILE_ROOT}" "${CMAKE_SOURCE_DIR}/src")
  target_link_libraries(${probe_target} PRIVATE ${gbmem_target})
  target_compile_options(${probe_target} PRIVATE -Wall -Wextra)
  set_target_properties(${probe_target} PROPERTIES ENABLE_EXPORTS ON)

  set(shell_sources src/main.c src/checkpoint.c src/digest.c src/persistence.c src/profile.c src/pc_options.c src/presentation.c src/runtime.c src/shell.c src/state_dump.c)
  if(profile STREQUAL "extended")
    add_executable(${shell_target} EXCLUDE_FROM_ALL ${shell_sources})
  else()
    add_executable(${shell_target} ${shell_sources})
  endif()
  if(profile STREQUAL "extended")
    target_compile_definitions(${shell_target} PRIVATE POKETCG_PROFILE_EXTENDED=1)
  endif()
  set_target_properties(${shell_target} PROPERTIES ENABLE_EXPORTS ON)
  target_include_directories(${shell_target} PRIVATE "${profile_build_root}" "${PROFILE_ROOT}" "${CMAKE_SOURCE_DIR}/src")
  target_link_libraries(${shell_target} PRIVATE Threads::Threads ${gbmem_target})
  target_compile_options(${shell_target} PRIVATE -Wall -Wextra)
  if(PROFILE_DATA_PACK)
    target_compile_definitions(${shell_target} PRIVATE POKETCG_DATA_PACK_PATH="${PROFILE_DATA_PACK}")
  endif()
  if(POKETCG_SDL_USABLE)
    target_compile_definitions(${shell_target} PRIVATE POKETCG_HAVE_SDL=1)
    if(TARGET SDL2::SDL2)
      target_link_libraries(${shell_target} PRIVATE SDL2::SDL2)
    else()
      target_include_directories(${shell_target} PRIVATE ${SDL2_INCLUDE_DIRS})
      target_link_directories(${shell_target} PRIVATE ${SDL2_LIBRARY_DIRS})
      target_link_libraries(${shell_target} PRIVATE ${SDL2_LIBRARIES})
    endif()
  endif()
  if(POKETCG_SDL_USABLE AND POKETCG_PULSE_USABLE)
    target_compile_definitions(${shell_target} PRIVATE POKETCG_HAVE_PULSE=1)
    target_include_directories(${shell_target} PRIVATE "${POKETCG_PULSE_INCLUDE_DIR}")
    target_link_libraries(${shell_target} PRIVATE "${POKETCG_PULSE_SIMPLE_LIBRARY}" "${POKETCG_PULSE_LIBRARY}")
  endif()
  if(POKETCG_DEBUG_MENU)
    target_compile_definitions(${shell_target} PRIVATE POKETCG_DEBUG_MENU=1)
  endif()
endfunction()

include(CheckCSourceCompiles)
find_package(SDL2 QUIET)
if(NOT SDL2_FOUND)
  find_package(PkgConfig QUIET)
  if(PkgConfig_FOUND)
    pkg_check_modules(SDL2 QUIET sdl2)
  endif()
endif()
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
find_path(POKETCG_PULSE_INCLUDE_DIR pulse/simple.h)
find_library(POKETCG_PULSE_SIMPLE_LIBRARY NAMES pulse-simple libpulse-simple.so.0)
find_library(POKETCG_PULSE_LIBRARY NAMES pulse libpulse.so.0)
set(POKETCG_PULSE_USABLE OFF)
if(POKETCG_PULSE_INCLUDE_DIR AND POKETCG_PULSE_SIMPLE_LIBRARY AND POKETCG_PULSE_LIBRARY)
  set(POKETCG_PULSE_USABLE ON)
endif()

add_poketcg_profile(vanilla
  DISASM "${POKETCG_DISASM}"
  ROM "${POKETCG_DISASM}/poketcg.gbc"
  MAP "${POKETCG_DISASM}/poketcg.map"
  SYM "${POKETCG_DISASM}/poketcg.sym"
  BINARY poketcg
  PROBE poketcg_probe
  DATA_PACK "${POKETCG_DATA_PACK}"
  INVENTORY "${CMAKE_SOURCE_DIR}/site/data/inventory.json")

if(POKETCG_ENABLE_EXTENDED)
  add_poketcg_profile(extended
    DISASM "${POKETCG_EXTENDED_DISASM}"
    ROM "${POKETCG_EXTENDED_DISASM}/poketcg_ext.gbc"
    MAP "${POKETCG_EXTENDED_DISASM}/poketcg_ext.map"
    SYM "${POKETCG_EXTENDED_DISASM}/poketcg_ext.sym"
    BINARY poketcg-extended
    PROBE poketcg_extended_probe
    DATA_PACK "${POKETCG_DATA_PACK_EXTENDED}"
    INVENTORY "${CMAKE_SOURCE_DIR}/site/data/extended/inventory.json")
endif()

if(POKETCG_ENABLE_LAUNCHER)
  if(NOT POKETCG_SDL_USABLE)
    message(FATAL_ERROR "profile chooser requires SDL2")
  endif()
  add_executable(poketcg-launcher EXCLUDE_FROM_ALL src/launcher.c)
  target_compile_definitions(poketcg-launcher PRIVATE POKETCG_HAVE_SDL=1)
  target_compile_options(poketcg-launcher PRIVATE -Wall -Wextra)
  if(TARGET SDL2::SDL2)
    target_link_libraries(poketcg-launcher PRIVATE SDL2::SDL2)
  else()
    target_include_directories(poketcg-launcher PRIVATE ${SDL2_INCLUDE_DIRS})
    target_link_directories(poketcg-launcher PRIVATE ${SDL2_LIBRARY_DIRS})
    target_link_libraries(poketcg-launcher PRIVATE ${SDL2_LIBRARIES})
  endif()
endif()
