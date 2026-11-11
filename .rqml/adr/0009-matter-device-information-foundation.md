# ADR-0009: Matter commissioning and standard device information

- **Status:** Accepted
- **Date:** 2026-11-09
- **Classification:** derived_from_requirements
- **Related requirements:** `MOT-PLAT-001`, `MOT-PLAT-004`, `MOT-INFO-001`, `MOT-BUILD-002`
- **Related ADRs:** [ADR-0002](0002-build-dependencies-and-code-tooling.md), [ADR-0004](0004-minimal-firmware-build.md), [ADR-0007](0007-size-limited-version-label.md)
- **Affected components:** SDK dependencies, Matter startup, commissioning/storage, build identity adapter, device model, build runner, hardware verification

## Context

The developer selected a commissionable Matter device with accessible firmware
information as the next milestone and confirmed that Home Assistant and a
working Thread border router are available. Product sensing and control remain
later work. The developer approved proceeding with this milestone.

The developer selected a development-style USB serial setup/reset interface for
this milestone. Defining and implementing deployed-device controls is deferred
to [issue #15](https://github.com/altendky/motley/issues/15).

The current build is ESP-IDF-only. Its read-only source mount and offline
compilation cannot acquire managed Matter dependencies in their default source
locations without a separate acquisition/staging decision.

## Decision drivers

- Demonstrate commissioning and real Home Assistant information reads.
- Preserve the full build identity and truthful device information.
- Use standard Matter attributes where practical.
- Retain reproducible dependencies and the existing artifact workflow.
- Keep application behavior small while physical and controller fit is tested.

## Options considered

| Option | Benefits | Costs and unresolved fit |
| --- | --- | --- |
| Managed esp-matter component with locked acquisition/staging | Product SDK without an additional full source checkout; documented match to current IDF pin | Runner needs an explicit dependency acquisition and writable-state design |
| Official combined ESP-Matter container/full source environment | Includes SDK and host tools | Larger environment and additional authoritative pins/identity to verify |
| Root endpoint only for the first information prototype | Avoids invented sensing or actuator behavior | Device-model conformity and installed-controller acceptance need validation |
| Add a genuine application endpoint immediately | Conventional application device model | Requires a meaningful device function and requirements beyond information access |

## Decision

Use managed `espressif/esp_matter` 1.6.1 with the existing ESP-IDF 6.0.2
container. Commit the complete generated dependency lock. Acquire dependencies
in a staged project copy with networking enabled, then compile read-only with
networking disabled. Check staged owned sources against the original inputs,
reject lock changes in ordinary builds, and record dependency content identities
in provenance. An explicit dependency-update operation produces a candidate lock
for review. Provide host commissioning/diagnostic tools separately when required.

Use BLE onboarding onto Thread and standard endpoint-zero Basic Information.
Show the commissioning code through the primary USB Serial/JTAG console and
provide the SDK's explicit `matter esp factoryreset` serial command. Physical
setup/reset controls are outside this milestone; ordinary serial connection and
reboot preserve commissioning state.
First prove the smallest root-node information prototype with the actual Home
Assistant installation. Source inspection suggests HA creates the device registry
entry independently of application entity discovery; this is an inference, not
an observed commissioning result or a conformity claim. Revisit the device model
before claiming the milestone if that prototype is unsuitable.

Serve the full current build identity through `SoftwareVersionString` when it
fits. The current SHA-1 identity plus cleanliness fits the standard capacity.
Keep the constrained SDK label separate. Install a static subclass of the SDK
configuration manager before its first use, overriding only the software-version
string getter. Preserve inherited SDK storage/reset behavior. Build and actual
Matter reads must validate this interface; changing a generated attribute alone
is not evidence of the transmitted value.

Use numeric `SoftwareVersion` 1, independently of the hash; revisit ordering
when OTA is specified. Use the SDK's development test vendor/product credentials,
vendor name `Motley development`, product name `Motley prototype`, and hardware
version 1 (`ESP32-C6 Feather prototype`). Disable the shared test serial number;
use the SDK's persisted random Basic Information UniqueID for stable identity
across ordinary reboot. Factory reset may regenerate that identity. Do not infer
product certification from an engineering commissioning test.

Commissioning persistence and deliberate reset use SDK/platform adapters. Avoid
creating an empty portable-core framework solely for this SDK integration; apply
the agreed core boundary when application decisions exist.

## Consequences

Use a single factory application partition and NVS in a 4 MiB layout, with
conservative DIO/40 MHz flashing. Confirm the connected Feather's actual flash
before flashing. Disable OTA and Wi-Fi station mode; use BLE onboarding and
Thread. A real device/controller test remains necessary for completion.
Diagnostics beyond SDK defaults and identification are outside this stage.

Advance `MOT-BUILD-001` from the completed idle-only bootstrap to the approved
Matter startup milestone. Its requirement and second acceptance criterion now
delegate application behavior to approved milestone requirements, preserving
their IDs and compiler/build/provenance obligations. This deliberately replaces
the earlier idle-only behavior; a separate bootstrap profile is unnecessary.

## Evidence

- [Published component compatibility](https://components.espressif.com/components/espressif/esp_matter/versions/1.6.1/readme) recommends the ESP-IDF release already pinned by Motley. Dependency resolution and SDK compilation/link/image inspection passed; the [plan](../plan.md#matter-integration-evidence-2026-11-09) records the tested source identities and the packaging rejection caused by concurrent checkout edits. A stable identified bundle remains to be verified.
- [Dependency lock guidance](https://docs.espressif.com/projects/idf-component-manager/en/latest/reference/dependencies_lock.html) describes the managed dependency record; [development routes](https://docs.espressif.com/projects/esp-matter/en/latest/esp32c6/developing.html) distinguish managed SDK delivery and host tools.
- [Pinned Basic Information schema](https://github.com/project-chip/connectedhomeip/blob/b1902b39ac6734913ce5f4d2abf153693a50264b/src/app/zap-templates/zcl/data-model/chip/basic-information-cluster.xml) defines the software identity fields and 64-character string capacity.
- [Pinned ESP32 default getter](https://github.com/project-chip/connectedhomeip/blob/b1902b39ac6734913ce5f4d2abf153693a50264b/src/platform/ESP32/ConfigurationManagerImpl.cpp) uses the SDK application descriptor; [manager registration](https://github.com/project-chip/connectedhomeip/blob/b1902b39ac6734913ce5f4d2abf153693a50264b/src/include/platform/ConfigurationManager.h) and the [ESP-Matter integration](https://github.com/espressif/esp-matter/blob/release/v1.6.1/components/esp_matter/data_model_provider/clusters/basic_information/integration.cpp) support the implemented narrow override. It compiled successfully; transmitted attributes and Home Assistant presentation remain unverified on hardware.
- [Home Assistant's adapter](https://github.com/home-assistant/core/blob/dev/homeassistant/components/matter/adapter.py) maps the standard string into device firmware information. Installed-version behavior still needs verification.

## Supersession

Supersedes: ADR-0004's idle-only startup and dependency-free build decisions.
Its compiler, container, artifact and provenance decisions remain applicable.
Superseded by: None.
