idf_component_register(SRCS "app_main.cpp" INCLUDE_DIRS "."
    PRIV_REQUIRES espressif__esp_matter nvs_flash)
configure_file("${CMAKE_CURRENT_LIST_DIR}/build_identity.hpp.in"
    "${CMAKE_CURRENT_BINARY_DIR}/build_identity.hpp" @ONLY)
target_include_directories(${COMPONENT_LIB} PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")
target_link_options(${COMPONENT_LIB} INTERFACE "LINKER:--undefined=motley_build_identity")

target_compile_options(${COMPONENT_LIB} PRIVATE
    -std=c++23 -fno-exceptions -fno-rtti -Wall -Wextra -Werror
)
