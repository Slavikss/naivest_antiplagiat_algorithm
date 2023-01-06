from pathlib import Path
import argparse
import io
import re


# Функция чтения файла
def read_file(file_path):
    file = []
    f = io.open(file_path, 'r', encoding='utf-8')
    for string in f:
        string = string.strip()
        if string != '':
            file.append(string)

    return file


# препроцессинг файла
def preprocess(file):
    # Удаляем знаки пунктуации
    file = [re.sub(r'[^\w\s]', '', string) for string in file if
            string.count('"') == string.count("'") == string.count('#') == 0]

    # Переводим всё в нижний регистр
    file = [string.lower() for string in file]

    # Удаляем всё, что находится внутри квадратных и фигурных скобок
    file = [re.sub(r"\[.*\]|\{.*\}", "", string) for string in file]

    # Удаляем нестандартные буквы, которые не входят в ascii
    file = [''.join([ch for ch in string if ch.isascii()]).strip() for string in file]

    # Убираем пустые строки
    file = [string for string in file if string != '']
    return file


# Расстояние Левенштейна между двумя строками
def compare(A, B):
    # Вычисляем размер матрицы размером на 1 больше
    len_a, len_b = len(A) + 1, len(B) + 1
    # Создаем ее
    D = [[float('inf') for _ in range(len_b)] for _ in range(len_a)]
    # Нумеруем по строкам и вертикалям
    for i in range(len_a):
        D[i][0] = i
    for j in range(len_b):
        D[0][j] = j

        # Проходимся по всей матрице, заполняя очередной элемент из минимума из элемента левее, выше, левее и выше
    for i in range(1, len_a):
        for j in range(1, len_b):
            c = A[i - 1] != B[j - 1]
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + c)

        # Результатом будет самый правый нижний элемент
    return D[len(A)][len(B)]

# Функция получения меры схожести двух файлов
def get_score(file1, file2):
    file1 = read_file(file1)
    file2 = read_file(file2)

    file1 = preprocess(file1)
    file2 = preprocess(file2)

    len_f_1 = sum([len(w) for w in file1])
    len_f_2 = sum([len(w) for w in file2])

    return round(1 - compare(''.join(file1), ''.join(file2)) / (len_f_1 + len_f_2),2)


# Основный блок, где читаются файлы для сравнения и записывается их результат
def main(input_dir, output_dir):
    files_to_check = [files.split() for files in read_file(input_dir)]

    with open(output_dir, 'w') as out:
        for pair in files_to_check:
            file1, file2 = pair
            out.write(str(get_score(file1, file2)))
            out.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Files to process')
    parser.add_argument('indir', type=str, help='Input dir for files')
    parser.add_argument('outdir', type=str, help='Output dir for score file')
    args = parser.parse_args()

    main('input.txt', 'output.txt')
