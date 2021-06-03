import csv

from typing import List

from config import BASIC_RESULT


def dictionariate(list_of_data: List, numb: int):
    """
    Переделывает из структуры лист листов листов в словарь и подрезает размерность
    по тз. Если по простому, переделываем из представления по рядам в представление
    по колонкам.
    :param list_of_data: список со структурой:[[[header],[row1]...],
                                                [[header],[row1]...]
                                                ]
    :param numb: минимальный макисмальный М для одного вида данных
    :return: словарь сделанный из list_of_data подрезанный снизу по numb
    """
    any_dict = {}
    any_dict.setdefault(str, [])
    for batch in list_of_data:
        for n, k in enumerate(batch[0]):
            if k[:1] == "M" and int(k[1:]) > numb:
                continue
            else:
                for temp in batch[1:]:
                    try:
                        any_dict[k].append(str(temp[n]))
                    except KeyError:
                        any_dict[k] = list(str(temp[n]))
    return any_dict


def lsum(l1: List, l2: List):
    """
    Складывает элементы массива
    :param l1:
    :param l2:
    :return:
    """
    for k in range(len(l1)):
        l1[k] = int(l1[k]) + int(l2[k])


def sort():
    """
    Читает файл и сортирует по первой колонке
    :return:
    """
    with open(BASIC_RESULT, "r+", newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)
        sorted_list = sorted(reader, key=lambda row: row[0])
        file.seek(0)
        file.truncate(0)
        wr = csv.writer(file, delimiter='\t')
        wr.writerow(header)
        for row in sorted_list:
            wr.writerow(row)
