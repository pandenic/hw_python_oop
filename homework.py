import typing as ty


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает форматированное сообщение
        с учётом переданных при инициализации данных.
        """
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """
    Базовый класс тренировки. Содержит
    данные о действиях (шаги, гребки и тд)
    и методы get_distance, get_mean_speed,
    get_spent_calories,show_training_info.
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите '
                                  'get_spent_calories подклассах-наследниках')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_minutes: float = self.duration * self.MIN_IN_H
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * duration_in_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CM_IN_M: float = 100
    KMH_IN_MSEC: float = round(1000 / (60 * 60), 3)
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

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
        av_speed_in_m_sec: float = (self.get_mean_speed()
                                    * self.KMH_IN_MSEC)
        duration_in_minutes: float = self.duration * self.MIN_IN_H
        height_in_m = self.height / self.CM_IN_M
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + (av_speed_in_m_sec ** 2 / height_in_m)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * duration_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUT_TYPES:
        raise NotImplementedError('Некорректное название тренировки')
    return WORKOUT_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


WORKOUT_TYPES: ty.Dict[str, ty.Union[ty.Type[Swimming],
                                     ty.Type[Running],
                                     ty.Type[SportsWalking]]] = (
    {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    })

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [420, 4, 20, 42]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
