"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_journal():
    return Product("journal", 50, "This is a journal", 2000)


@pytest.fixture
def cart():
    cart = Cart()
    cart.products = {}
    return cart


@pytest.fixture
def cart_with_products(product, product_journal):
    cart = Cart()
    cart.add_product(product, 500)
    cart.add_product(product_journal, 400)
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(0) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

        # TODO напишите проверки на метод buy

    def test_product_buy_less_than_available(self, product):
        initial_quantity = product.quantity
        product.buy(100)
        assert product.quantity == initial_quantity - 100

    def test_product_buy_equal_to_available(self, product):
        initial_quantity = product.quantity
        product.buy(1000)
        assert product.quantity == initial_quantity - 1000

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_empty_cart(self, cart, product):
        assert len(cart.products) == 0
        cart.add_product(product, 1)
        assert cart.get_product_quantity(product) == 1
        assert cart.get_products_count() == 1

    def test_add_product_not_empty_cart(self, cart, product):
        cart.products = {
            product: 1
        }
        assert cart.products[product] == 1
        cart.add_product(product, 2)
        assert cart.get_product_quantity(product) == 3
        assert cart.get_products_count() == 1

    def test_remove_product_without_remove_count(self, cart, product):
        cart.products = {
            product: 1
        }
        assert cart.get_product_quantity(product) == 1
        cart.remove_product(product)
        assert cart.get_products_count() == 0

    def test_remove_product_more_then_remove_count(self, cart, product):
        cart.products = {
            product: 2
        }
        assert cart.get_product_quantity(product) == 2
        cart.remove_product(product, 3)
        assert cart.get_products_count() == 0

    def test_remove_product_less_then_remove_count(self, cart, product):
        cart.products = {
            product: 8
        }
        assert cart.get_product_quantity(product) == 8
        cart.remove_product(product, 4)
        assert cart.get_product_quantity(product) == 4

    def test_remove_product_equal_remove_count(self, cart, product):
        cart.products = {
            product: 35
        }
        assert cart.get_product_quantity(product) == 35
        cart.remove_product(product, 35)
        assert cart.get_products_count() == 0

    def test_clear_cart(self, cart, product):
        cart.products = {
            product: 35
        }
        assert cart.products[product] == 35
        cart.clear()
        assert cart.get_products_count() == 0

    def test_get_total_price_cart(self, cart, cart_with_products):
        assert cart.get_total_price() == 0.0
        assert cart_with_products.get_total_price() == 70000

    def test_buy_product(self, cart, product):
        cart.add_product(product, 50)
        cart.buy()
        assert product.quantity == 950
        assert len(cart.products) == 0

    def test_buy_product_more_than_quantity(self, cart, product):
        cart.add_product(product, 1500)
        with pytest.raises(ValueError):
            assert cart.buy()
