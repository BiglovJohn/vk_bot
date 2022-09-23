from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from machine import ConditionMachine
from database import Category, Goods

from env import *


def generate_keyboard(get_db_info, add_butt=None):
    """Генерируем клавиатуру в зависимости от состояния"""

    keyboard = VkKeyboard(one_time=True, inline=False)
    if type(get_db_info) == str:
        keyboard.add_button(
            label=get_db_info,
            color=VkKeyboardColor.POSITIVE,
            payload={"type": 'click'}
        )
    else:
        for item in get_db_info:
            keyboard.add_button(
                label=item,
                color=VkKeyboardColor.POSITIVE,
                payload={"type": 'click'}
            )
    if add_butt:
        if add_butt['add_butt_back']:
            keyboard.add_button(
                "Back",
                color=VkKeyboardColor.NEGATIVE,
                payload={"type": "back"},
            )
    return keyboard


def start_page_send(act, vk, condition):
    """Создаем приветственное сообщение при старте бота + кнопка 'Выбор категорий'"""

    photo = condition['page_photo']
    vk.messages.send(
        user_id=act.obj.message["from_id"],
        random_id=get_random_id(),
        peer_id=act.obj.message["from_id"],
        keyboard=generate_keyboard('Выбор категорий').get_keyboard(),
        attachment=f'photo-{ENV.GROUP_ID}_{photo}',
        message="Добро пожаловать в нашу пекарню!",
    )


def page_view(event, vk, condition, butt_back=False):
    """
        Генерим сообщения и набора кнопок в зависимости от состояния:
            - информационное сообщение + список кнопок с категориями меню
            - информационное сообщение + список кнопок с товарами + кнопка 'назад'
            - карточка товара + кнопка 'назад'
    """

    photo = condition['page_photo']
    discription = 'Я Бот-витрина и с удовольствием продеманстрирую Вам всё, что у нас есть! Для этого Вам нужно ' \
                  'выбрать интересующую Вас категорию из списка ниже.'
    if condition['discription'] is not None:
        discription = condition['discription']

    if condition['level_page'] == 4:  # Убираем лишние кнопки на нижнем уровне меню
        vk.messages.send(
            user_id=event.obj.message["from_id"],
            random_id=get_random_id(),
            peer_id=event.obj.message["from_id"],
            keyboard=generate_keyboard([], condition).get_keyboard(),
            attachment=f'photo-{ENV.GROUP_ID}_{photo}',
            message=discription
        )
    else:
        vk.messages.send(
            user_id=event.obj.message["from_id"],
            random_id=get_random_id(),
            peer_id=event.obj.message["from_id"],
            keyboard=generate_keyboard(condition['page_butt_name'],
                                       condition).get_keyboard(),
            attachment=f'photo-{ENV.GROUP_ID}_{photo}',
            message=discription
        )


def main():
    """Функция для определения основной логики"""

    vk_session = VkApi(token=ENV.TOKEN, api_version=ENV.API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=ENV.GROUP_ID)
    user = ConditionMachine()
    all_valid_name = Category.get_all_category_name() + Goods.get_all_goods_name() + ['Back', 'Выбор категорий']

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj.message["text"]
            if message == "start":
                user.state_stack = []
                user.user_id = event.obj.message['from_id']
                condition = user.get_page_view('start')
                start_page_send(event, vk, condition)
            elif message in all_valid_name[0] or all_valid_name:
                condition = user.get_page_view(message)
                page_view(event, vk, condition)


if __name__ == "__main__":
    main()
