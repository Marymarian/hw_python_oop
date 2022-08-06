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

        return f'Тип тренировки: {self.training_type}; ' + \
            f'Длительность: {self.duration:0.3f} ч.; ' + \
            f'Дистанция: {self.distance:0.3f} км; ' + \
            f'Ср. скорость: {self.speed:0.3f} км/ч; ' + \
            f'Потрачено ккал: {self.calories:0.3f}.'


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    DURATION_IN_MINUTES: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        result_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return result_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
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

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""

        spent_calories_run = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                              - self.COEFF_CALORIE_2) * self.weight
                              / self.M_IN_KM * self.DURATION_IN_MINUTES
                              * self.duration)
        return spent_calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    COEFF_SPEED: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""

        spent_calories_wlk = ((self.COEFF_CALORIE_1
                               * self.weight
                               + (self.get_mean_speed() ** self.COEFF_SPEED
                                  // self.height)
                               * self.COEFF_CALORIE_2 * self.weight)
                              * self.DURATION_IN_MINUTES * self.duration)
        return spent_calories_wlk


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""

        mean_speed_swm = (self.length_pool * self.count_pool
                          / self.M_IN_KM / self.duration)
        return mean_speed_swm

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""

        spent_calories_swm = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                              * self.COEFF_CALORIE_2 * self.weight)
        return spent_calories_swm


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    types_of_training: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return types_of_training[workout_type](*data)
    except KeyError:
        print('Отсутствует ключ')


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
