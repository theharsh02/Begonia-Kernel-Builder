import sys, os

path = 'fs/proc/cmdline.c'
if not os.path.exists(path):
    print(f"SKIP: {path} not found")
    sys.exit(0)

with open(path, 'r') as f:
    content = f.read()

extern_block = (
    '#ifdef CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG\n'
    'extern int susfs_spoof_cmdline_or_bootconfig(struct seq_file *m);\n'
    '#endif\n\n'
)

susfs_check = (
    '#ifdef CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG\n'
    '\tif (!susfs_spoof_cmdline_or_bootconfig(m)) {\n'
    '\t\tseq_putc(m, \'\\n\');\n'
    '\t\treturn 0;\n'
    '\t}\n'
    '#endif\n'
)

marker = 'static int cmdline_proc_show'
func_open = 'static int cmdline_proc_show(struct seq_file *m, void *v)\n{'

if extern_block not in content:
    content = content.replace(marker, extern_block + marker, 1)
    print('Inserted SUSFS extern declaration')

if susfs_check not in content:
    content = content.replace(func_open, func_open + '\n' + susfs_check, 1)
    print('Inserted SUSFS cmdline check')

with open(path, 'w') as f:
    f.write(content)

print('cmdline.c patched for SUSFS')
