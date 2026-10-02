# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target chapt4_interfaces::chapt4_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${chapt4_interfaces_TARGETS}.
if(chapt4_interfaces_TARGETS AND NOT TARGET chapt4_interfaces::chapt4_interfaces)
  add_library(chapt4_interfaces::chapt4_interfaces INTERFACE IMPORTED)
  set_target_properties(chapt4_interfaces::chapt4_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${chapt4_interfaces_TARGETS}")
endif()
