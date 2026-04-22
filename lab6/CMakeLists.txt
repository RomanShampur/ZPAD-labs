cmake_minimum_required(VERSION 3.10)
project(OpenCV_Lab3)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
include_directories(include ${OpenCV_INCLUDE_DIRS})

add_executable(lab3 
    src/main.cpp 
    src/CameraProvider.cpp 
    src/FrameProcessor.cpp
)
target_link_libraries(lab3 ${OpenCV_LIBS})
