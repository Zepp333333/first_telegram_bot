from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils import helpers

# test_keyboard = [['top-left', 'top-right'],
#                  ['bottom-left', 'bottom-right']]
# reply_markup = ReplyKeyboardMarkup(test_keyboard)
#
# test_inline_keyboard = [
#     [
#         InlineKeyboardButton("Option 1", callback_data='1'),
#         InlineKeyboardButton("Option 2", callback_data='2'),
#     ],
#     [InlineKeyboardButton("Option 3", callback_data='3')],
# ]
#
# reply_inline_test_markup = InlineKeyboardMarkup(test_inline_keyboard)
#
#
# def make_single_button_kbd(key_name, key_payload):
#     return InlineKeyboardMarkup.from_button(
#         InlineKeyboardButton(key_name, key_payload)
#     )
#
# def prepare_pin_message_kbd(bot, destination):
#     url = helpers.create_deep_linked_url(bot_username=bot.get_me().username, payload=destination)
#     return make_single_button_kbd('start', url)
#
#
# def keyboard_maker(keys: list):
#     def recursive_map(f, lst):
#         return (list(recursive_map(f, x) if isinstance(x, list) else f(x) for x in lst))
#
#     result = recursive_map(lambda k: InlineKeyboardButton(k, callback_data=k), keys)
#     return InlineKeyboardMarkup(result)
#     # def convert_key_to_markup(k):
#     #     return InlineKeyboardButton(k, callback_data=key)


class PagingKeyboard:
    def __init__(self,
                 num_pages: int = 1,
                 keys_above: 'list[InlineKeyboardButton]' = None,
                 keys_below: 'list[InlineKeyboardButton]' = None
                 ):
        assert num_pages >= 1
        self.num_pages: int = num_pages
        self.active_key: int = 0
        self.keys_above = keys_above
        self.keys_below = keys_below
        self.keyboard: list[InlineKeyboardButton] = self.initialize_keyboard()

    def set_keyboard_size(self, num_pages: int) -> None:
        assert num_pages >= 1
        self.num_pages = num_pages

    def initialize_keyboard(self):
        keyboard_size = 5 if self.num_pages > 5 else self.num_pages
        return [InlineKeyboardButton('') for _ in range(keyboard_size)]

    def set_active_key(self, key: int = 0) -> None:
        assert 0 <= key <= self.num_pages-1
        self.active_key = key

    def make_keyboard_markup(self, active_key: int = None) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(self.make_keyboard(active_key))

    def make_keyboard(self, active_key: int) -> 'list[list[InlineKeyboardButton]]':
        self.set_active_key(active_key)

        if self.num_pages <= 5:
            self.prepare_simple_keyboard()
        else:
            if self.active_key <= 2:
                self.prepare_left_keyboard()
            elif self.active_key >= self.num_pages - 2:
                self.prepare_right_keyboard()
            else:
                self.prepare_mid_keyboard()

        return self.return_inline_keyboard()

    def return_inline_keyboard(self) -> 'list[list[InlineKeyboardButton]]':
        result = []
        if self.keys_above:
            result.append(self.keys_above)
        result.append(self.keyboard)
        if self.keys_below:
            result.append(self.keys_below)
        return result

    def prepare_simple_keyboard(self) -> None:
        for k in range(self.num_pages):
            if k == self.active_key:
                label = 'active'
            else:
                label = 'inactive'
            self.keyboard[k] = self.make_key(k, label)

    def prepare_left_keyboard(self) -> None:
        for k in range(4):
            if k == self.active_key:
                label = 'active'
            elif k == 3:
                label = 'fwd'
            else:
                label = 'inactive'
            self.keyboard[k] = self.make_key(k, label)
        self.keyboard[4] = self.make_key(self.num_pages-1, 'ffwd') # num_pages -1 as we internally count buttons from 0

    def prepare_right_keyboard(self) -> None:
        last_page = self.num_pages
        self.keyboard[0] = self.make_key(0, 'fback')
        page = last_page-4
        for k in range(1, 5):
            if page == self.active_key:
                label = 'active'
            elif page == last_page-4:
                label = 'back'
            else:
                label = 'inactive'
            self.keyboard[k] = self.make_key(page, label)
            page += 1

    def prepare_mid_keyboard(self) -> None:
        active_key = self.active_key
        last_page = self.num_pages
        self.keyboard[0] = self.make_key(0, 'fback')
        self.keyboard[1] = self.make_key(active_key - 1, 'back')
        self.keyboard[2] = self.make_key(active_key, 'active')
        self.keyboard[3] = self.make_key(active_key + 1, 'fwd')
        self.keyboard[4] = self.make_key(last_page -1 , 'ffwd') # num_pages -1 as we internally count buttons from 0

    def make_key(self, key: int, label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self.set_key_label(key, label=label), callback_data=f'#{str(key)}')

    @staticmethod
    def set_key_label(key: int, label: str = 'inactive') -> str:
        key += 1  # So that keyboard starts with 1 instead of 0
        key_text = {
            'inactive': f'  {str(key)}  ',
            'active': f'• {str(key)} •',
            'fwd': f'  {str(key)} >',
            'ffwd': f'  {str(key)} »',
            'back': f'< {str(key)}  ',
            'fback': f'« {str(key)}  ',
        }
        return key_text[label]


