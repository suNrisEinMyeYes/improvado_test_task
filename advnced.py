import csv

from dataOperating import lsum

from config import ADVANCED_RESULT, BASIC_RESULT


def advanced():
    """
    Вся эта функция выполняет задачу advanced. Берется вывод из базового задания,
    поля Д и М разделяются в разные листы, и путем не очень сложных операций находим
    повторяющиеся пункты Д, складываем их, записываем какой ряд нужно попнуть.
    Далее все которые нужно попнуть убираем из уже конечного листа.
    Врайтер работает только для словарей, поэтому тут его использовать нельзя.
    Конечно можно перегрузить его, но перегрузка будет использовать только тут,
    поэтому врайтер не используется и не перегружен
    :return:
    """
    out = []
    header = []
    with open(BASIC_RESULT, "r+", newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)
        data_ds = []
        data_ms = []
        to_pop = []

        for row in reader:
            data_ds.append(row[:3])
            data_ms.append(row[3:])

        n = 1
        for row in range(len(data_ds)):
            current = data_ds.pop(0)
            pos = n
            if current in data_ds:
                for j in data_ds:
                    if j[0] != current[0]:
                        break
                    elif j == current and pos not in to_pop:
                        lsum(data_ms[n - 1], data_ms[pos])
                        to_pop.append(pos)
                    pos += 1
            out.append(current + data_ms[row])
            n += 1
        to_del = list()
        for i in to_pop:
            to_del.append(out[i])
        out = [ele for ele in out if ele not in to_del]

    with open(ADVANCED_RESULT, "w", newline='') as output:
        output_writer = csv.writer(output, delimiter='\t')

        output_writer.writerow(header)
        for row in out:
            output_writer.writerow(row)
