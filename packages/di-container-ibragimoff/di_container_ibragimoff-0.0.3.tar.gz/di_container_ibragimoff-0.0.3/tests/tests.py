from typing import Any, Callable
from di_container_ibragimoff.container import Container


class TestService:
    def __init__(self, c: Container):
        self.text = c.get('test')
        self.number = None

    def get_value(self):
        return self.text

    def set_number(self, val: int):
        self.number = val

    def get_number(self):
        return self.number


class TestFactory:
    def __init__(self, number):
        self.number = number

    def __call__(self, c: Container):
        test_service = TestService(c)
        test_service.set_number(self.number)
        return test_service


def test_container():
    container = Container()
    container.set('my_test_service', lambda c: TestService(c))
    container.set('test', lambda c: 'Example text')

    example_value = container.get('my_test_service').get_value()
    assert example_value == 'Example text'


def test_factory():
    container = Container()
    container.set('test', lambda c: 'Example text')

    factory = TestFactory(5)
    container.set('my_test_service', factory)

    service = container.get('my_test_service')
    assert service.get_value() == 'Example text'
    assert service.get_number() == 5


def set_number(c: Container, service: TestService) -> Any:
    service.set_number(c.get('number'))
    return service


def test_tagged_definitions():
    container = Container()

    container.set('test', lambda c: 'Example text')
    container.set('number', lambda c: 12)
    container.set('test_tagged_service', lambda c: TestService(c))

    container.set_tag('test_tagged_service', 'set_number_service')

    for id in container.find_ids_by_tag('set_number_service'):
        container.extends(id, set_number)

    assert container.get('number') == 12
    assert container.get('test_tagged_service').get_number() == 12
