from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Administrator keyboard
admin_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Додати ФОП або ТОВ➕", callback_data="fop_tov_add")
        ],
        [
            InlineKeyboardButton(text="Редагування організацій📝", callback_data="refactor")
        ],
        [
            InlineKeyboardButton(text="Знайти по ЄДРПОУ🔍", callback_data="find_by_edrpoy")
        ],
        [
            InlineKeyboardButton(text="Організації💼", callback_data="organization")
        ]
    ]
)

# User keyboard
user_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Знайти по ЄДРПОУ🔍", callback_data="find_by_edrpoy")
        ],
        [
            InlineKeyboardButton(text="Організації💼", callback_data="organization")
        ]
    ]
)

# Main menu markup ( created for return from different handlers to main menu )
main_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="До головного меню📃", callback_data="main_menu")
        ]
    ]
)

# Cancel menu markup ( created for cancel FSM States )
cancel_inline = InlineKeyboardMarkup(
    inline_keyboard = [
        [
          InlineKeyboardButton(text="Відміна❌", callback_data="cancel")
        ]
    ]
)


# Administrator list objects menu ( function get "id" - id of organization  )
def create_admin_organization_list_markup(id):

    # Creating id numbers for next and priviouse objects
    forward = str(int(id) + 1)
    back = str(int(id) - 1)

    refactor_organization = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Редагувати📝", callback_data=f"refactor_organization:{id}")
            ],
            [
                InlineKeyboardButton(text="Видалити❌", callback_data=f"delete_organization:{id}")
            ],
            [
                InlineKeyboardButton(text="До головного меню📃", callback_data="main_menu")
            ],
            [
                InlineKeyboardButton(text="⏪ Назад", callback_data=f"back_organization:{back}"),
                InlineKeyboardButton(text="Вперел ⏩", callback_data=f"forward_organization:{forward}")
            ]

        ]
    )

    # Return edited markup
    return refactor_organization


# User list objects menu ( function get "id" - id of organization  )
def create_user_organization_list_markup(id):

    # Creating id numbers for next and priviouse objects
    forward = str(int(id) + 1)
    back = str(int(id) - 1)

    refactor_organization = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Додати нотатку✏️", callback_data=f"notion:{id}")
            ],
            [
                InlineKeyboardButton(text="Не показувати далі⛔", callback_data=f"not_show:{id}")
            ],
            [
                InlineKeyboardButton(text="До головного меню📃", callback_data="main_menu")
            ],
            [
                InlineKeyboardButton(text="⏪ Назад", callback_data=f"back_organization:{back}"),
                InlineKeyboardButton(text="Вперел ⏩", callback_data=f"forward_organization:{forward}")
            ]

        ]
    )

    # Return edited markup
    return refactor_organization


# Administrator refactoring menu ( function get "id" - id of organization  )
def create_refactor_list_markup(id):
    murkup = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Навза компанії", callback_data=f"ref:company_name:{id}")
            ],
            [
                InlineKeyboardButton(text="Код ЕДРПОУ", callback_data=f"ref:edrpoy_code:{id}")
            ],
            [
                InlineKeyboardButton(text="ПІБ контакної особи", callback_data=f"ref:cont_name:{id}")
            ],
            [
                InlineKeyboardButton(text="Телеофн контакної особи", callback_data=f"ref:cont_phone_number:{id}")
            ],
            [
                InlineKeyboardButton(text="Електрона пошта", callback_data=f"ref:email:{id}")
            ],
            [
                InlineKeyboardButton(text="Адреса компанії", callback_data=f"ref:adress:{id}")
            ],
            [
                InlineKeyboardButton(text="Показати/скрити введіть 0 або 1 (0 - показати, 1 - скрити)",
                                     callback_data=f"ref:is_checked:{id}")
            ],
            [
                InlineKeyboardButton(text="Нотатка", callback_data=f"ref:notion:{id}")
            ],
            [
                InlineKeyboardButton(text="До головного меню📃", callback_data="main_menu")
            ]
        ]
    )

    # Return edited markup
    return murkup