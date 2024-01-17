#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "raspimouse::raspimouse_component" for configuration ""
set_property(TARGET raspimouse::raspimouse_component APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(raspimouse::raspimouse_component PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libraspimouse_component.so"
  IMPORTED_SONAME_NOCONFIG "libraspimouse_component.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS raspimouse::raspimouse_component )
list(APPEND _IMPORT_CHECK_FILES_FOR_raspimouse::raspimouse_component "${_IMPORT_PREFIX}/lib/libraspimouse_component.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
