from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '    # строка
        'Дистанция: {distance:.3f} км; '       # сообщения
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод строки сообщения."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int   # кол-во выполненных движений
    duration: float   # длительность тренировки
    weight: float   # вес
    LEN_STEP: float = 0.65   # длина 1 шага
    M_IN_KM: int = 1000   # длинна км(м)
    M_IN_HOUR: int = 60   # минут в часе
    height: int = 1

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)   # формула расчета дистанции

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return(self.get_distance()
               / self.duration)   # формула ср. скор.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    action: int
    duration: float
    weight: float
    coef_calorie_run_1: int = 18   # коэффициент каллорий при беге 1
    coef_calorie_run_2: int = 20   # коэффициент каллорий при беге 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.coef_calorie_run_1           # формула
                * self.get_mean_speed()            # потраченных
                - self.coef_calorie_run_2)         # каллорий
                * self.weight / self.M_IN_KM       # при
                * self.duration * self.M_IN_HOUR   # беге
                )


class SportsWalking(Training):   # создание дочернего класса
    """Тренировка: спортивная ходьба."""

    coef_calorie_walk_1: float = 0.035   # коэффициент каллорий при ходьбе 1
    coef_calorie_walk_2: int = 2         # коэффициент каллорий при ходьбе 2
    coef_calorie_walk_3: float = 0.029   # коэффициент каллорий при ходьбе 3

    def __init__(self,   # конструктор класса-наследника
                 action: int,      #
                 duration: float,  # аргументы
                 weight: float,    # конструктора
                 height: float     #
                 ) -> None:
        super().__init__(action, duration, weight)   # наследование
        self.height = height   # добавление нового свойства

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coef_calorie_walk_1
                * self.weight
                + (self.get_mean_speed()
                 ** self.coef_calorie_walk_2
                 // self.height)  # формула каллорий
                * self.coef_calorie_walk_3 * self.weight)
                * (self.duration
                * self.M_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # длинна гребка(м)
    coef_callorie_swim_1: float = 1.1  # коэффициент каллорий при плавании 1
    coef_callorie_swim_2: int = 2  # коэффициент каллорий при плавании 2
    length_pool: int = 25

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 LEN_STEP: float = 1.38
                 ) -> None:
        super().__init__(action, duration, weight, LEN_STEP)  # наследование
        self.length_pool: int = length_pool  # свойство длинны бассейна
        self.count_pool: int = count_pool  # переплываний бассейна

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()        # формула
                + self.coef_callorie_swim_1)  # каллорий
                * self.coef_callorie_swim_2
                * self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool   # формула
                * self.count_pool  # средней скорости
                / self.M_IN_KM     # при плавании
                / self.duration)


def read_package(workout_type: str, data: list):
    """Чтение данных."""
    my_dict: Dict[str, list] = {'SWM': Swimming,            # словарь
                                'RUN': Running,             # с
                                'WLK': SportsWalking}       # данными

    if workout_type in my_dict.keys():
        return (my_dict.get(workout_type)(*data))
    else:
        raise KeyError('Нет такой тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()  # сохранение объекта в переменную
    print(info.get_message())  # вывод сообщения о тренировке


if __name__ == 'main':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training=training)
