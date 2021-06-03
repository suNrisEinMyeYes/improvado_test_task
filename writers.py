import csv

from typing import Dict

from config import BASIC_RESULT


def create_output(csv_d: Dict, json_d: Dict, xml_d: Dict):
    """
    объединяет в себе несколько вызовов writer. Потом будет легче масштабировать
    :param csv_d:
    :param json_d:
    :param xml_d:
    :return:
    """
    writer(csv_d, True)
    writer(json_d)
    writer(xml_d)
    pass


def writer(any_dict: Dict, write_head: bool = False):
    """
    Записывает переданный словарь в файл.
    :param any_dict:
    :param write_head:
    :return:
    """
    with open(BASIC_RESULT, 'a', newline='') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        keys = list(any_dict.keys())
        temp = list()
        if write_head:
            tsv_writer.writerow(keys)
        for numb in range(len(any_dict[keys[0]])):
            for key in keys:
                temp.append(any_dict[key][numb])
            tsv_writer.writerow(temp)
            temp.clear()
