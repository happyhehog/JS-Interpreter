from interpreter.parser import parse_file
from interpreter.ast.ast_printer import get_ast, print_ast

parsed_tuple = parse_file("example.js")
parse_tree = parsed_tuple[1]
ast_tree = get_ast(parse_tree)
print_ast(ast_tree)