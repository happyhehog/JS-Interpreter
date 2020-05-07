import os

from interpreter.ast.ast_printer import get_ast, get_str_ast
from interpreter.parser import parse_file


def get_files_by_type(type: str):
    file_list = []
    for root, dirs, files in os.walk("test_ast_files/"):
        for file in files:
            if file.endswith(type):
                file_list.append(os.path.join(root, file))
    return file_list


def test_ast():
    js_files_list = get_files_by_type(".js")
    for filename in js_files_list:
        parse_tree = parse_file(filename)[1]
        ast_tree = get_ast(parse_tree)
        assert get_str_ast(ast_tree) == open(filename.replace(".js", ".ast")).read()
