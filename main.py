"""Домашка по питону"""
import csv
from typing import Callable


def read_csv_to_list(file_name: str) -> list:
    """Читает csv в массив

    Args:
        file_name (str): имя файла

    Returns:
        list: массив с данными
    """
    data = []

    with open(file_name, mode="r", encoding="utf-8", newline="") as file:
        csv_reader = csv.reader(file, delimiter=";")
        for row in csv_reader:
            data.append(row)

    return data


def print_decorator(message_template: str):
    """Выводит сообщение перед принтом

    Args:
        message_template (str): Строка сообщения перед выводом функции
    """

    def dict_decorator(func) -> Callable:
        """Декоратор, который принимает функцию, выполняет её, и выводит
        результат с отступами и линиями.
        """

        def wrapper(*args, **kwargs):
            """Внутренняя функция-обертка, которая вызывает переданную функцию
            и выводит результат с отступами и линиями.
            """
            print(f"{message_template}")
            inp_dict = func(*args, **kwargs)

            for key, value in inp_dict.items():
                print(key + ":")
                for subkey, subvalue in value.items():
                    if not isinstance(subvalue, list):
                        print("  ├─ ", subkey + ":", subvalue)
                    elif isinstance(subvalue, list):
                        print("  ", subkey + ":")
                        for i, item in enumerate(subvalue):
                            is_last_item = i == len(subvalue) - 1
                            print(
                                "    └─ " if is_last_item else "    ├─ ",
                                item,
                            )

            return inp_dict

        return wrapper

    return dict_decorator


@print_decorator("Иерархия команд по демартаментам:")
def department_data_structure(data: dict) -> dict:
    """Функция вывода сводного отчёт по департаментам:

    Args:
        data (dict): словарь с данными

    Returns:
        report (dict): словарь с данными
    """
    report: dict = {}
    for row in data[1:]:
        department, section, position = row[1], row[2], row[3]

        if department not in report:
            report[department] = {}
        if section not in report[department]:
            report[department][section] = []
        if position not in report[department][section]:
            report[department][section].append(position)

    return report


def analyze_department_data(data: dict) -> dict:
    """Функция вывода сводного отчёт по департаментам:

    Args:
        data (dict): словарь с данными

    Returns:
        dict: словарь с данными
    """
    department_info: dict = {}
    salary_info: dict = {}
    for i, (_, department, _, _, _, salary) in enumerate(data[1:]):
        if department not in department_info:
            department_info[department] = {
                "Численность": 0,
                "Средняя ЗП": [],
                "Вилка ЗП": "",
            }

        department_info[department]["Численность"] = (
            department_info[department].get("Численность", 0) + 1
        )

        department_info[department]["Средняя ЗП"].append(salary)

        salary = int(salary)

        if department not in salary_info:
            salary_info[department] = {
                "Мин. ЗП": salary,
                "Макс. ЗП": salary,
            }
        else:
            if salary > salary_info[department]["Макс. ЗП"]:
                salary_info[department]["Макс. ЗП"] = salary

            if salary < salary_info[department]["Мин. ЗП"]:
                salary_info[department]["Мин. ЗП"] = salary

        min_salary = salary_info[department]["Мин. ЗП"]
        max_salary = salary_info[department]["Макс. ЗП"]
        department_info[department][
            "Вилка ЗП"
        ] = f"{min_salary} - {max_salary}"

    for k in department_info.keys():
        n, z = list(department_info[k].values())[:2]
        mean = round(sum(list(map(int, z))) / n)
        department_info[k]["Средняя ЗП"] = mean

    return department_info


def write_to_csv(data: dict, filename: str = "report.csv") -> None:
    """Читает словарь записывает в csv

    Args:
        data (dict): словарь с данными
        filename (str): название файла с отчетом, по умолчанию "report.csv"
    """
    data = analyze_department_data(data)
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        fieldnames = ["Департамент", "Численность", "Средняя ЗП", "Вилка ЗП"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for department, info in data.items():
            writer.writerow(
                {
                    "Департамент": department,
                    "Численность": info["Численность"],
                    "Средняя ЗП": info["Средняя ЗП"],
                    "Вилка ЗП": info["Вилка ЗП"],
                }
            )


def run_app(file_name: str) -> None:
    """Запуск программы

    Args:
        file_name (str): имя файла
    """
    data_lst = read_csv_to_list(file_name)
    app = {
        1: department_data_structure,
        2: print_decorator("Сводный отчёт по департаментам:")(
            analyze_department_data
        ),
        3: write_to_csv,
    }
    while True:
        key = int(
            input(
                "Выберите пункт меню:\n"
                "1. Вывести иерархию команд;\n"
                "2. Вывести сводный отчёт по департаментам;\n"
                "3. Сохранить сводный отчёт в формате csv.\n"
            )
        )
        if key in (1, 2, 3):
            run = app[key]
            run(data_lst)
            break
        else:
            print("Пожалуйста, выберите одну из доступных опций (1, 2 или 3).")


if __name__ == "__main__":
    FILE_NAME = "Corp_Summary.csv"
    run_app(FILE_NAME)
