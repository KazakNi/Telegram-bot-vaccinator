from cgitb import text
from dotenv import load_dotenv
from faq_base import faq, questions
from keyboards import (
    choice_button,
    markup_age_child,
    markup_age_infant,
    markup_category,
    ignore,
    ignore_vaccine,
    button_age,
    markup_menu,
    markup_vaccine,
    markup_exit,
    inline_markup,
    inline_markup_menu_faq
)
import logging
import os
import sys
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler,
                          Updater)
from telegram import ReplyKeyboardRemove, ParseMode, Sticker, Update
from utils import vaccine_schedule


load_dotenv()

mylogger = logging.getLogger("telegram_bot")

formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(name)s,'
                              '%(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
mylogger.addHandler(handler)
mylogger.setLevel(logging.DEBUG)

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
CHOOSING, AGE, VACCINE, FAQ = range(4)


def start(update: Update, context: CallbackContext):
    mylogger.info('Бот запущен')
    user = update.message.from_user
    update.message.reply_text(f"Здравствуйте, {user['first_name']}! "
                              "Вас приветствует бот-помощник по "
                              "вакцинопрофилактике, пожалуйста, "
                              "выберите интересующий вопрос. 😊",
                              reply_markup=markup_menu)
    return CHOOSING


def help(update: Update, context: CallbackContext):
    update.message.reply_text('Справка:\nВся информация от бота носит '
                              'ориентировочный характер и не является '
                              'врачебным предписанием, для дальнейшей '
                              'консультации с врачом Вы можете '
                              'воспользоваться '
                              'кнопкой связи в меню.\nV1 — первый компонент '
                              'вакцины\nV2 — второй\nV3 — третий'
                              '\nRV1 — первый компонент ревакцинации.\nRV2 —'
                              'второй\nRV3 — третий')
    return CHOOSING


def choice_action(update: Update, context: CallbackContext):
    if update.message.text.lower() in ['рекомендуемые прививки',
                                       'рассчитать заново']:
        update.message.reply_text("Укажите возрастную категорию ребёнка",
                                  reply_markup=markup_category)
        return AGE
    elif update.message.text.lower() in ['частые вопросы']:
        update.message.reply_text('Пожалуйста, выберите интересующий '
                                  'Вас номер вопроса:',
                                  reply_markup=inline_markup)
        return FAQ
    elif update.message.text.lower() in ['связаться с врачом']:
        update.message.reply_text(text='<a href="https://vk.com/i.ulybayas">'
                                       'Любовь Казакова</a>',
                                       parse_mode=ParseMode.HTML,
                                       reply_markup=markup_menu)
    elif update.message.text.lower() in ['показать график']:
        try:
            update.message.reply_photo(photo=open('graph.png', 'rb'),
                                       reply_markup=markup_menu)
        except Exception as error:
            mylogger.critical(f'Не удалось отправить фото {error}.')
            update.message.reply_text('К сожалению, фото графика недоступно на'
                                      'данный момент, администратор уведомлен'
                                      'о проблеме.')
            context.bot.send_message(chat_id=CHAT_ID,
                                     text='Внимание! Пользователь не смог'
                                          'загрузить фото графика.',
                                          reply_markup=markup_menu)
            return CHOOSING
    return CHOOSING


def clarify_question(update: Update, context: CallbackContext):
    update.message.reply_text('Простите, сообщение не распознано, пожалуйста, '
                              'выберите опцию меню', reply_markup=markup_menu)
    mylogger.warning(f'Ввод пользователя не распознан: {update.message.text}')
    return CHOOSING


def age_category(update: Update, context: CallbackContext):
    '''Уточнение возрастной категории для получения списка прививок.'''
    context.user_data['age_dimension'] = update.message.text
    if update.message.text.lower() in '0-23 месяца':
        update.message.reply_text('Выберите возраст',
                                  reply_markup=markup_age_infant)
        return VACCINE
    elif update.message.text.lower() in '2-17 лет':
        update.message.reply_text('Выберите возраст',
                                  reply_markup=markup_age_child)
        return VACCINE
    elif update.message.text.lower() in 'в меню':
        update.message.reply_text('Пожалуйста, выберите интересующий '
                                  'Вас вопрос',
                                  reply_markup=markup_menu)
        return CHOOSING
    else:
        update.message.reply_text('Пожалуйста, выберите из предлагаемого '
                                  'диапазона', reply_markup=markup_category)
        return AGE


def result(update: Update, context: CallbackContext):
    '''Функция обращается к базе данных и выдает рекомендуемый список вакцин'''
    ''' к определённому возрасту.'''

    if update.message.text.lower() in 'в меню':
        update.message.reply_text("Пожалуйста, выберите интересующий вопрос",
                                  reply_markup=markup_menu)
        return CHOOSING
    import re
    regex = re.compile('^[0-9]')
    result = regex.match(update.message.text)
    age_dimension = context.user_data['age_dimension']
    if not result and age_dimension in '0-23 месяца':
        update.message.reply_text('Пожалуйста, введите число месяцев',
                                  reply_markup=markup_age_infant)
        return VACCINE
    if not result and age_dimension in '2-17 лет':
        update.message.reply_text('Пожалуйста, введите число лет',
                                  reply_markup=markup_age_child)
        return VACCINE
    elif age_dimension in '0-23 месяца' and int(update.message.text) > 24:
        update.message.reply_text('Пожалуйста, введите целое число до 2',
                                  reply_markup=markup_exit)
        return VACCINE
    elif age_dimension in '2-17 лет' and int(update.message.text) > 17:
        update.message.reply_text('Пожалуйста, введите целое число до 17'
                                  'включительно', reply_markup=markup_exit)
        return VACCINE
    context.user_data['age'] = update.message.text
    age = context.user_data['age']
    update.message.reply_text(f"{vaccine_schedule(age, age_dimension)}",
                              reply_markup=markup_vaccine,
                              parse_mode=ParseMode.HTML)
    return CHOOSING


def faq_answer(update: Update, context: CallbackContext):
    '''Callbackquery по словарю вытаскивает ответы на популярные вопросы.'''

    query = update.callback_query
    if str(update.callback_query.data) in ('RESTART'):
        query.message.edit_text('Пожалуйста, выберите интересующий Вас номер '
                                'вопроса:', reply_markup=inline_markup)
        return FAQ
    if str(update.callback_query.data) in ('MENU'):
        query.message.reply_text('Пожалуйста, выберите интересующий Вас '
                                 'вопрос:', reply_markup=markup_menu)
        return CHOOSING
    else:
        answer_num = query.data
        query.answer()
        query.edit_message_text(text=f'\nВопрос №'
                                     f'<b>{questions[int(answer_num)-1]}</b>\n'
                                     f'\nОтвет: {faq[answer_num]}',
                                reply_markup=inline_markup_menu_faq,
                                parse_mode=ParseMode.HTML)
        return FAQ


def cancel(update: Update, context: CallbackContext):
    """Завершение беседы, очистка клавиатуры."""

    remove_keyboard = ReplyKeyboardRemove()
    query = update.callback_query
    if query:
        user = query.from_user
        query.message.reply_text(f'До свидания, {user["first_name"]}, '
                                 'хорошего дня 😊!', 
                                 reply_markup=remove_keyboard)
    else:
        user = update.message.from_user
        update.message.reply_text(f'До свидания, {user["first_name"]},'
                                  'хорошего дня! 😊',
                                  reply_markup=remove_keyboard)
    mylogger.info('Пользователь завершил беседу')
    return ConversationHandler.END


def secret_word(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_message.chat_id,
                             text='Чат-бот разработан Казаковым Никитой.\n'
                             'Протестирован Пархоменко Владом, спасибо ему :)')

    context.bot.send_sticker(chat_id=update.effective_message.chat_id,
                             sticker='https://cdn.tlgrm.app/stickers/a9a/146'
                             '/a9a1468d-6946-37c0-a1a6-13ed601a8685/192/1.webp'
                             )


handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), 
                      MessageHandler(Filters.text('Начать заново'), start)],
        states={
            CHOOSING: [MessageHandler(Filters.text(choice_button),
                                      choice_action),
                       MessageHandler(Filters.regex(fr'[^{ignore}]'),
                                      clarify_question),
                       CallbackQueryHandler(choice_action,
                                            pattern='^[^MENU]')],
            AGE: [MessageHandler(Filters.text(button_age) |
                                 Filters.regex(r'\w'), age_category)],
            VACCINE: [MessageHandler(Filters.regex(r'\d'), result),
                      MessageHandler(Filters.regex(fr'[^{ignore_vaccine}]'),
                                     result)],
            FAQ: [
                CallbackQueryHandler(faq_answer, pattern='^[^STOP]'),
                CallbackQueryHandler(faq_answer, pattern='^' +
                                     str('RESTART') + '$'),
                MessageHandler(Filters.text(choice_button), choice_action),
                MessageHandler(Filters.regex(fr'[^{ignore}]'),
                               clarify_question)],
                },
        fallbacks=[MessageHandler(Filters.regex("Отменить"), cancel),
                   CallbackQueryHandler(cancel, pattern='^' + str('STOP')
                   + '$')], allow_reentry=True
      )


def main() -> None:
    """Start the bot."""
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^Разработчик'),
                                          secret_word))
    dispatcher.add_handler(handler)
    dispatcher.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
