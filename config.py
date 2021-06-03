from glob import glob

CSVS = [k for k in glob("data/*.csv")]
XMLS = [k for k in glob("data/*.xml")]
JSONS = [k for k in glob("data/*.json")]

BASIC_RESULT = "output/b_result.tsv"
ADVANCED_RESULT = "output/a_result.tsv"






