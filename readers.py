import csv
import xml.etree.ElementTree as ET
import json

from config import (
    CSVS,
    JSONS,
    XMLS,
)


def read_csv():
    """
    Читает .csv файлы из листа конфига. Заносит данные в программу в виде списков,
    а также вычисляет минимальное из конечных значений "M". Выход - мин. макс. значение
    М и список, который по длине равен количеству файлов данного типа, который хранит
    данные в виде file[[header],[row 1],[row 2]..[row n]]
    """
    list_u = []
    batch = []
    min_numb_of_headers = None
    headers_read = False
    while len(CSVS) > 0:
        with open(CSVS.pop(), "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if not headers_read:
                    batch.append(row)
                    headers_read = True
                    temp = (max(row)[1:])
                    if min_numb_of_headers is None:
                        min_numb_of_headers = temp
                    elif temp < min_numb_of_headers:
                        min_numb_of_headers = temp
                else:
                    batch.append(row)
            headers_read = False
            temp = batch.copy()
            list_u.append(temp)
            batch.clear()
    return int(min_numb_of_headers), list_u


def read_json():
    """
    Делает то же самое, что и csv_reader и по такому же принцыпу, но для json
    """
    min_max_numb_of_headers = None
    list_u = []
    batch = []
    head_read = False
    while len(JSONS) > 0:
        with open(JSONS.pop(), "r") as json_file:
            data = json.load(json_file)
            for i in data["fields"]:
                if not head_read:
                    batch.append(list(i.keys()))
                    head_read = True
                batch.append(list(i.values()))
            head_read = False
            temp = batch.copy()
            temp_max = max(temp[0])[1:]
            if min_max_numb_of_headers is None:
                min_max_numb_of_headers = temp_max
            elif min_max_numb_of_headers > temp_max:
                min_max_numb_of_headers = temp_max
            list_u.append(temp)
            batch.clear()
    return int(min_max_numb_of_headers), list_u


def read_xml():
    """
        Делает то же самое, что и csv_reader и по такому же принцыпу, но для xml
    """
    min_max_numb_of_headers = None
    list_of_headers = []
    list_of_values = []
    list_u = []
    while len(XMLS) > 0:
        name = XMLS.pop()
        root = ET.parse(name).getroot()
        for tag in root.findall("objects/object"):
            value = tag.attrib["name"]
            list_of_headers.append(value)
            list_of_values.append(tag.findall("value")[0].text)
        temp = (max(list_of_headers)[1:])
        if min_max_numb_of_headers is None:
            min_max_numb_of_headers = temp
        elif temp < min_max_numb_of_headers:
            min_max_numb_of_headers = temp

        list_u.append([list_of_headers, list_of_values])
    return int(min_max_numb_of_headers), list_u
