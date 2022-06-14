from dataclasses import dataclass, asdict
from typing import List, Union


@dataclass
class InfoMessage:
    '''Информационное сообщение о тренировке.'''

    training_type: 'Training'
    duration: float
    distance: float
    speed: float
    calories: float
    final_message = ('Тип тренировки: {training_type}; '
                     'Длительность: {duration:0.3f} ч.; '
                     'Дистанция: {distance:0.3f} км; '
                     'Ср. скорость: {speed:0.3f} км/ч; '
                     'Потрачено ккал: {calories:0.3f}.')

    def get_message(self) -> str:
        '''Возвращает характеристику тренировки:
           тип, длительность, дистанцию, ср. скорость,
           количество потраченных калорий.'''
#        return (f'Тип тренировки: {self.training_type}; '
#                f'Длительность: {self.duration:0.3f} ч.; '
#                f'Дистанция: {self.distance:0.3f} км; '
#                f'Ср. скорость: {self.speed:0.3f} км/ч; '
#                f'Потрачено ккал: {self.calories:0.3f}.')
        return self.final_message.format(**asdict(self))


class Training:
    '''Базовый класс тренировки.'''

    M_IN_KM = 1000
    H_IN_MIN = 60
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        '''Получить дистанцию в км.'''
        km_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return km_distance

    def get_mean_speed(self) -> float:
        '''Получить среднюю скорость движения.'''
        d = self.get_distance()
        mean_speed = d / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        '''Получить количество затраченных калорий.'''
        raise NotImplementedError(
            'Переопределите метод '
            f'в классе-наследнике {self.__class__.__name__}.'
        )

    def show_training_info(self) -> InfoMessage:
        '''Вернуть информационное сообщение о выполненной тренировке.'''
        message = InfoMessage(self.__class__.__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    '''Тренировка: бег.'''

    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        '''Получить количество затраченных калорий.'''
        spent_calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                          - self.coeff_calorie_2) * self.weight
                          / self.M_IN_KM * (self.duration * Training.H_IN_MIN))
        return spent_calories


class SportsWalking(Training):
    '''Тренировка: спортивная ходьба.'''

    LEN_STEP = 0.65
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029

    def __init__(self, action, duration, weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.coeff_calorie_1 * self.weight
                          + (self.get_mean_speed()**2 // self.height)
                          * self.coeff_calorie_2 * self.weight)
                          * (self.duration * Training.H_IN_MIN))
        return spent_calories


class Swimming(Training):
    '''Тренировка: плавание.'''

    LEN_STEP = 1.38
    const_1 = 1.1
    const_2 = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        '''Получить среднюю скорость движения.'''
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        '''Получить количество затраченных калорий.'''
        spent_calories = ((self.get_mean_speed() + self.const_1)
                          * self.const_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    '''Прочитать данные, полученные от датчиков.'''
    train_code = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking}
    if workout_type in train_code.keys():
        result = train_code[workout_type](*data)
        return result
    else:
        raise ValueError(
            f'Введён неверный тип тренировки: "{workout_type}". '
            'Поддерживаемые типы тренировок: "SWM", "RUN", "WLK".'
        )


def main(training: Training) -> None:
    '''Главная функция.'''
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
