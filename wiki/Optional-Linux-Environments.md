# Optional Linux Environments: PRoot and NetHunter

This page records a support boundary, not an installer. SYN_LAUNCH does not automatically install a Linux distribution, change Android settings, root a device, flash a kernel, or configure NetHunter.

## PRoot-Distro

Upstream project: https://github.com/termux/proot-distro

PRoot-Distro can provide a rootless Linux userspace inside Termux. It is useful for testing Linux-oriented package workflows and applications that do not require host-level privileges. It is not a VM and does not supply a separate kernel.

Important limits documented upstream include:
- A simulated root identity inside PRoot is not Android host root.
- Kernel features and operations that require real root, mounts, network namespaces, kernel modules, or some service managers remain unavailable.
- Filesystem-heavy workloads can be slower because PRoot intercepts system calls.
- Cross-architecture Termux-type containers are not supported as a way to hide host-architecture binaries.

SYN_LAUNCH support policy:
- Native Termux remains the primary supported environment.
- PRoot presence may be detected as environment context in a future capability profile, but is not an installability or compatibility guarantee.
- Any future PRoot integration must be opt-in, read-only during discovery, and must never reset or remove a container without a separate explicit action.

## Kali NetHunter

Official documentation:
- Overview and editions: https://www.kali.org/docs/nethunter/
- NetHunter Rootless: https://www.kali.org/docs/nethunter/nethunter-rootless/
- Device-specific installation: https://www.kali.org/docs/nethunter/installing-nethunter/

Kali documents three materially different configurations:
- **Rootless:** userspace tools on an unrooted, stock Android device; some capabilities are unavailable.
- **NetHunter Lite:** rooted device, with fewer kernel-dependent features.
- **Full NetHunter:** supported device and purpose-built kernel for additional hardware/kernel features.

A PRoot or NetHunter userspace does not by itself grant Android host root, Wi-Fi injection, HID support, privileged packet capture, or other kernel-dependent functionality. Device support, kernel, root state, ABI, and Android version must be evaluated separately.

SYN_LAUNCH support policy:
- NetHunter is an optional integration, not a prerequisite for native Termux.
- Do not recommend flashing a kernel or rooting a phone as an automatic remediation.
- Do not infer that a tool works merely because it is available inside a Kali userspace.
- Before any integration, test the user's exact device/edition and document the edition, kernel, root state, architecture, and feature-level evidence.

## Current implementation status

SYN_LAUNCH has read-only local device audit and APK archive inventory adapters. PRoot/NetHunter detection and installation management are not implemented. The roadmap tracks these as optional future work.
