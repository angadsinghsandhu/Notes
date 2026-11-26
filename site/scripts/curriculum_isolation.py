"""OS restrictions installed in the curriculum child before lesson execution."""

import ctypes
import errno
import resource
import sys


class IsolationError(RuntimeError):
    """The child could not establish the required limits."""


# The child prepares its evidence and diagnostic descriptors before confinement.
# Permit operations on existing descriptors, memory, signals, clocks and exit.
_LINUX_SYSCALLS = (
    "read",
    "write",
    "close",
    "fstat",
    "lseek",
    "brk",
    "mmap",
    "munmap",
    "mprotect",
    "mremap",
    "madvise",
    "futex",
    "clock_gettime",
    "clock_nanosleep",
    "nanosleep",
    "getpid",
    "gettid",
    "rt_sigaction",
    "rt_sigprocmask",
    "rt_sigreturn",
    "sigaltstack",
    "exit",
    "exit_group",
)
_DARWIN_PROFILE = b"(version 1) (deny default) (allow process-info-pidinfo)"
_ADDRESS_SPACE = 256 * 1024 * 1024


def confine(output_bytes: int) -> None:
    if sys.platform not in {"darwin", "linux"}:
        raise IsolationError(f"unsupported platform: {sys.platform}")
    try:
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_CPU, (4, 4))
        resource.setrlimit(resource.RLIMIT_FSIZE, (output_bytes, output_bytes))
        # Darwin rejects the address-space limit and uses the time/output bounds.
        if sys.platform == "linux":
            resource.setrlimit(resource.RLIMIT_AS, (_ADDRESS_SPACE, _ADDRESS_SPACE))
    except (OSError, ValueError) as exc:
        raise IsolationError("could not apply resource limits") from exc
    if sys.platform == "darwin":
        _seatbelt()
    else:
        _seccomp()


def _seatbelt() -> None:
    try:
        library = ctypes.CDLL("/usr/lib/libsandbox.1.dylib")
        initialize = library.sandbox_init
        initialize.argtypes = [
            ctypes.c_char_p,
            ctypes.c_uint64,
            ctypes.POINTER(ctypes.c_char_p),
        ]
        initialize.restype = ctypes.c_int
        release_error = library.sandbox_free_error
        release_error.argtypes = [ctypes.c_char_p]
        release_error.restype = None
    except (OSError, AttributeError) as exc:
        raise IsolationError("Darwin Seatbelt unavailable") from exc
    error = ctypes.c_char_p()
    if initialize(_DARWIN_PROFILE, 0, ctypes.byref(error)) != 0:
        if error.value is not None:
            release_error(error)
        raise IsolationError("could not enable Darwin Seatbelt")


def _seccomp() -> None:
    try:
        library = ctypes.CDLL("libseccomp.so.2")
        initialize = library.seccomp_init
        initialize.argtypes = [ctypes.c_uint32]
        initialize.restype = ctypes.c_void_p
        add_rule = library.seccomp_rule_add
        add_rule.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_int,
            ctypes.c_uint,
        ]
        add_rule.restype = ctypes.c_int
        resolve = library.seccomp_syscall_resolve_name
        resolve.argtypes = [ctypes.c_char_p]
        resolve.restype = ctypes.c_int
        load = library.seccomp_load
        load.argtypes = [ctypes.c_void_p]
        load.restype = ctypes.c_int
        release = library.seccomp_release
        release.argtypes = [ctypes.c_void_p]
        release.restype = None
    except (OSError, AttributeError) as exc:
        raise IsolationError("Linux libseccomp unavailable") from exc
    context = initialize(0x00050000 | errno.EPERM)  # SCMP_ACT_ERRNO
    if not context:
        raise IsolationError("could not initialize Linux seccomp")
    try:
        for name in _LINUX_SYSCALLS:
            syscall = resolve(name.encode("ascii"))
            if (
                syscall == -1 or add_rule(context, 0x7FFF0000, syscall, 0) != 0
            ):  # SCMP_ACT_ALLOW
                raise IsolationError(f"could not allow {name} under Linux seccomp")
        if load(context) != 0:
            raise IsolationError("could not enable Linux seccomp")
    finally:
        release(context)
