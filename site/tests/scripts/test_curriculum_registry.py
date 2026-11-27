import importlib
import unittest

from scripts import curriculum
from scripts.curriculum_minimum_path_sum import verify_row_storage
from scripts.curriculum_trace import PythonAdapter


class CurriculumRegistryTests(unittest.TestCase):
    def test_reviewed_row_storage_enrollment_is_available_to_the_cli(self) -> None:
        registry = importlib.import_module("scripts.curriculum_registry")
        self.assertIs(curriculum.Enrollment, registry.Enrollment)
        self.assertIs(curriculum.Registry, registry.Registry)
        self.assertIs(curriculum._ENROLLED, registry.ENROLLED)
        self.assertEqual(
            registry.ENROLLED[64, "row-storage"],
            curriculum.Enrollment(
                "solutions.py",
                "8f11ee992b9ae3158008046c2ce8ca7cf093df5a152030940b63243a41883842",
                PythonAdapter("row_storage"),
                verify_row_storage,
            ),
        )
