from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Додати ФОП або ТОВ", callback_data="fop_tov_add")
        ],
        [
            InlineKeyboardButton(text="Редагування організацій", callback_data="refactor")
        ],
        [
            InlineKeyboardButton(text="Знайти по ЄДРПОУ", callback_data="find_by_edrpoy")
        ]
    ]
)

start_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Знайти по ЄДРПОУ", callback_data="find_by_edrpoy")
        ]
    ]
)

main_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="До головного меню", callback_data="main_menu")
        ]
    ]
)

cancel_inline = InlineKeyboardMarkup(
    inline_keyboard = [
        [
          InlineKeyboardButton(text="Відміна❌", callback_data="cancel")
        ],
    ]
)

refactor_organization = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Редагувати📝", callback_data="refactor_organization")
        ],
        [
            InlineKeyboardButton(text="Видалити❌", callback_data="delete_organization")
        ],
        [
            InlineKeyboardButton(text="⏪ Назад", callback_data="back_organization"),
            InlineKeyboardButton(text="Вперел ⏩", callback_data="forward_organization")
        ]

    ]
)
