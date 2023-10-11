cmake_minimum_required(VERSION 3.10)

project(TunNetGen)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories("src/")

file(
  GLOB_RECURSE
  source_files
  src/*.[chi]pp
)

set(CMAKE_BUILD_TYPE Debug)

add_definitions(-O2 -Wall -Wextra)
add_executable(tunNetGen ${source_files})
target_link_libraries(tunNetGen)
