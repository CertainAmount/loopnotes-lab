# Why does Ollama fall back to the CPU after an Ubuntu update, and when did the driver change?

Checked 2026-11-16. This note backs the article "Ollama not using GPU after an update" on loopnotes.dev. It covers Ubuntu with an NVIDIA driver installed from the Ubuntu archive (`nvidia-driver-XXX` packages). The machine used for these checks has no GPU. No GPU or Ollama behaviour was measured here. What was checked are the Ubuntu and apt defaults that decide whether an NVIDIA driver can be upgraded without you, when that happens, and whether the machine reboots afterwards.

## Conclusions

1. On a default Ubuntu install, unattended-upgrades is allowed to install packages from the `-security` pocket, and Ubuntu archive NVIDIA drivers do ship through that pocket. If you upgraded nothing, check the unattended upgrade before you reinstall or downgrade Ollama.
2. The unattended install runs between about 06:00 and 07:00 local time on a machine that was left on, or soon after the next boot if it was off then. It does not run "overnight". The `Start-Date` of the last block in `/var/log/apt/history.log` should match one of those two times.
3. Unattended-upgrades does not reboot by default. Ubuntu's own driver update policy says that a driver update leaves the loaded kernel module and the new user-space libraries at different versions until a reboot. Restarting the Ollama service does not fix that. Reboot the machine.
4. `Package-Blacklist` only applies to unattended-upgrades. `apt-mark hold` stops apt from automatically installing, upgrading or removing a package, so it also covers an `apt upgrade` you type yourself. To stop this happening again, use both, and hold every installed NVIDIA package, not just one.
5. NVIDIA driver security fixes keep coming for current Ubuntu LTS releases, so a hold is not permanent. Plan a manual upgrade that you finish with an immediate reboot.

## 1. When unattended-upgrades runs (apt timers)

The `apt-daily-upgrade.timer` unit starts the unattended install. Its settings are the same on Ubuntu 22.04 and 24.04:

| Setting | Ubuntu 22.04 (apt 2.4.10, read on this machine) | Ubuntu 24.04 (apt 2.7.14, upstream tag) |
|---|---|---|
| `OnCalendar` | `*-*-* 6:00` | `*-*-* 6:00` |
| `RandomizedDelaySec` | `60m` | `60m` |
| `Persistent` | `true` | `true` |

- Calculation: a 06:00 start plus up to 60 minutes of random delay puts the install between 06:00 and 07:00 local time. With `Persistent=true`, a machine that was off at that time runs the install soon after it next boots.
- `apt-daily.timer`, which downloads package lists and packages, runs at `6,18:00` with up to 12 hours of random delay. It downloads packages but does not install them.
- Raw files: [`apt-timers-2204.txt`](apt-timers-2204.txt) and [`apt-timers-2404-upstream.txt`](apt-timers-2404-upstream.txt). The 24.04 file comes from the apt source repository on salsa.debian.org, tag 2.7.14, fetched 2026-11-16.

## 2. What unattended-upgrades may install and whether it reboots

From the default `/etc/apt/apt.conf.d/50unattended-upgrades` shipped with unattended-upgrades 2.8ubuntu1 (Ubuntu 22.04), read 2026-11-16:

- `Unattended-Upgrade::Allowed-Origins` includes `${distro_id}:${distro_codename}-security`.
- `Unattended-Upgrade::Package-Blacklist` takes Python regular expressions, and its default entries are all commented out. Nothing is excluded by default.
- `//Unattended-Upgrade::Automatic-Reboot "false";` is commented out, so the default applies: no automatic reboot.
- This machine's own `20auto-upgrades` has unattended upgrades switched off (`"0"`). That is a local server setting, not the Ubuntu default. It is recorded here so nobody mistakes it for one.

Raw lines: [`apt-mark-and-unattended-defaults-2204.txt`](apt-mark-and-unattended-defaults-2204.txt).

## 3. Scope of `apt-mark hold`

apt-mark(8), apt 2.4.10, read 2026-11-16: "hold is used to mark a package as held back, which will prevent the package from being automatically installed, upgraded or removed." The same raw file is linked in section 2.

| Mechanism | Unattended upgrade | `apt upgrade` typed by hand |
|---|---|---|
| `Package-Blacklist` in `50unattended-upgrades` | blocked | not blocked |
| `apt-mark hold` | blocked | blocked |

The left column comes from Ubuntu's Automatic updates page, which describes the blacklist as an unattended-upgrades setting. The right column comes from the apt-mark text above.

## 4. Official pages put side by side

None of these pages says on its own that a default Ubuntu install can upgrade the NVIDIA driver in the morning, leave the old module loaded, and leave Ollama on the CPU. That conclusion only appears when they are read together.

| Source | What it says (relevant part) | Read |
|---|---|---|
| [Ubuntu Server docs: Automatic updates](https://ubuntu.com/server/docs/how-to/software/automatic-updates/) | unattended-upgrades is installed by default and runs daily. `Package-Blacklist` lives in `50unattended-upgrades` and takes regular expressions. `20auto-upgrades` switches it on or off. | 2026-11-16 (search snippet) |
| [Ubuntu SRU: NVIDIA GPU driver updates](https://ubuntu.com/project/docs/SRU/reference/exception-NVidia-Updates) | Updating the driver creates a version mismatch between the loaded kernel module and the user-space components. A reboot right away is recommended, even for minor updates. | 2026-11-16 (page fetched, no date on page) |
| [noble-changes: nvidia-graphics-drivers-580 580.126.09-0ubuntu0.24.04.2 accepted into noble-security](https://lists.snapcraft.io/archives/noble-changes/2026-March/054040.html) | A real case of the 24.04 driver going out through the `-security` pocket (March 2026). | 2026-11-16 (search snippet) |
| [Ubuntu CVE-2026-24197](https://ubuntu.com/security/CVE-2026-24197) | A security fix for the 580 driver packages ships to 24.04 LTS and other releases as 580.159.03. Driver security updates keep coming. | 2026-11-16 (search snippet) |
| [Ollama FAQ](https://docs.ollama.com/faq) | `ollama ps` PROCESSOR column shows `100% GPU`, `100% CPU`, or a CPU/GPU split. | 2026-11-16 (search snippet) |
| [Ollama GPU docs](https://docs.ollama.com/gpu) | NVIDIA needs compute capability 5.0+ and driver 550+ (570+ for 5.0–6.2). After suspend/resume Ollama can fail to find the GPU and fall back to the CPU. Reloading `nvidia_uvm` fixes that. | 2026-11-16 (page fetched, no date on page) |
| [Ollama troubleshooting](https://docs.ollama.com/troubleshooting) | On systemd Linux, server logs are in `journalctl -u ollama`. | 2026-11-16 (search snippet) |

## 5. Other people's reports of the same failure

These are reports from other people. They show the same thing happening elsewhere. Each has a one-line summary.

- [Launchpad #2031178, "Loaded previous kernel module breaks during upgrade"](https://bugs.launchpad.net/bugs/2031178): the old module stays loaded during an upgrade, and the GPU is unusable with an NVML mismatch until a reboot.
- [Launchpad #1917119, "NVIDIA update 460.39 breaks system until reboot"](https://bugs.launchpad.net/bugs/1917119): the same failure in 2021, so this is not tied to one driver version.
- [NVIDIA developer forum: unattended-upgrades leads to NVML driver/library version mismatch](https://forums.developer.nvidia.com/t/ubuntu-unattended-upgrades-leads-to-failed-to-initialize-nvml-driver-library-version-mismatch/250484): users report that an unattended upgrade caused the mismatch.
- [Launchpad #1824804](https://bugs.launchpad.net/ubuntu/+source/unattended-upgrades/+bug/1824804): a report of unattended-upgrades acting on held packages. We did not confirm its status. It is listed here as one more reason to use the blacklist and the hold together, and the article does not rely on it.

Top search results for "ollama not using gpu after update linux" on 2026-11-16, for comparison: a nuvotex blog post about rolling back a Windows driver, [ollama/ollama #4563](https://github.com/ollama/ollama/issues/4563), which is about Docker Desktop, and a macmyths guide that covers `ollama ps` but not `nvidia-smi`, the reboot, or preventing a repeat. None of the top ten explained how to stop the problem coming back.

## 6. How a reader can confirm which tool upgraded the driver

Run these before you reboot, because a reboot loads the new module and the mismatch disappears.

1. `cat /proc/driver/nvidia/version` shows the version of the module that is currently loaded.
2. `dpkg -l nvidia-driver-580` (use your driver branch) shows the version of the installed package. If it differs from step 1, you have the mismatch.
3. Look at the last block of `/var/log/apt/history.log`. `Commandline: /usr/bin/unattended-upgrade` with a `Start-Date` between 06:00 and 07:00, or just after a boot, means the unattended upgrade did it. An `apt upgrade` or `apt install` command line means someone upgraded by hand and did not reboot. Either way, the fix is to reboot.
4. `/var/log/unattended-upgrades/unattended-upgrades.log` lists the packages that the unattended run upgraded.

No command output from these steps is reproduced here, because the test machine has no NVIDIA driver. No version numbers were made up.

## Limits

- No GPU measurement. The test machine has no GPU, so this note shows no Ollama speed, `ollama ps` output, or `nvidia-smi` output from a real failure. The failure itself is documented by Ubuntu's driver policy and the reports in section 5.
- The conclusions apply to NVIDIA drivers from the Ubuntu archive with the default unattended-upgrades settings. Drivers installed with NVIDIA's `.run` installer or from NVIDIA's CUDA repository take a different path. A machine with `Automatic-Reboot` turned on reboots on its own.
- The 24.04 timer values come from the upstream apt source for the version 24.04 ships, not from a running 24.04 system.
- Some official pages were read from search snippets, not full page fetches. The table in section 4 says which.
- No Naver or other Korean web counts were collected. This is an English-language Linux question with no Korea angle.
- No dataset was built. The values that matter can only be measured on a machine with an NVIDIA GPU.

## 7. Kernel updates while the NVIDIA driver is held (added 2026-11-16, reader fix)

A reader asked whether holding and blacklisting the NVIDIA packages, `linux-modules-nvidia-.*` included, leaves the next kernel without an NVIDIA module. It depends on how the module is installed.

| Source | What it says (relevant part) | Read |
|---|---|---|
| [Ubuntu Server docs: NVIDIA drivers installation](https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/) | `ubuntu-drivers` installs the pre-built, signed modules by default (`linux-modules-nvidia-${DRIVER_BRANCH}-${FLAVOUR}`). The DKMS package (`nvidia-dkms-${DRIVER_BRANCH}`) with `linux-headers` is the alternative. Its troubleshooting section gives the same `Driver/library version mismatch` cause and says a reboot fixes it. | 2026-11-16 (page fetched) |
| [packages.ubuntu.com: linux-modules-nvidia-580-generic, noble-updates](https://packages.ubuntu.com/noble-updates/linux-modules-nvidia-580-generic) | Version 6.8.0-149.149. Depends on `linux-modules-nvidia-580-6.8.0-149-generic (= 6.8.0-149.149)` and `nvidia-kernel-common-580 (>= 580.178.04)`. | 2026-11-16 (page fetched) |
| [packages.ubuntu.com: linux-modules-nvidia-580-6.8.0-149-generic](https://packages.ubuntu.com/noble-updates/linux-modules-nvidia-580-6.8.0-149-generic) | Depends on `linux-image-6.8.0-149-generic` and `nvidia-kernel-common-580 (>= 580.178.04)`. One module package per kernel ABI. | 2026-11-16 (page fetched) |
| [dkms(8), noble](https://manpages.ubuntu.com/manpages/noble/man8/dkms.8.html) | `autoinstall`: "Attempt to install the latest revision of all modules that have been installed for other kernel revisions." This is what runs when a new kernel is installed. | 2026-11-16 (page fetched) |

Conclusion used in the article: with pre-built modules, each new kernel gets its NVIDIA module only through an upgrade of the `linux-modules-nvidia-580-generic` metapackage, which the hold and the blacklist stop. A kernel from `-security` still installs unattended, and booting into it leaves no NVIDIA module, so Ollama falls back to the CPU. With `nvidia-dkms-580` (the author's setup), DKMS builds the held driver version for the new kernel when the kernel's headers are installed. The article gives one check that works for both: `modinfo -k <newest kernel> -F version nvidia` prints a version if a module exists for that kernel, and fails with `Module nvidia not found` if not.

Commands in the article's manual upgrade, and why they look this way:

- Held packages show as `hi`, not `ii`, in `dpkg -l`, so the hold line (`$1=="ii"`) cannot be reused to unhold. The article takes the held set from `apt-mark showhold | grep nvidia`, saves it to a file, unholds it, and upgrades only those packages with `apt install --only-upgrade`. After the upgrade the packages are `ii` again, so rerunning the hold line re-holds the set plus any package the upgrade added (for example a new per-kernel module package).
- None of these commands was run on an NVIDIA machine here; the test machine has no GPU (see Limits). The sequence is the author's (unhold, `apt install`, `dkms status`, reboot, `ollama ps`, hold again), with the package arguments filled in from apt-mark(8) and dpkg's status letters.

## 8. When the reboot doesn't bring the GPU back (added 2026-11-16, reader fix 2)

A reader asked what to do if `nvidia-smi` still fails after the reboot (a failed DKMS build, or Secure Boot refusing the module).

| Source | What it says (relevant part) | Read |
|---|---|---|
| [Ubuntu Security docs: UEFI Secure Boot](https://documentation.ubuntu.com/security/security-features/platform-protections/secure-boot/) | "Unsigned modules aren't loaded by the kernel." New DKMS modules are signed with the MOK; on the first boot after the key is created, MokManager asks to "Enroll MOK", and after that reboot "third-party drivers signed by the newly enrolled MOK load as necessary." | 2026-11-16 (page fetched) |
| [Ubuntu Server docs: NVIDIA drivers installation](https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/) | `ubuntu-drivers` installs "the pre-built, signed drivers which are known to work with Secure Boot"; "the DKMS drivers are not signed with Canonical's key". For the version mismatch it says to check `sudo dmesg` for API mismatch messages and reboot. | 2026-11-16 (page fetched) |

Conclusion used in the article: after a reboot, a still-failing `nvidia-smi` means the new module didn't load. `sudo dmesg | grep -i nvidia` shows the reason; on DKMS, `dkms status` without an `installed` line for `uname -r` means the build failed; with Secure Boot on, a DKMS module loads only after its key is confirmed on the Enroll MOK screen, while the pre-built modules are already signed. Not run here (no NVIDIA GPU on the test machine).

Cut from the body in the same pass (reader: scene detail that didn't help): the agent and codebase named in the slow-reply scene, the reply-latency numbers ("two or three seconds", "more than ten"), and the `journalctl -u ollama` check. The scene keeps its point (context and an Ollama update were ruled out first; about ten minutes lost before checking the hardware).

Article: [Ollama Not Using GPU After an Update on Linux: The Fix](https://loopnotes.dev/ollama-not-using-gpu-after-update/)
