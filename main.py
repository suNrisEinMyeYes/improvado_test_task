import os
from config import BASIC_RESULT, ADVANCED_RESULT

from readers import (
    read_xml,
    read_json,
    read_csv
)

from advnced import advanced
from dataOperating import (
    sort,
    dictionariate,
)
from writers import create_output

if __name__ == "__main__":
    if os.path.isfile(BASIC_RESULT):
        os.remove(BASIC_RESULT)
    if os.path.isfile(ADVANCED_RESULT):
        os.remove(ADVANCED_RESULT)
    csv_min, csv_list = read_csv()
    json_min, json_list = read_json()
    xml_min, xml_list = read_xml()
    min_over = min(csv_min, json_min, xml_min)

    csv_dict = dict(sorted(list(dictionariate(csv_list, min_over).items())[1:]))
    json_dict = dict(sorted(list(dictionariate(json_list, min_over).items())[1:]))
    xml_dict = dict(sorted(list(dictionariate(xml_list, min_over).items())[1:]))

    create_output(csv_dict, json_dict, xml_dict)
    sort()
    advanced()
