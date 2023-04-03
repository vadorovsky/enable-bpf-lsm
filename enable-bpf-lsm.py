#!/usr/bin/env python3

import subprocess

def main():
    with open("/sys/kernel/security/lsm", "r") as f:
        lsms = f.read().strip().split(",")

    if "bpf" in lsms:
        print("BPF LSM is already enabled")
        return

    lsms.append("bpf")

    content = []
    with open("/etc/default/grub", "r") as f:
        for l in f:
            if l.startswith("GRUB_CMDLINE_LINUX=") and "lsm" not in l:
                cmdline = l.lstrip("GRUB_CMDLINE_LINUX=\"").rstrip("\"\n")
                cmdline_lsm = "lsm={}".format(",".join(lsms))
                if cmdline == "":
                    cmdline = cmdline_lsm
                else:
                    cmdline += " " + cmdline_lsm
                l = 'GRUB_CMDLINE_LINUX="{}"\n'.format(cmdline)
            content.append(l)

    with open("/etc/default/grub", "w") as f:
        for l in content:
            f.write(l)

    subprocess.run(["grub2-mkconfig", "-o", "/boot/grub2/grub.cfg"])

    print("BPF LSM is now enabled. Please reboot your system.")


if __name__ == "__main__":
    main()