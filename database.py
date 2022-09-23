from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///test_bakery.db")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base(bind=engine)


class Category(Base):
    """Инициализируем таблицу категорий, описываем её и создаем необходимые методы"""

    __tablename__ = 'category'

    id = Column('id', Integer, primary_key=True)
    good = relationship('Goods', backref="category")
    name = Column('name', String(50), nullable=False)
    photo = Column('photo', String(50))

    def __repr__(self):
        return f'{self.name}'

    @classmethod
    def get_category(cls):
        return session.query(Category.name).all()  # Получаем все категории

    @classmethod
    def get_category_photo(cls, category_name):
        return session.query(Category.photo).filter_by(name=category_name).all()  # Получаем фотографии категорий

    @classmethod
    def get_all_category_name(cls):
        return session.query(Category.name).all()  # Получаем все названия категорий


class Goods(Base):
    """Инициализируем таблицу товаров, описываем её и создаем необходимые методы"""

    __tablename__ = 'goods'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    description = Column('description', String(250))
    photo = Column('photo', String(50))

    def __repr__(self):
        return f'{self.name}: категория {self.category_id}\n' \
               f'описание {self.description}\n' \
               f'идентификатор фото {self.photo}'

    @classmethod
    def get_all_goods(cls, category):
        return session.query(Goods.name).filter(Goods.category_id == session.query(Category.id).filter(
            Category.name == category).scalar_subquery()).all()  # Получаем все товары и имена категорий

    @classmethod
    def get_good_info(cls, good_name):
        return session.query(Goods).filter(Goods.name == good_name).all()  # Получаем описания товаров

    @classmethod
    def get_all_goods_name(cls):
        return session.query(Goods.name).all()  # Получаем все имена товаров


Base.metadata.create_all()
