import unittest

from machine import ConditionMachine
from database import Goods, Category


class TestMachine(unittest.TestCase):
    """
        Тест машины: пробегаемся по списку туда и обратно + тестим запросы в БД
    """

    def test_all_rout(self):
        rout_map = [('start', 1),
                    ('categories_page', 2),
                    ('pizza', 3),
                    ('Маргарита', 4),
                    ('Back', 3),
                    ('Back', 2),
                    ('Back', 1)]
        test_machine = ConditionMachine()
        for message, level_page in rout_map:
            test_machine.get_page_view(message)
            self.assertEqual(test_machine.level_page, level_page)


class TestGoodsTable(unittest.TestCase):
    """
        Проверяем основные запросы к БД таблицы Goods.
        Нобходимо, чтобы БД была минмально заполнена: одна категория(pizza)
        и один товар(Маргарита)
    """
    def test_goods_parameters(self):
        self.assertNotEqual(len(Goods.get_all_goods_name()), 0)
        self.assertEqual(type(Category.get_category_photo('pizza')[0][0]), str)
        good_info = Goods.get_good_info('Маргарита')
        self.assertEqual(good_info[0].id, 1)
        self.assertEqual(type(good_info[0].description), str)
        self.assertIsNotNone(good_info[0].description)
        self.assertIsNotNone(good_info[0].category_id)
        self.assertIsNotNone(good_info[0].photo)
