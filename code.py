import random
from typing import List, Tuple, Optional

CELL_DESIGN = {
    "empty": "▢",
    "tank": "▣",
    "miss": "◼",
    "hit": "✘"
}


class Tank:

    def __init__(self, rows: Tuple[int, int], column: int) -> None:
        self.rows = rows
        self.column = column


class Shot:

    def __init__(self, row: int, column: int, hit: bool = False) -> None:
        self.row = row
        self.column = column
        self.hit = hit


class Field:

    def __init__(self) -> None:
        self.data = [[CELL_DESIGN["empty"] for _ in range(10)] for _ in range(10)]
        self.tanks: List[Tank] = []
        self.shots: List[Shot] = []

    def place_tank(self, tank: Tank) -> bool:
        """

        Пытается разместить танк

        Args:
            tank (Tank): Танк для размещения

        Returns:
            bool: True если танк размещен, False - не

        """
        if self.is_valid_placement(tank):
            self.tanks.append(tank)
            return True
        return False

    def is_valid_placement(self, tank: Tank) -> bool:
        """

        Проверяет, можно ли разместить танк на поле

        Args:
            tank (Tank): Танк для проверки

        Returns:
            bool: True если норм, False если не

        """

        if tank.rows[1] - tank.rows[0] != 1:
            return False

        for r in range(tank.rows[0], tank.rows[1] + 1):
            if not (0 <= r < 10) or not (0 <= tank.column < 10):
                return False

        for existing in self.tanks:
            for r in range(tank.rows[0], tank.rows[1] + 1):
                if (abs(r - existing.rows[0]) <= 1 and
                        abs(tank.column - existing.column) <= 1):
                    return False
        return True

    def receive_shot(self, row: int, col: int) -> bool:
        """

        Обрабатывает выстрел по полю

        Args:
            row (int): Номер строки выстрела
            col (int): Номер столбца выстрела

        Returns:
            bool: True есть, False если промах

        """

        # Проверяем, не было ли уже выстрела в эту клетку
        for shot in self.shots:
            if shot.row == row and shot.column == col:
                raise ValueError("Повторный выстрел в ту же клетку")

        # Остальная логика...
        for tank in self.tanks:
            if col == tank.column and row in tank.rows:
                self.shots.append(Shot(row, col, hit=True))
                return True

        self.shots.append(Shot(row, col, hit=False))
        return False
    def destroyed_tanks(self) -> bool:
        """

        Проверяет, все ли танки на поле уничтожены

        Returns:
            bool: True если да, False если нет

        """
        if not self.tanks:  # Если нет танков
            return True

        for tank in self.tanks:
            tank_destroyed = all(
                any(shot.row == row and shot.column == tank.column and shot.hit
                    for shot in self.shots)
                for row in tank.rows
            )
            if not tank_destroyed:
                return False
        return True

    def fill_field(self) -> None:
        """Обновляет представление поля"""
        self.data = [[CELL_DESIGN["empty"] for _ in range(10)] for _ in range(10)]
        for tank in self.tanks:
            for row in tank.rows:
                self.data[row][tank.column] = CELL_DESIGN["tank"]
        for shot in self.shots:
            self.data[shot.row][shot.column] = (
                CELL_DESIGN["hit"] if shot.hit else CELL_DESIGN["miss"]
            )

    def display(self) -> None:
        """Выводит поле в консоль"""
        self.fill_field()
        print("   А Б В Г Д Е Ж З И К")
        for i, row in enumerate(self.data):
            print(f"{i + 1:2} {' '.join(row)}")


class Game:

    def __init__(self) -> None:
        self.computer_c = 10
        self.player_field = Field()
        self.computer_field = Field()
        self.last_hit: Optional[Tuple[int, int]] = None
        self.current_player = "player"

    def start(self) -> None:
        """Запускает игру"""
        print(" === Танковое сражение === ")
        self.setup_player_tanks()
        self.setup_computer_tanks()
        self.play()
        self.computer_c = 10

    def setup_player_tanks(self) -> None:
        """Расстановка танков для игрока"""
        print("Расставьте 10 танков (10 принимается за 0)(формат: А1А2 Б3Б4 В5В6 ...):")
        while True:
            try:
                coords = input("> ").upper().split()
                tanks = self.parse_tank_coords(coords)
                if len(tanks) != 10:
                    raise ValueError(f"Нужно 10 танков, а введено {len(tanks)}")
                self.player_field.tanks.clear()
                for tank in tanks:
                    if not self.player_field.place_tank(tank):
                        raise ValueError("Некорректная расстановка!")
                break
            except ValueError as a:
                print(f"Ошибка: {a}. Попробуйте ещё раз.")

    #@staticmethod
    def parse_tank_coords(self, coords: List[str]) -> List[Tank]:
        """

        Преобразует строки координат в объекты Tank

        Args:
            coords (List[str]): Список строк с координатами танков

        Returns:
            List[Tank]: Список объектов Tank

        Raises:
            ValueError: Если формат координат неверный

        """
        tanks = []
        russian_letters = 'АБВГДЕЖЗИК'

        for coord in coords:
            if len(coord) not in (4, 5):  # Формат А1А2 или А10А10
                raise ValueError(f"Неправильный формат: {coord}")

            # Разбор координат
            col1 = coord[0]
            num_part = coord[1:]

            # Обработка формата А10А9
            if len(coord) == 5:
                if coord[1:3] != '10':
                    raise ValueError(f"Неправильный номер строки: {coord}")
                num1 = '10'
                col2 = coord[3]
                num2 = coord[4]
            else:  # Формат А1А2
                num1 = coord[1]
                col2 = coord[2]
                num2 = coord[3]

            # Проверка букв
            if col1 not in russian_letters or col2 not in russian_letters:
                raise ValueError(f"Используйте русские буквы от А до К: {coord}")

            # Преобразование номеров строк
            try:
                col1_num = int(num1) - 1  # "1" → 0, "10" → 9
                col2_num = int(num2) - 1
            except ValueError:
                raise ValueError(f"Неправильный номер строки: {coord}")

            # Проверка диапазона
            if not (0 <= col1_num <= 9) or not (0 <= col2_num <= 9):
                raise ValueError(f"Номера строк должны быть от 1 до 10: {coord}")

            # Проверка вертикальности и соседства
            if russian_letters.index(col1) != russian_letters.index(col2):
                raise ValueError(f"Танк должен быть вертикальным: {coord}")
            if abs(col1_num - col2_num) != 1:
                raise ValueError(f"Танк должен занимать две соседние клетки: {coord}")

            tanks.append(Tank(
                (min(col1_num, col2_num), max(col1_num, col2_num)),
                russian_letters.index(col1)
            ))

        return tanks

    def setup_computer_tanks(self) -> None:
        """Случайным образом расставляет танки компьютера"""
        attempts = 0
        max_global_attempts = 3

        while attempts < max_global_attempts:
            self.computer_field = Field()
            success = True

            for _ in range(10):
                placed = False
                for _ in range(100):
                    col = random.randint(0, 9)
                    row1 = random.randint(0, 8)
                    tank = Tank((row1, row1 + 1), col)
                    if self.computer_field.place_tank(tank):
                        placed = True
                        break

                if not placed:
                    success = False
                    break

            if success:
                return

            attempts += 1
            print(f"Попытка {attempts}: не удалось разместить танки, пробуем ещё раз...")

        raise RuntimeError("Компьютер не смог расставить танки после нескольких попыток")

    def play(self) -> None:
        """Основной игровой цикл"""
        while True:
            if self.check_win():  # Проверка в начале каждого хода
                break

            print("\nКоманды: 'выход' - завершить игру, 'помощь' - показать справку")
            print("\n        ВАШЕ поле - слева,                       поле ИИ - справа")
            self.print_combined_fields()

            if self.current_player == "player":
                self.player_turn()
            else:
                self.computer_turn()

    def print_combined_fields(self) -> None:
        """Выводит оба поля рядом"""
        # letters = "  ".join(["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"])
        # print(f"   {letters}      {letters}")
        print("   А   Б  В  Г   Д  Е  Ж   З  И   К      А   Б  В  Г   Д  Е  Ж   З  И   К")

        self.player_field.fill_field()
        self.computer_field.fill_field()

        for i in range(10):
            player_row = "  ".join(self.player_field.data[i])
            computer_row = []
            for j in range(10):
                cell = self.computer_field.data[i][j]
                if cell in (CELL_DESIGN["hit"], CELL_DESIGN["miss"]):
                    computer_row.append(cell)
                else:
                    computer_row.append(CELL_DESIGN["empty"])

            line = f"{i + 1:2} {player_row}   {i + 1:2} {'  '.join(computer_row)}"
            print(line)

    def player_turn(self) -> None:
        """Обрабатывает ход игрока"""
        while True:
            try:
                print(f"Противника кол-во кораблей: {self.computer_c}")
                coord = input("Ваш выстрел: ").upper().strip()
                if coord == "ВЫХОД":
                    if input("Точно выйти? (да/нет): ").lower() == "да":
                        print("Игра завершена")
                        exit()
                    continue

                if  3 < len(coord) < 2 or not coord[0].isalpha() or not coord[1:].isdigit() :
                    raise ValueError("Неверный формат")

                col_char = coord[0]
                row_num = int(coord[1:])

                if col_char not in 'АБВГДЕЖЗИК':
                    raise ValueError("Буква должна быть от А до К (без Ё)")

                if not 1 <= row_num <= 10:
                    raise ValueError("Номер строки должен быть от 1 до 10")

                col = 'АБВГДЕЖЗИК'.index(col_char)
                row = row_num - 1

                if any(s.row == row and s.column == col
                       for s in self.computer_field.shots):
                    print("Вы уже стреляли сюда!")
                    continue

                hit = self.computer_field.receive_shot(row, col)

                if hit:
                    self.print_combined_fields()
                    print("Попадание!")
                    for tank in self.computer_field.tanks:
                        if col == tank.column and row in tank.rows:
                            if all(any(s.row == r and s.column == col and s.hit
                                       for s in self.computer_field.shots)
                                   for r in tank.rows):
                                print("Танк противника уничтожен!")
                                self.computer_c -= 1
                else:
                    self.print_combined_fields()
                    print("Мимо!")
                    self.current_player = "computer"
                    break

            except ValueError as e:
                print(f"Ошибка: {e}. Пример ввода: А1")

    def computer_turn(self) -> None:
        """Обрабатывает ход компьютера"""
        if self.last_hit:
            row, col = self.get_next_target()
        else:
            row, col = self.get_random_target()

        hit = self.player_field.receive_shot(row, col)
        col_char = 'АБВГДЕЖЗИК'[col]

        if hit:
            print(f"Компьютер попал в {col_char}{row + 1}!")
            self.last_hit = (row, col)
            if not self.player_field.destroyed_tanks():
                self.computer_turn()
        else:
            print(f"Компьютер выстрелил в {col_char}{row + 1}, но промахнулся")
            self.last_hit = None
            self.current_player = "player"

    def get_random_target(self) -> Tuple[int, int]:
        """

        Выбирает случайную цель для компьютера

        Returns:
            Tuple[int, int]: Координаты (строка, столбец) цели

        """
        # Создаём список всех возможных клеток
        available = []
        for row in range(10):
            for col in range(10):
                # Проверяем, не стреляли ли уже сюда
                cell_clear = True
                for shot in self.player_field.shots:
                    if shot.row == row and shot.column == col:
                        cell_clear = False
                        break

                if cell_clear:
                    available.append((row, col))

        if not available:
            raise RuntimeError("Не осталось клеток для выстрела!")

        return random.choice(available)

    def get_next_target(self) -> Tuple[int, int]:
        """

        Выбирает цель для компьютера после попадания.

        Returns:
            Tuple[int, int]: Координаты (строка, столбец) цели

        """
        last_row, last_col = self.last_hit

        for dr in [-1, 1]:
            new_row = last_row + dr
            if 0 <= new_row < 10:
                if not any(s.row == new_row and s.column == last_col
                           for s in self.player_field.shots):
                    return new_row, last_col

        for dc in [-1, 1]:
            new_col = last_col + dc
            if 0 <= new_col < 10:
                if not any(s.row == last_row and s.column == new_col
                           for s in self.player_field.shots):
                    return last_row, new_col

        return self.get_random_target()

    def check_win(self) -> bool:
        """

        Проверяет условия победы и управляет завершением игры

        Returns:
            bool: True если игра окончена, False если игра продолжается

        """
        if self.computer_field.destroyed_tanks():
            self.print_combined_fields()
            print("Вы победили! Все танки компьютера уничтожены!")
            return True

        if self.player_field.destroyed_tanks():
            self.print_combined_fields()
            print("Компьютер выйграл! Все ваши танки уничтожены!")
            return True

        return False

if __name__ == "__main__":
    while True:
        game = Game()
        game.start()
        if input("Сыграть ещё раз? (да/нет): ").lower() != 'да':
            print("Спасибо за игру!")
            break