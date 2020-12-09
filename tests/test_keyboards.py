import unittest
from keyboards import PagingKeyboard


class TestPagingKeyboard(unittest.TestCase):
    def setUp(self) -> None:
        self.keyboard = PagingKeyboard()

    def tearDown(self) -> None:
        del self.keyboard

    def test_set_keyboard_size(self):
        self.keyboard.set_keyboard_size(5)
        self.assertEqual(self.keyboard.num_pages, 5)
        with self.assertRaises(AssertionError):
            self.keyboard.set_keyboard_size(0)

    def test_set_active_key(self):
        self.keyboard.set_keyboard_size(5)
        self.keyboard.set_active_key(5)
        self.assertEqual(self.keyboard.active_key, 5)

        with self.assertRaises(AssertionError):
            self.keyboard.set_active_key(6)

        with self.assertRaises(AssertionError):
            self.keyboard.set_active_key(0)

    # def test_make_keyboard(self):
    #     self.fail()
    #
    def test_prepare_simple_keyboard(self):
        self.keyboard.set_keyboard_size(1)


    #
    # def test_prepare_left_keyboard(self):
    #     self.fail()
    #
    # def test_prepare_right_keyboard(self):
    #     self.fail()
    #
    # def test_prepare_mid_keyboard(self):
    #     self.fail()
    #
    # def test_make_key(self):
    #     self.fail()
    #
    # def test_set_key_label(self):
    #     self.fail()


if __name__ == "__main__":
    unittest.main()
