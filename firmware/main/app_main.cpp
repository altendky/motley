#include "build_identity.hpp"
#include <cstdlib>
#include <cstring>
#include <string_view>
#include <esp_log.h>
#include <esp_matter.h>
#include <esp_matter_console.h>
#include <esp_openthread_types.h>
#include <nvs_flash.h>
#include <platform/ConfigurationManager.h>
#include <platform/ESP32/OpenthreadLauncher.h>
#include <setup_payload/OnboardingCodesUtil.h>

#if defined(__cpp_exceptions) || defined(__GXX_RTTI)
#error "Owned firmware code requires exceptions and RTTI disabled"
#endif

extern "C" const char motley_build_identity[]
    __attribute__((used, section(".rodata_custom_desc"), aligned(4))) = MOTLEY_BUILD_IDENTITY;

namespace {
constexpr char firmware_version[] = MOTLEY_FIRMWARE_VERSION;
constexpr std::string_view matter_version = sizeof(firmware_version) <= 65
    ? MOTLEY_FIRMWARE_VERSION : MOTLEY_SDK_VERSION;
static_assert(matter_version.size() <= 64, "Matter software version string capacity exceeded");

// The SDK retains responsibility for persistent identity, fabric storage and reset.
class ConfigurationManager final : public chip::DeviceLayer::ConfigurationManagerImpl {
public:
    CHIP_ERROR GetSoftwareVersionString(char *buffer, size_t capacity) override {
        if (capacity < matter_version.size() + 1) {
            return CHIP_ERROR_BUFFER_TOO_SMALL;
        }
        std::memcpy(buffer, matter_version.data(), matter_version.size() + 1);
        return CHIP_NO_ERROR;
    }
};
ConfigurationManager configuration_manager;
}

extern "C" void app_main() {
    chip::DeviceLayer::SetConfigurationMgr(&configuration_manager);
    // Fail visibly instead of silently erasing a commissioned device on NVS errors.
    ESP_ERROR_CHECK(nvs_flash_init());

    esp_matter::node::config_t node_config{};
    if (esp_matter::node::create(&node_config, nullptr, nullptr) == nullptr) {
        ESP_LOGE("motley", "Matter root node creation failed");
        std::abort();
    }

    esp_openthread_platform_config_t thread_config{};
    thread_config.radio_config.radio_mode = RADIO_MODE_NATIVE;
    thread_config.host_config.host_connection_mode = HOST_CONNECTION_MODE_NONE;
    thread_config.port_config.storage_partition_name = "nvs";
    thread_config.port_config.netif_queue_size = 10;
    thread_config.port_config.task_queue_size = 10;
    ESP_ERROR_CHECK(set_openthread_platform_config(&thread_config));
    ESP_ERROR_CHECK(esp_matter::start(nullptr));
    PrintOnboardingCodes(chip::RendezvousInformationFlags(chip::RendezvousInformationFlag::kBLE));
    ESP_ERROR_CHECK(esp_matter::console::factoryreset_register_commands());
    ESP_ERROR_CHECK(esp_matter::console::init());
    ESP_LOGI("motley", "Firmware %s; development reset: matter esp factoryreset", firmware_version);
}
