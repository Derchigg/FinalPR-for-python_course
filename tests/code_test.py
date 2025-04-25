import pytest
from code import Field, Tank, Game

@pytest.fixture
def empty_field():
    return Field

@pytest.fixture
def game_with_tanks():
    """Просто самые первоначальные данные"""
    game = Game()
    game.player_field.tanks = [Tank((0, 1), 0), Tank((5, 6), 3)]
    game.computer_field.tanks = [Tank((2, 3), 1), Tank((7, 8), 4)]
    return game

# Тест размещения танка
def test_tank_placement(empty_field):
    """Проверка корректного размещения танка"""
    tank = Tank((0, 1), 0)
    assert empty_field.place_tank(tank) is True
    assert len(empty_field.tanks) == 1

# Тест на пересечение танков
def test_invalid_placement(empty_field):
    """Проверка обработки пересечения танков"""
    tank1 = Tank((0, 1), 0)
    tank2 = Tank((1, 2), 0)  # Пересекается с tank1
    empty_field.place_tank(tank1)
    assert empty_field.place_tank(tank2) is False
