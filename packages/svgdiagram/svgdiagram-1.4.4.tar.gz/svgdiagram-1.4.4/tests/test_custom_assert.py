from unittest import TestCase

from .custom_assert import SAVE_MISMATCH_TO, OVERRIDE


class TestCustomAssert(TestCase):
    def test_save_missmatch_to(self):
        self.assertEqual(SAVE_MISMATCH_TO, '')

    def test_override(self):
        self.assertFalse(OVERRIDE)
