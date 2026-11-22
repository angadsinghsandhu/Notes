import unittest
from unittest.mock import Mock, patch

from scripts.curriculum_isolation import IsolationError, confine


class CurriculumIsolationTests(unittest.TestCase):
    def test_unsupported_platform_fails_closed(self) -> None:
        with (
            patch("scripts.curriculum_isolation.sys.platform", "unsupported"),
            self.assertRaisesRegex(IsolationError, "unsupported"),
        ):
            confine(1024)

    def test_missing_backend_fails_closed(self) -> None:
        with (
            patch("scripts.curriculum_isolation.sys.platform", "linux"),
            patch("scripts.curriculum_isolation.ctypes.CDLL", side_effect=OSError),
            patch("scripts.curriculum_isolation.resource.setrlimit"),
            self.assertRaisesRegex(IsolationError, "unavailable"),
        ):
            confine(1024)

    def test_failed_resource_limit_fails_closed(self) -> None:
        with (
            patch(
                "scripts.curriculum_isolation.resource.setrlimit",
                side_effect=ValueError,
            ),
            self.assertRaisesRegex(IsolationError, "resource limits"),
        ):
            confine(1024)

    def test_linux_load_failure_never_continues(self) -> None:
        library = Mock()
        library.seccomp_init.return_value = 1
        library.seccomp_syscall_resolve_name.return_value = 2
        library.seccomp_rule_add.return_value = 0
        library.seccomp_load.return_value = -1
        with (
            patch("scripts.curriculum_isolation.sys.platform", "linux"),
            patch("scripts.curriculum_isolation.resource.setrlimit"),
            patch("scripts.curriculum_isolation.ctypes.CDLL", return_value=library),
            self.assertRaisesRegex(IsolationError, "could not enable Linux seccomp"),
        ):
            confine(1024)
        library.seccomp_release.assert_called_once_with(1)
