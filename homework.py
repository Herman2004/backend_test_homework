from typing import Dict, List, Union, Type, Optional
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

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
    COEFF_TO_SPEED: float = 18
    SUBTRAHEND_CALORIES: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_TO_SPEED * self.get_mean_speed()
                - self.SUBTRAHEND_CALORIES)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float

    COEFF_OF_WEIGHT = 0.035
    COEFF_OF_ACCELERATION = 0.029

    def get_spent_calories(self) -> float:
        return ((self.COEFF_OF_WEIGHT * self.weight + (self.get_mean_speed()
                ** 2 // self.height)
                * self.COEFF_OF_ACCELERATION * self.weight) * self.duration
                * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    LEN_STEP: float = 1.38
    COEFF_SPEED: float = 1.1
    COEFF_TO_WEIGHT: float = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_SPEED)
                * self.COEFF_TO_WEIGHT * self.weight)


CONFORMITY_TO_CLASSES: Dict[str, Type[Training]] = {"SWM": Swimming,
                                                    "RUN": Running,
                                                    "WLK": SportsWalking}
AVAILABLE_CODES_STR = ', '.join(CONFORMITY_TO_CLASSES.keys())


def read_package(workout_type: str,
                 data: List[Union[float, int]]) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in CONFORMITY_TO_CLASSES:
        raise KeyError("f'Неизвестный код {workout_type}'")
    return CONFORMITY_TO_CLASSES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    if training is None:
        print(training.show_training_info().get_message())
    raise AttributeError


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
