project(thrift-generate-cpp)

#Make sure gen-cpp files can be included
include_directories("${CMAKE_CURRENT_BINARY_DIR}")
include_directories("${CMAKE_CURRENT_BINARY_DIR}/gen-cpp")

add_custom_command(
    OUTPUT 
        gen-cpp/Calculator.cpp
        gen-cpp/Calculator.h
        gen-cpp/calculator_constants.cpp
        gen-cpp/calculator_constants.h
        gen-cpp/calculator_types.cpp
        gen-cpp/calculator_types.h
    COMMAND thrift --gen cpp "${CMAKE_CURRENT_LIST_DIR}/calculator.thrift"
    COMMENT "Generating cpp files"
)

set(gencpp_SOURCES
    gen-cpp/Calculator.cpp
    gen-cpp/calculator_constants.cpp
    gen-cpp/calculator_types.cpp
)

message("${CONAN_LIBS}")

add_library(${PROJECT_NAME} STATIC ${gencpp_SOURCES})
target_link_libraries(${PROJECT_NAME} PUBLIC ${CONAN_LIBS})
target_include_directories(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/gen-cpp>")

set_target_properties( ${PROJECT_NAME} PROPERTIES CXX_STANDARD 11 )