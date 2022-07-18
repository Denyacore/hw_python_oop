class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,   # конструктор класса
                 training_type: str,          #
                 duration: float,             #
                 distance: float,             # аргументы класса
                 speed: float,                #
                 calories: float) -> None:    #
        self.training_type = training_type       #
        self.duration = duration                 # свойства
        self.distance = distance                 # конструктора
        self.speed = speed                       #
        self.calories = calories                 #

    def get_message(self) -> str:   # метод возврата строки сообщения
        info = (f'Тип тренировки: {self.training_type}; '    #
                f'Длительность: {self.duration:.3f} ч.; '    # строка
                f'Дистанция: {self.distance:.3f} км; '       # сообщения
                f'Ср. скорость: {self.speed:.3f} км/ч; '     #
                f'Потрачено ккал: {self.calories:.3f}.')     #
        return info   # возврат строки сообщения


class Training:   # создание родительского класса
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65   # длинна шага(м)
    M_IN_KM: int = 1000   # длинна км(м)
    M_IN_HOUR: int = 60   # минут в часе
    training_type: str = ''   # код тренировки

    def __init__(self,   # конструктор родительского класса
                 action: int,   # кол-во выполненных движений
                 duration: float,   # длительность тренировки
                 weight: float,   # вес
                 LEN_STEP: float = 0.65   # длина 1 шага
                 ) -> None:
        self.action = action                 # свойства
        self.duration = duration             #
        self.weight = weight                 #
        self.LEN_STEP: float = LEN_STEP      # конструктора

    def get_distance(self) -> float:   # метод получения дистанции
        """Получить дистанцию в км."""

        distance: float = (self.action
                           * self.LEN_STEP
                           / self.M_IN_KM)   # формула расчета дистанции
        return distance   # возврат значения дистанции

    def get_mean_speed(self) -> float:   # метод получения средней скорости
        """Получить среднюю скорость движения."""

        speed: float = (self.get_distance()
                        / self.duration)   # формула ср. скор.
        return speed   # возврат значения скорости

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,      #
                                   self.duration,                # свойства
                                   self.get_distance(),          # класса
                                   self.get_mean_speed(),        #
                                   self.get_spent_calories())    #
        return info_message   # возврат данных


class Running(Training):    # создание дочернего класса
    """Тренировка: бег."""

    coef_calorie_run_1: int = 18   # коэффициент каллорий при беге 1
    coef_calorie_run_2: int = 20   # коэффициент каллорий при беге 2
    training_type: str = 'RUN'   # код тренировки

    def __init__(self,    # конструктор класса-наследника
                 action: int,       #
                 duration: float,   # аргументы
                 weight: float      # конструктора
                 ) -> None:         #
        super().__init__(action, duration, weight)   # наследование

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        calories_run: float = ((self.coef_calorie_run_1         # формула
                               * self.get_mean_speed()            # потраченных
                               - self.coef_calorie_run_2)         # каллорий
                               * self.weight / self.M_IN_KM       # при
                               * self.duration * self.M_IN_HOUR    # беге
                               )
        return calories_run   # возврат полученного значения


class SportsWalking(Training):   # создание дочернего класса
    """Тренировка: спортивная ходьба."""

    CCW1: float = 0.035   # коэффициент каллорий при ходьбе 1
    CCW2: int = 2         # коэффициент каллорий при ходьбе 2
    CCW3: float = 0.029   # коэффициент каллорий при ходьбе 3
    training_type: str = 'WLK'   # код тренировки

    def __init__(self,   # конструктор класса-наследника
                 action: int,      #
                 duration: float,  # аргументы
                 weight: float,    # конструктора
                 height: float     #
                 ) -> None:
        super().__init__(action, duration, weight)   # наследование
        self.height = height   # добавление нового свойства

    def get_spent_calories(self) -> float:   # каллори при ходьбе
        calories_walking: float = ((self.CCW1
                                   * self.weight
                                   + (self.get_mean_speed()**self.CCW2
                                    // self.height)            # формула
                                   * self.CCW3 * self.weight)  # каллорий
                                   * (self.duration
                                   * self.M_IN_HOUR)
                                   )
        return calories_walking     # возврат полученного значения


class Swimming(Training):  # создание дочернего класса
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # длинна гребка(м)
    training_type: str = 'SWM'  # код тренировки
    coef_callorie_swim_1: float = 1.1  # коэффициент каллорий при плавании 1
    coef_callorie_swim_2: int = 2  # коэффициент каллорий при плавании 2

    def __init__(self,                         #
                 action: int,                  #
                 duration: float,              # аргументы
                 weight: float,                # конструктора
                 length_pool: int,             #
                 count_pool: int,              #
                 LEN_STEP: float = 1.38        #
                 ) -> None:
        super().__init__(action, duration, weight, LEN_STEP)  # наследование
        self.length_pool = length_pool  # добавление свойства длинны бассейна
        self.count_pool = count_pool  # переплываний бассейна

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_swimming: float = ((self.get_mean_speed()        # формула
                                    + self.coef_callorie_swim_1)  # каллорий
                                    * self.coef_callorie_swim_2
                                    * self.weight)
        return calories_swimming  # возврат полученного значения

    def get_mean_speed(self) -> float:  # расчет ср. скор.
        mean_speed_swimming: float = (self.length_pool   # формула
                                      * self.count_pool
                                      / self.M_IN_KM       # средней скорости
                                      / self.duration)      # при плавании
        return mean_speed_swimming  # возврат полученного значения


def read_package(workout_type: str, data: list):   # функция чтения данных
    my_dict = {'SWM': Swimming,            # словарь
               'RUN': Running,             # с
               'WLK': SportsWalking
               }       # данными
    for key, value in my_dict.items():  # перебор значений
        if key == workout_type:  # условие возврата значения
            return value(*data)  # возврат значения


def main(Training) -> None:
    """Главная функция."""

    info = Training.show_training_info()  # сохранение объекта в переменную
    print(info.get_message())  # вывод сообщения о тренировке

    if __name__ == '__main__':
        packages = [
            ('SWM', [720, 1, 80, 25, 40]),
            ('RUN', [15000, 1, 75]),
            ('WLK', [9000, 1, 75, 180]),
        ]

        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)
