import sys, os

path = 'kernel/reboot.c'
if not os.path.exists(path):
    print(f"SKIP: {path} not found")
    sys.exit(0)

with open(path, 'r') as f:
    content = f.read()

if 'ksu_handle_sys_reboot' in content:
    print("ksu_handle_sys_reboot already present in reboot.c — skipping")
    sys.exit(0)

# Insert extern declaration + call right after the first line inside SYSCALL_DEFINE4(reboot, ...)
# That line is: "	struct pid_namespace *pid_ns = task_active_pid_ns(current);"
hook_block = (
    '#ifdef CONFIG_KSU\n'
    '\textern void ksu_handle_sys_reboot(void);\n'
    '\tksu_handle_sys_reboot();\n'
    '#endif\n'
)

target = '\tstruct pid_namespace *pid_ns = task_active_pid_ns(current);\n'

if target not in content:
    print(f"ERROR: could not find target line in {path}")
    sys.exit(1)

content = content.replace(target, hook_block + target, 1)

with open(path, 'w') as f:
    f.write(content)

print("reboot.c patched: ksu_handle_sys_reboot hook added")
