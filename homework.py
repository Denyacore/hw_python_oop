

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
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод строки сообщения."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60
    height: int = 1

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return(self.get_distance()
               / self.duration)

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
    coef_calorie_run_1: int = 18
    coef_calorie_run_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.coef_calorie_run_1
                * self.get_mean_speed()
                - self.coef_calorie_run_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coef_calorie_walk_1: float = 0.035
    coef_calorie_walk_2: int = 2
    coef_calorie_walk_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coef_calorie_walk_1
                * self.weight
                + (self.get_mean_speed()
                 ** self.coef_calorie_walk_2
                 // self.height)
                * self.coef_calorie_walk_3 * self.weight)
                * (self.duration
                * self.M_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    coef_callorie_swim_1: float = 1.1
    coef_callorie_swim_2: int = 2
    length_pool: int = 25

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 LEN_STEP: float = 1.38
                 ) -> None:
        super().__init__(action, duration, weight, LEN_STEP)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.coef_callorie_swim_1)
                * self.coef_callorie_swim_2
                * self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)


def read_package(workout_type: str, data: list):
    """Чтение данных."""
    my_dict: Dict[str, list] = {'SWM': Swimming,
                                'RUN': Running,
                                'WLK': SportsWalking}

    if workout_type in my_dict.keys():
        return (my_dict.get(workout_type)(*data))
    else:
        raise KeyError('Нет такой тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == 'main':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training=training)
