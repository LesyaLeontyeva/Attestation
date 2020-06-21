import itertools
from pprint import pprint
from typing import Iterable, Dict, Optional, List, Any


class OutOfResourceError(Exception):
    def __init__(self: Any, message: str) -> None:
        super().__init__(message)


def get_robot(item: Dict) -> Optional[int]:
    return item.get("robot")


def calculate(mydict: Iterable) -> List:
    # группируем исходные данные по роботам
    robot_resource = itertools.groupby(mydict, get_robot)
    water = None
    sugar = None
    other_resources = list()
    overall_instruction = list()  # запишем сюда все инструкции
    robot_manager = dict()  # для того чтобы распределять ресурсы на разных роботах и избежать пересечений
    for key, group in robot_resource:
        if not robot_manager.get(key):
            robot_manager[key] = dict()
            robot_manager[key]["вкусовые добавки"] = list()
        for resource in group:
            if resource.get("resource") == "вода":  # вода - базовый ресурс, работаем с ним отдельно
                robot_manager[key]["вода"] = resource
            elif resource.get("resource") == "сахар":  # сахар - базовый ресурс
                robot_manager[key]["сахар"] = resource
            else:
                robot_manager[key]["вкусовые добавки"].append(resource)  # вкусовые добавки - в отдельный список, для
                # упорядочивания

    for key, item in robot_manager.items():
        water = item.get("вода")
        sugar = item.get("сахар")
        other_resources = item.get("вкусовые добавки")
        if water is None or sugar is None:
            raise OutOfResourceError("Ошибка")
        # выясняем сколько возможно сделать бутылок с газировкой
        max_bottle_available = min(int(water.get("limit") // water.get("portion")),
                                   int(sugar.get("limit") // sugar.get("portion")))

        for other_resource in other_resources:

            # Выясняем сколько вкусовых добавок можно использовать
            portions_avail = int(other_resource.get("limit") // other_resource.get("portion"))

            # Предусматриваем вариант, что вкусовых добавок может быть больше, чем оставшейся воды и сахара
            portions_with_syrup = min((max_bottle_available, portions_avail))

            # Пополняем инструкции для производства новыми инструкциями изготовления газировки
            for i in range(portions_with_syrup):
                overall_instruction.append(
                    {
                        water.get("resource"): water.get("portion"),
                        sugar.get("resource"): sugar.get("portion"),
                        other_resource.get("resource"): other_resource.get("portion"),
                        "robot": key
                    }
                )
            # вычитаем из возможного количества порций. вода и сахар была использована.
            max_bottle_available -= portions_with_syrup
        if max_bottle_available > 0:
            for i in range(max_bottle_available):
                overall_instruction.append(
                    {
                        water.get("resource"): water.get("portion"),
                        sugar.get("resource"): sugar.get("portion"),
                        "robot": key
                    }
                )
    # если не удалось составить ни одной инструкции - говорим что ресурсы распределены неверно
    if overall_instruction == []:
        raise OutOfResourceError("Ошибка")

    return overall_instruction


try:
    pprint(calculate([
        {
            "robot": 1,
            "resource": "вода",
            "limit": 2,
            "portion": 1
        },
        {
            "robot": 1,
            "resource": "яблочная вкусовая добавка",
            "limit": 2,
            "portion": 1
        }
    ]))
except OutOfResourceError:
    print("OutOfResourceError")
