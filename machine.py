from database import Category, Goods


class ConditionMachine:
    """Машина состояний"""

    def __init__(self):
        self.actual_page = None
        self.page_photo = None
        self.page_butt_name = None
        self.page_back_condition = None
        self.page_discription = None
        self.add_butt_back = None
        self.level_page = None
        self.user_id = None
        self.state_stack = []

    def get_context(self):
        context = {
            'actual_page': self.actual_page,
            'page_photo': self.page_photo,
            'page_butt_name': self.page_butt_name,
            'page_back_condition': self.page_back_condition,
            'level_page':  self.level_page,
            'state_stack': self.state_stack,
            'discription': self.page_discription,
            'add_butt_back': self.add_butt_back,
        }
        return context

    def start_page(self):
        """Параметры состояния стартовой страницы"""

        self.actual_page = 'start_page'
        self.page_photo = '457239027'
        self.page_butt_name = ['Выбор категорий']
        self.page_discription = None
        self.level_page = 1
        self.state_stack.append(self.actual_page)
        self.add_butt_back = False

    def categories_page(self):
        """Параметры состояния страницы с категориями"""

        self.page_butt_name = [category['name'] for category in Category.get_category()]
        self.page_photo = None
        self.page_back_condition = self.actual_page
        self.page_discription = None
        self.actual_page = 'category_page'
        self.level_page = 2
        self.state_stack.append(self.actual_page)
        self.add_butt_back = False

    def goods_page(self, category_name):
        """Параметры состояния страницы с товарами"""

        self.page_butt_name =\
            [good[0] for good in Goods.get_all_goods(category_name)]
        self.page_photo = None  # Category.get_category_photo(category_name)[0][0] <- Если надо какую-то фотку
        self.page_back_condition = self.actual_page
        self.page_discription = f'Представляю Вам раздел {category_name} нашей пекарни!' \
                                f' Выберите, понравившийся вариант.'
        self.actual_page = category_name
        self.level_page = 3
        self.state_stack.append(self.actual_page)
        self.add_butt_back = True

    def good_page(self, good_name):
        """Параметры состояния страницы карточки товара"""

        good = Goods.get_good_info(good_name)
        self.page_photo = good[0].photo
        self.page_back_condition = self.actual_page
        self.page_discription = f"{good[0].name}\n{good[0].description}"
        self.actual_page = good_name
        self.level_page = 4
        self.state_stack.append(self.actual_page)
        self.add_butt_back = True

    def go_back(self):
        """Логика кнопки 'назад'"""

        self.state_stack.pop()
        page_back = self.state_stack.pop()
        self.get_page_view(page_back)

    def get_page_view(self, status):
        """Перенаправление между состояниями"""

        level_page = len(self.state_stack)
        if status == 'Back':
            print('Back')
            self.go_back()
        elif level_page == 0:
            print('start start_page')
            self.start_page()
        elif level_page == 1:
            print('start categories_page')
            self.categories_page()
        elif level_page == 2:
            print('start goods_page')
            self.goods_page(status)
        elif level_page == 3:
            print('start good_page')
            self.good_page(status)
        return self.get_context()
