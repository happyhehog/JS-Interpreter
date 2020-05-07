import typing
from interpreter.parser import JavaScriptParser
from interpreter.ast.ast_visitor import ASTVisitor
from interpreter.ast.ast_view import ASTView
from interpreter.ast import ast_nodes


def get_ast(tree: JavaScriptParser.ProgramContext) -> ast_nodes.Program:
    parse_tree_visitor = ASTVisitor()
    return parse_tree_visitor.visit(tree)


def save_ast_to_file(ast_nodes: ast_nodes.Program, filename: str) -> typing.NoReturn:
    ast_viewver = ASTView()
    ast_viewver.visit(ast_nodes)
    ast_viewver.ast_tree.save2file(filename, key=False)


def print_ast(ast_nodes: ast_nodes.Program) -> typing.NoReturn:
    ast_viewver = ASTView()
    ast_viewver.visit(ast_nodes)
    ast_viewver.ast_tree.show(key=False)