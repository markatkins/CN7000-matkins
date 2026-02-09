# AI Developer Sudo Permissions

The `aidev` group has limited NOPASSWD sudo permissions for kernel module operations.

**Important**: Always use the full path `/usr/bin/sudo` with the `-n` (non-interactive) flag.

## Allowed Commands

### Module Loading (`insmod`)
- `/usr/bin/sudo -n /sbin/insmod */hfi1.ko [params]` - Load hfi1 kernel module with optional parameters
- `/usr/bin/sudo -n /sbin/insmod */rdmavt.ko [params]` - Load rdmavt kernel module with optional parameters

### Module Unloading (`rmmod`)
- `/usr/bin/sudo -n /sbin/rmmod hfi1` - Unload hfi1 kernel module
- `/usr/bin/sudo -n /sbin/rmmod rdmavt` - Unload rdmavt kernel module

## Usage Examples

```bash
# Load modules (rdmavt must be loaded before hfi1)
/usr/bin/sudo -n /sbin/insmod /path/to/rdmavt.ko
/usr/bin/sudo -n /sbin/insmod /path/to/hfi1.ko

# Load hfi1 with parameters
/usr/bin/sudo -n /sbin/insmod /path/to/hfi1.ko num_user_contexts=4

# Unload modules (hfi1 must be unloaded before rdmavt)
/usr/bin/sudo -n /sbin/rmmod hfi1
/usr/bin/sudo -n /sbin/rmmod rdmavt
```

## Notes

- Module load order: `rdmavt` before `hfi1`
- Module unload order: `hfi1` before `rdmavt`
- Only these specific modules are permitted; no other kernel modules can be loaded/unloaded via sudo