cmake_minimum_required(VERSION 3.20)
project(poketcg_pc C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "" FORCE)
endif()

set(POKETCG_DISASM "${CMAKE_SOURCE_DIR}/poketcg" CACHE PATH "default profile source checkout")
set(POKETCG_DATA_PACK "" CACHE FILEPATH "default profile sparse production data pack")
set(PORT_FILES "" CACHE STRING "semicolon-separated pret basenames to build; empty = all")
option(POKETCG_ENABLE_LAUNCHER "build the profile chooser" OFF)
option(POKETCG_DEBUG_MENU "enable the host playtest debug menu" OFF)
option(POKETCG_TRACE "record function entries in the ported routines" OFF)


find_package(Threads REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
execute_process(
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/profile_path.py" default
  WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
  OUTPUT_VARIABLE POKETCG_DEFAULT_PROFILE
  OUTPUT_STRIP_TRAILING_WHITESPACE
  COMMAND_ERROR_IS_FATAL ANY)
execute_process(
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/profile_path.py" profiles
  WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
  OUTPUT_VARIABLE POKETCG_PROFILE_NAMES
  OUTPUT_STRIP_TRAILING_WHITESPACE
  COMMAND_ERROR_IS_FATAL ANY)
foreach(profile IN LISTS POKETCG_PROFILE_NAMES)
  if(NOT profile STREQUAL POKETCG_DEFAULT_PROFILE)
    string(TOUPPER "${profile}" profile_upper)
    set(enable_var "POKETCG_ENABLE_${profile_upper}")
    option(${enable_var} "build the ${profile} profile targets" OFF)
  endif()
endforeach()
execute_process(
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/profile_path.py" sym --profile "${POKETCG_DEFAULT_PROFILE}"
  WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
  OUTPUT_VARIABLE POKETCG_CATALOG_DEFAULT_SYM
  OUTPUT_STRIP_TRAILING_WHITESPACE
  COMMAND_ERROR_IS_FATAL ANY)
get_filename_component(POKETCG_DEFAULT_SYM_NAME "${POKETCG_CATALOG_DEFAULT_SYM}" NAME)
set(POKETCG_DEFAULT_SYM "${POKETCG_DISASM}/${POKETCG_DEFAULT_SYM_NAME}")

file(GLOB SHARED_HOME_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/home/*.c")
file(GLOB SHARED_PROBE_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/probe/*.c")
file(GLOB SHARED_HOME_HEADERS CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/home/*.h")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS
  "${CMAKE_SOURCE_DIR}/profiles/profiles.json" "${CMAKE_SOURCE_DIR}/tools/profile_path.py"
  "${CMAKE_SOURCE_DIR}/tools/compose_profile.py")

function(profile_sources profile out_dir home_out probe_out headers_out profile_root_out compose_out)
  execute_process(
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/profile_path.py" --profile "${profile}" overlay-root
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    OUTPUT_VARIABLE overlay_root
    OUTPUT_STRIP_TRAILING_WHITESPACE
    COMMAND_ERROR_IS_FATAL ANY)
  set(profile_root "")
  if(overlay_root)
    set(profile_root "${CMAKE_SOURCE_DIR}/${overlay_root}")
    file(GLOB override_files CONFIGURE_DEPENDS
      "${profile_root}/home/*.c" "${profile_root}/home/*.h" "${profile_root}/probe/*.c")
  endif()
  execute_process(
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/compose_profile.py" sources --profile "${profile}" --out "${out_dir}"
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    OUTPUT_VARIABLE listing
    COMMAND_ERROR_IS_FATAL ANY)
  string(REPLACE "\n" ";" rows "${listing}")
  set(home "")
  set(probe "")
  set(headers "")
  set(composed "")
  foreach(row ${rows})
    if(row MATCHES "^unit=([^|]+)\\|([^|]+)\\|([^|]+)\\|([01])$")
      set(output "${CMAKE_MATCH_1}")
      set(shared "${CMAKE_MATCH_2}")
      set(override "${CMAKE_MATCH_3}")
      set(probe_unit "${CMAKE_MATCH_4}")
      set(arguments unit --override "${override}" --out "${output}" --line-marks)
      set(inputs "${override}")
      if(NOT shared STREQUAL "-")
        list(APPEND arguments --shared "${shared}")
        list(APPEND inputs "${shared}")
      endif()
      if(probe_unit STREQUAL "1")
        list(APPEND arguments --probe)
      endif()
      add_custom_command(
        OUTPUT "${output}"
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/compose_profile.py" ${arguments}
        DEPENDS "${CMAKE_SOURCE_DIR}/tools/compose_profile.py" "${CMAKE_SOURCE_DIR}/tools/factory_blocks.py" ${inputs}
        VERBATIM)
      list(APPEND composed "${output}")
    elseif(row MATCHES "^home=(.+)$")
      list(APPEND home "${CMAKE_MATCH_1}")
    elseif(row MATCHES "^probe=(.+)$")
      list(APPEND probe "${CMAKE_MATCH_1}")
    elseif(row MATCHES "^header=(.+)$")
      list(APPEND headers "${CMAKE_MATCH_1}")
    endif()
  endforeach()
  set(${home_out} ${home} PARENT_SCOPE)
  set(${probe_out} ${probe} PARENT_SCOPE)
  set(${headers_out} ${headers} PARENT_SCOPE)
  set(${profile_root_out} "${profile_root}" PARENT_SCOPE)
  set(${compose_out} ${composed} PARENT_SCOPE)
endfunction()

function(profile_catalog_path profile kind output)
  execute_process(
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/profile_path.py" "${kind}" --profile "${profile}"
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    OUTPUT_VARIABLE value
    OUTPUT_STRIP_TRAILING_WHITESPACE
    COMMAND_ERROR_IS_FATAL ANY)
  set(${output} "${value}" PARENT_SCOPE)
endfunction()

function(add_poketcg_profile profile)
  set(options)
  set(one_value_args DISASM ROM MAP SYM BINARY PROBE DATA_PACK INVENTORY)
  cmake_parse_arguments(PROFILE "" "${one_value_args}" "" ${ARGN})
  if(NOT EXISTS "${PROFILE_SYM}")
    message(FATAL_ERROR "missing ${PROFILE_SYM}; run the profile bootstrap")
  endif()

  set(profile_build_root "${CMAKE_BINARY_DIR}/generated/${profile}")
  profile_sources(${profile} "${profile_build_root}" HOME_SOURCES PROBE_SOURCES HOME_HEADERS PROFILE_ROOT COMPOSED_SOURCES)
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

  set(compose_target "compose_${profile}")
  add_custom_target(${compose_target} DEPENDS ${COMPOSED_SOURCES})
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
            --profile "${profile}" --disasm "${PROFILE_DISASM}" --out "${profile_generated}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_constants.py" ${profile_constant_sources}
            "${PROFILE_DISASM}/src/text/text_offsets.asm" "${CMAKE_SOURCE_DIR}/profiles/profiles.json"
    COMMENT "gen_constants: ${profile}"
    VERBATIM)
  set(profile_header "${profile_generated}/profile_features.h")
  add_custom_command(
    OUTPUT "${profile_header}"
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_profile_header.py"
            --profile "${profile}" --out "${profile_generated}"
    DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_profile_header.py" "${CMAKE_SOURCE_DIR}/profiles/profiles.json"
    COMMENT "gen_profile_header: ${profile}"
    VERBATIM)
  set(layout_target "gen_layout_${profile}")
  add_custom_target(${layout_target} DEPENDS ${generated_headers} ${constant_headers} "${profile_header}")
  if(profile STREQUAL POKETCG_DEFAULT_PROFILE)
    add_custom_target(gen_layout DEPENDS ${layout_target})
  endif()

  set(save_import_sources "")
  if(PROFILE_ROOT AND EXISTS "${PROFILE_ROOT}/host/save_import.c")
    set(save_import_header "${profile_generated}/save_import_layout.h")
    file(GLOB save_import_inputs CONFIGURE_DEPENDS
      "${POKETCG_DISASM}/src/constants/*.asm" "${POKETCG_DISASM}/src/text/*.asm"
      "${PROFILE_DISASM}/src/constants/*.asm" "${PROFILE_DISASM}/src/text/*.asm")
    add_custom_command(
      OUTPUT "${save_import_header}"
      COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/tools/gen_save_import.py"
              --vanilla-sym "${POKETCG_DEFAULT_SYM}" --extended-sym "${PROFILE_SYM}"
              --vanilla-disasm "${POKETCG_DISASM}" --extended-disasm "${PROFILE_DISASM}"
              --out "${save_import_header}"
      DEPENDS "${CMAKE_SOURCE_DIR}/tools/gen_save_import.py" "${CMAKE_SOURCE_DIR}/tools/gen_constants.py"
              "${POKETCG_DEFAULT_SYM}" "${PROFILE_SYM}" ${save_import_inputs}
      COMMENT "gen_save_import: ${profile}"
      VERBATIM)
    set(save_import_sources "${PROFILE_ROOT}/host/save_import.c" "${save_import_header}")
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
  set(script_entry_overlay "")
  if(PROFILE_ROOT)
    set(script_entry_overlay --overlay "${profile_build_root}/home")
  endif()
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
            ${script_entry_overlay}
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

  if(profile STREQUAL POKETCG_DEFAULT_PROFILE)
    set(gbmem_target "gbmem")
  else()
    set(gbmem_target "gbmem_${profile}")
  endif()
  set(probe_target "${PROFILE_PROBE}")
  set(shell_target "${PROFILE_BINARY}")

  set(gbmem_sources src/mem.c src/ppu.c src/apu.c src/printer_sink.c src/runtime_events.c src/trace.c
                    src/bank_guard.c src/link.c src/isr.c src/serial_track.c src/widescreen.c ${HOME_SOURCES})
  foreach(host_source IN ITEMS link serial_track)
    if(PROFILE_ROOT AND EXISTS "${PROFILE_ROOT}/host/${host_source}.c")
      list(REMOVE_ITEM gbmem_sources "src/${host_source}.c")
      list(APPEND gbmem_sources "${PROFILE_ROOT}/host/${host_source}.c")
    endif()
  endforeach()
  if(POKETCG_DEBUG_MENU)
    list(APPEND gbmem_sources src/debug_cheats.c)
  endif()
  if(NOT PORT_FILES)
    list(APPEND gbmem_sources "${bank_guard_source}")
  endif()
  if(profile STREQUAL POKETCG_DEFAULT_PROFILE)
    add_library(${gbmem_target} STATIC ${gbmem_sources})
  else()
    add_library(${gbmem_target} STATIC EXCLUDE_FROM_ALL ${gbmem_sources})
  endif()
  add_dependencies(${gbmem_target} ${layout_target} ${compose_target})
  target_include_directories(${gbmem_target} PUBLIC
    "${profile_build_root}"
    "${CMAKE_SOURCE_DIR}/src"
    "${CMAKE_SOURCE_DIR}/include")
  target_compile_options(${gbmem_target} PRIVATE -Wall -Wextra)
  if(POKETCG_DEBUG_MENU)
    target_compile_definitions(${gbmem_target} PUBLIC POKETCG_DEBUG_MENU=1)
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
  if(profile STREQUAL POKETCG_DEFAULT_PROFILE)
    add_executable(${probe_target} src/probe.c src/probe_table.c ${PROBE_SOURCES})
  else()
    add_executable(${probe_target} EXCLUDE_FROM_ALL src/probe.c src/probe_table.c ${PROBE_SOURCES})
  endif()
  target_include_directories(${probe_target} PRIVATE "${probe_root}" "${profile_build_root}" "${CMAKE_SOURCE_DIR}/src")
  add_dependencies(${probe_target} ${compose_target})
  target_link_libraries(${probe_target} PRIVATE ${gbmem_target})
  target_compile_options(${probe_target} PRIVATE -Wall -Wextra)
  set_target_properties(${probe_target} PROPERTIES ENABLE_EXPORTS ON)

  set(shell_sources src/main.c src/checkpoint.c src/digest.c src/persistence.c src/profile.c src/pc_options.c src/presentation.c src/runtime.c src/shell.c src/state_dump.c ${save_import_sources})
  if(profile STREQUAL POKETCG_DEFAULT_PROFILE)
    add_executable(${shell_target} ${shell_sources})
  else()
    add_executable(${shell_target} EXCLUDE_FROM_ALL ${shell_sources})
  endif()
  if(PROFILE_ROOT AND EXISTS "${PROFILE_ROOT}/host/save_import.c")
    target_compile_definitions(${shell_target} PRIVATE POKETCG_SAVE_IMPORT=1)
  endif()
  set_target_properties(${shell_target} PROPERTIES ENABLE_EXPORTS ON)
  target_include_directories(${shell_target} PRIVATE "${profile_build_root}" "${CMAKE_SOURCE_DIR}/src")
  if(PROFILE_ROOT)
    target_include_directories(${shell_target} PRIVATE "${PROFILE_ROOT}/host")
  endif()
  add_dependencies(${shell_target} ${compose_target})
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

foreach(profile IN LISTS POKETCG_PROFILE_NAMES)
  string(TOUPPER "${profile}" profile_upper)
  if(NOT profile STREQUAL POKETCG_DEFAULT_PROFILE)
    set(enable_var "POKETCG_ENABLE_${profile_upper}")
    if(NOT ${enable_var})
      continue()
    endif()
  endif()
  profile_catalog_path("${profile}" source profile_source)
  profile_catalog_path("${profile}" rom profile_rom_catalog)
  profile_catalog_path("${profile}" map profile_map_catalog)
  profile_catalog_path("${profile}" sym profile_sym_catalog)
  profile_catalog_path("${profile}" binary profile_binary_catalog)
  profile_catalog_path("${profile}" probe profile_probe_catalog)
  profile_catalog_path("${profile}" pack profile_pack_catalog)
  profile_catalog_path("${profile}" inventory profile_inventory_catalog)
  if(profile STREQUAL POKETCG_DEFAULT_PROFILE)
    set(profile_disasm_default "${POKETCG_DISASM}")
  else()
    set(profile_disasm_default "${profile_source}")
  endif()
  set(disasm_var "POKETCG_PROFILE_${profile_upper}_DISASM")
  set(${disasm_var} "${profile_disasm_default}" CACHE PATH "source checkout for ${profile}")
  set(profile_disasm "${${disasm_var}}")
  get_filename_component(profile_rom_name "${profile_rom_catalog}" NAME)
  get_filename_component(profile_map_name "${profile_map_catalog}" NAME)
  get_filename_component(profile_sym_name "${profile_sym_catalog}" NAME)
  set(profile_rom "${profile_disasm}/${profile_rom_name}")
  set(profile_map "${profile_disasm}/${profile_map_name}")
  set(profile_sym "${profile_disasm}/${profile_sym_name}")
  get_filename_component(profile_binary "${profile_binary_catalog}" NAME)
  get_filename_component(profile_probe "${profile_probe_catalog}" NAME)
  set(profile_pack_default "")
  if(profile STREQUAL POKETCG_DEFAULT_PROFILE AND POKETCG_DATA_PACK)
    set(profile_pack_default "${POKETCG_DATA_PACK}")
  elseif(EXISTS "${profile_pack_catalog}")
    set(profile_pack_default "${profile_pack_catalog}")
  endif()
  set(pack_var "POKETCG_PROFILE_${profile_upper}_DATA_PACK")
  set(${pack_var} "${profile_pack_default}" CACHE FILEPATH "data pack for ${profile}")
  set(inventory_var "POKETCG_PROFILE_${profile_upper}_INVENTORY")
  set(${inventory_var} "${profile_inventory_catalog}" CACHE FILEPATH "inventory for ${profile}")
  add_poketcg_profile("${profile}"
    DISASM "${profile_disasm}"
    ROM "${profile_rom}"
    MAP "${profile_map}"
    SYM "${profile_sym}"
    BINARY "${profile_binary}"
    PROBE "${profile_probe}"
    DATA_PACK "${${pack_var}}"
    INVENTORY "${${inventory_var}}")
endforeach()

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
