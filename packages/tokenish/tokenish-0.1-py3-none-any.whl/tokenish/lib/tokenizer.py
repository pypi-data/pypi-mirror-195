import os


def get_file_lines(file_path):
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()
    return list(map(lambda line: line.replace("\n", ""), lines))


def get_all_file_paths(directory_path):
    dir_elements = list(map(lambda element: os.path.join(directory_path, element), os.listdir(directory_path)))
    dir_files = list(filter(lambda element_path: os.path.isfile(element_path), dir_elements))
    return dir_files


def gather_tokens(token_paths):
    token_lists = [[] for _ in token_paths]
    for i in range(0, len(token_paths)):
        if os.path.isfile(token_paths[i]):
            token_lists[i] += get_file_lines(token_paths[i])
        else:
            file_paths = get_all_file_paths(token_paths[i])
            for path in file_paths:
                token_lists[i] += get_file_lines(path)
    return token_lists


def fill_tokens(token_lists, pattern):
    token_symbols = ["&TOKEN_{}&".format(i) for i in range(0, len(token_lists))]
    for token_symbol in token_symbols:
        if token_symbol not in pattern:
            raise ValueError("missing expression \"{}\" in pattern {}".format(token_symbol, pattern))
    filled_expressions_buffer = list(map(lambda token: pattern.replace("&TOKEN_0&", token), token_lists[0]))
    for i in range(1, len(token_lists)):
        new_filled_expressions = []
        for filled_expression in filled_expressions_buffer:
            new_filled_expressions += \
                list(map(lambda token: filled_expression.replace("&TOKEN_{}&".format(i), token), token_lists[i]))
        filled_expressions_buffer = new_filled_expressions
    return filled_expressions_buffer
