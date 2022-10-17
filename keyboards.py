from telegram import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                      InlineKeyboardButton)
from faq_base import questions
ignore = r'''Рекомендуемые прививки|Частые вопросы|Связаться с врачом
|Начать заново|Отменить|RESTART|Рассчитать заново|Показать график|/help|В меню
'''
ignore_vaccine = r'''Рекомендуемые прививки|Частые вопросы|Связаться с врачом
|Начать заново|Отменить|RESTART|Показать график|/help'''
button_age = ['0-24 месяца', '2-17 лет', 'В меню']
choice_button = ['Рекомендуемые прививки', 'Частые вопросы',
                 'Связаться с врачом', 'В меню', 'Показать график',
                 'Рассчитать заново']
keyboard = [
        [InlineKeyboardButton(f"{questions[0]}", callback_data='1')],
        [InlineKeyboardButton(f"{questions[1]}", callback_data='2')],
        [InlineKeyboardButton(f"{questions[2]}", callback_data='3')],
        [InlineKeyboardButton(f"{questions[3]}", callback_data='4')],
        [InlineKeyboardButton(f"{questions[4]}", callback_data='5')],
        [InlineKeyboardButton(f"{questions[5]}", callback_data='6')],
        [InlineKeyboardButton(f"{questions[6]}", callback_data='7')],
        [InlineKeyboardButton(f"{questions[7]}", callback_data='8')],
        [InlineKeyboardButton("Вернуться в меню", callback_data='MENU')],
    ]
keyboard_menu_restart = [
        [InlineKeyboardButton("Отменить", callback_data='STOP'),
         InlineKeyboardButton("Спросить заново", callback_data='RESTART')],
        [InlineKeyboardButton("Вернуться в меню", callback_data='MENU')],
        ]

reply_keyboard = [
    ["Рекомендуемые прививки", "Частые вопросы"],
    ["Связаться с врачом", "Отменить"],
    ['Показать график']
]

reply_keyboard_link = [['Профиль вконтакте']]
reply_keyboard_exit = [['Отменить', 'Начать заново']]
reply_keyboard_vaccine = [['Отменить', 'Рассчитать заново'],
                          ['Показать график']]
markup_vaccine = ReplyKeyboardMarkup(reply_keyboard_vaccine,
                                     one_time_keyboard=True,
                                     resize_keyboard=True)
keyboard_infant_category = [['0-24 месяца', '2-17 лет'], ['В меню']]
keyboard_ages_child = [range(2, 10), range(10, 18), ['В меню']]
keyboard_ages_infant = [range(1, 13), range(13, 25), ['В меню']]
markup_age_infant = ReplyKeyboardMarkup(keyboard_ages_infant,
                                        one_time_keyboard=True,
                                        resize_keyboard=True)
markup_age_child = ReplyKeyboardMarkup(keyboard_ages_child,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
markup_category = ReplyKeyboardMarkup(keyboard_infant_category,
                                      one_time_keyboard=True,
                                      resize_keyboard=True)
markup_menu = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                  resize_keyboard=True)
markup_link = ReplyKeyboardMarkup(reply_keyboard_link, one_time_keyboard=True,
                                  resize_keyboard=True)
markup_exit = ReplyKeyboardMarkup(reply_keyboard_exit, one_time_keyboard=True,
                                  resize_keyboard=True)
inline_markup = InlineKeyboardMarkup(keyboard)
inline_markup_menu_faq = InlineKeyboardMarkup(keyboard_menu_restart)
