#include "build_identity.hpp"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#if defined(__cpp_exceptions) || defined(__GXX_RTTI)
#error "Owned firmware code requires exceptions and RTTI disabled"
#endif

extern "C" const char motley_build_identity[]
    __attribute__((used, section(".rodata_custom_desc"), aligned(4))) = MOTLEY_BUILD_IDENTITY;

extern "C" void app_main() {
    for (;;) {
        vTaskSuspend(nullptr);
    }
}
