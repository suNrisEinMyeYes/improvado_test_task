import csv
import xml.etree.ElementTree as ET
import json
import os

from typing import List,Dict

from config import (
    CSVS,
    JSONS,
    XMLS,
)


def read_csv():
    list_u = []
    batch = []
    min_numb_of_headers = None
    list_of_headers = []
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
    min_max_numb_of_headers = None
    list_u = []
    batch = []
    head_read = False
    list_of_values = []
    list_of_headers = []
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
    min_max_numb_of_headers = None
    list_of_headers = []
    list_of_values = []
    list_u = []
    batch = []
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


csv_min, csv_list = read_csv()
json_min, json_list = read_json()
xml_min, xml_list = read_xml()
min_over = min(csv_min, json_min, xml_min)
print(type(min_over))


def dictionariate(list_of_data : List, numb : int = min_over):
    dict = {}
    dict.setdefault(str, [])
    for l in list_of_data:
        for n,k in enumerate(l[0]):
            if k[:1] == "M" and int(k[1:]) > numb:
                continue
            else:
                for temp in l[1:]:
                    try:
                        dict[k].append(str(temp[n]))
                    except KeyError:
                        dict[k] = list(str(temp[n]))
    return dict


csv_dict = dict(sorted(list(dictionariate(csv_list).items())[1:]))
json_dict = dict(sorted(list(dictionariate(json_list).items())[1:]))
xml_dict = dict(sorted(list(dictionariate(xml_list).items())[1:]))


def sort():
    with open("output/result.tsv", "r+", newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)
        sorted_list = sorted(reader, key=lambda row: row[0])
        file.seek(0)
        file.truncate(0)
        wr = csv.writer(file, delimiter='\t')
        wr.writerow(header)
        for row in sorted_list:
            wr.writerow(row)

def advanced():
    out = []
    header = []
    with open("output/result.tsv", "r+", newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        header.append(next(reader))
        data_ds = []
        data_ms =[]
        to_pop = []
        #out = []
        for row in reader:
            data_ds.append(row[:3])
            data_ms.append(row[3:])
        #print(data_ds, data_ms)
        n = 1
        for row in range(len(data_ds)):
            current = data_ds.pop(0)
            pos = n
            if current in data_ds:
                for j in data_ds:
                    if j[0] != current[0]:
                        break
                    elif j == current and pos not in to_pop:
                        lsum(data_ms[n-1], data_ms[pos])
                        to_pop.append(pos)
                    pos += 1
            #print(row)
            out.append(current + data_ms[row])
            #print(out)
            n += 1
        to_del = list()
        for i in to_pop:
            to_del.append(out[i])
        out = [ele for ele in out if ele not in to_del]
    with open("output/advanced_result.tsv", "w", newline='') as output:
        output_writer = csv.writer(output, delimiter='\t')
        output_writer.writerow(header)
        for row in out:
            output_writer.writerow(row)


def lsum(l1 : List, l2 : List):
    for k in range(len(l1)):
        l1[k] = int(l1[k]) + int(l2[k])


def create_output(csv_d: Dict, json_d : Dict, xml_d : Dict):
    writer(csv_d, True)
    writer(json_d)
    writer(xml_d)

    pass


def writer(any_dict : Dict, write_head : bool = False):
    with open('output/result.tsv', 'a', newline='') as out_file:
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

advanced()
#create_output(csv_dict, json_dict,xml_dict)
#sort()
