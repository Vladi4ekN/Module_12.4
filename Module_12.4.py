import logging
import unittest

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename='runner_tests.log',
    filemode='w',
    encoding='utf-8',
    format='%(levelname)s: %(message)s'
)


class Runner:
    def __init__(self, name, speed=5):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError(f'Имя может быть только строкой, передано {type(name).__name__}')
        self.distance = 0
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError(f'Скорость не может быть отрицательной, сейчас {speed}')

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    logging.info(f'{participant.name} финишировал на {place} месте')
                    place += 1
                    self.participants.remove(participant)

        return finishers


class RunnerTest(unittest.TestCase):
    def test_runner_initialization(self):
        runner = Runner('Вося', 10)
        self.assertEqual(runner.name, 'Вося')
        self.assertEqual(runner.speed, 10)

    def test_run(self):
        try:
            runner = Runner(12345)
            runner.run()
            logging.info('"test_run" выполнен успешно')
        except TypeError:
            logging.warning("Неверный тип данных для объекта Runner")

    def test_walk(self):
        try:
            runner = Runner('Арсен', -10)
            runner.walk()
            logging.info('"test_walk" выполнен успешно')
        except ValueError:
            logging.warning("Неверная скорость для Runner")

    def test_tournament(self):
        first = Runner('Вося', 10)
        second = Runner('Илья', 5)

        t = Tournament(101, first, second)
        finishers = t.start()

        self.assertIn(1, finishers)
        self.assertIn(2, finishers)
        self.assertEqual(finishers[1].name, 'Вося')
        self.assertEqual(finishers[2].name, 'Илья')


if __name__ == "__main__":
    unittest.main()
