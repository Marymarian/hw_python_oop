class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть строку сообщения с данными о тренировке."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 LEN_STEP: float = 0.65,
                 M_IN_KM: int = 1000
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = LEN_STEP
        self.M_IN_KM = M_IN_KM

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        result_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return result_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.result_distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 LEN_STEP: float,
                 M_IN_KM: int,
                 coeff_calorie_1: int = 18,
                 coeff_calorie_2: int = 20) -> None:
        """Наследуем функциональность конструктора из класса-родителя."""
        super().__init__(action, duration, weight, LEN_STEP, M_IN_KM)
        """Добавляем новую функциональность: свойства coeff_calorie_1 и 2."""
        self.coeff_calorie_1 = coeff_calorie_1
        self.coeff_calorie_2 = coeff_calorie_2

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""

        spent_calories_run = ((self.coeff_calorie_1 * self.mean_speed
                              - self.coeff_calorie_2) * self.weight
                              / self.M_IN_KM * self.duration)
        return spent_calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 LEN_STEP: float,
                 M_IN_KM: int,
                 height: float,
                 coeff_calorie_3: float = 0.035,
                 coeff_calorie_4: float = 0.029,
                 coeff_speed: int = 2) -> None:
        """Наследуем функциональность конструктора из класса-родителя."""
        super().__init__(action, duration, weight, LEN_STEP, M_IN_KM)
        """Добавляем новую функциональность: свойства coeff_calorie_3 и 4,
           coeff_speed, height."""
        self.coeff_calorie_3 = coeff_calorie_3
        self.coeff_calorie_4 = coeff_calorie_4
        self.coeff_speed = coeff_speed
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""

        spent_calories_wlk = ((self.coeff_calorie_3
                               * self.weight
                               + (self.mean_speed**self.coeff_speed
                                  // self.height)
                               * self.coeff_calorie_4 * self.weight)
                              * self.duration)
        return spent_calories_wlk


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 M_IN_KM: int,
                 length_pool: float,
                 count_pool: int,
                 coeff_calorie_5: float = 1.1,
                 coeff_calorie_6: float = 2,
                 LEN_STEP: float = 1.38) -> None:
        """Наследуем функциональность конструктора из класса-родителя."""
        super().__init__(action, duration, weight, M_IN_KM)
        """Добавляем новую функциональность: свойства coeff_calorie_5 и 6,
        length_pool, count_pool, LEN_STEP."""
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.coeff_calorie_5 = coeff_calorie_5
        self.coeff_calorie_6 = coeff_calorie_6
        self.LEN_STEP = LEN_STEP

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""

        mean_speed_swm = (self.length_pool * self.count_pool
                          / self.M_IN_KM / self.duration)
        return mean_speed_swm

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""

        spent_calories_swm = ((self.mean_speed_swm + self.coeff_calorie_5)
                              * self.coeff_calorie_6 * self.weight)
        return spent_calories_swm


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    types_of_training: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return types_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
