from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def make_paging_keyboard(
        total_pages: int,
        active_page: int = 0,
        keys_above: 'list[InlineKeyboardButton]' = [],
        keys_below: 'list[InlineKeyboardButton]' = []) -> InlineKeyboardMarkup:

    key_values = {i: str(i + 1) for i in range(total_pages)}
    last_page = total_pages -1
    print(key_values)

    def set_key_label(key_value: str, label: str = 'inactive') -> str:
        key_text = {
            'inactive': f'  {key_value}  ',
            'active': f'• {key_value} •',
            'fwd': f'  {key_value} >',
            'ffwd': f'  {key_value} »',
            'back': f'< {key_value}  ',
            'fback': f'« {key_value}  ',
        }
        return key_text[label]

    def initialize_keyboard() -> 'list[InlineKeyboardButton]':
        keyboard_size = 5 if total_pages > 5 else total_pages
        return [InlineKeyboardButton('') for _ in range(keyboard_size)]

    def make_key(key: int, label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=set_key_label(key_values[key], label=label),
            callback_data=f'#{str(key)}'
        )

    def prepare_simple_keyboard() -> 'list[InlineKeyboardButton]':
        keyboard = initialize_keyboard()
        for k in range(total_pages):
            if k == active_page:
                label = 'active'
            else:
                label = 'inactive'
            keyboard[k] = make_key(k, label)
        return keyboard

    def prepare_left_keyboard() -> 'list[InlineKeyboardButton]':
        keyboard = initialize_keyboard()
        for k in range(4):
            if k == active_page:
                label = 'active'
            elif k == 3:
                label = 'fwd'
            else:
                label = 'inactive'
            keyboard[k] = make_key(k, label)
        keyboard[4] = make_key(last_page, 'ffwd')
        return keyboard

    def prepare_right_keyboard() -> 'list[InlineKeyboardButton]':
        keyboard = initialize_keyboard()
        keyboard[0] = make_key(0, 'fback')
        page = total_pages - 4
        for k in range(1, 5):
            if page == active_page:
                label = 'active'
            elif page == total_pages - 4:
                label = 'back'
            else:
                label = 'inactive'
            keyboard[k] = make_key(page, label)
            page += 1
        return keyboard

    def prepare_mid_keyboard() -> 'list[InlineKeyboardButton]':
        keyboard = initialize_keyboard()
        keyboard[0] = make_key(0, 'fback')
        keyboard[1] = make_key(active_page - 1, 'back')
        keyboard[2] = make_key(active_page, 'active')
        keyboard[3] = make_key(active_page + 1, 'fwd')
        keyboard[4] = make_key(last_page, 'ffwd')
        return keyboard

    def prepare_paging_keyboard() -> 'list[InlineKeyboardButton]':
        if total_pages <= 5:
            keyboard = prepare_simple_keyboard()
        else:
            if active_page <= 2:
                keyboard = prepare_left_keyboard()
            elif active_page >= total_pages - 2:
                keyboard = prepare_right_keyboard()
            else:
                keyboard = prepare_mid_keyboard()
        return keyboard

    def prepare_keyboard() -> 'list[list[InlineKeyboardButton]]':
        keyboard = []
        if keys_above:
            keyboard.append(keys_above)
        keyboard.append(prepare_paging_keyboard())
        if keys_below:
            keyboard.append(keys_below)
        return keyboard

    return InlineKeyboardMarkup(prepare_keyboard())


# todo : delete
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


