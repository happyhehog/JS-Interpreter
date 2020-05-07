import os
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
    ast_viewver.ast_tree.save2file(filename, key=False, line_type="ascii")


def print_ast(ast_nodes: ast_nodes.Program) -> typing.NoReturn:
    ast_viewver = ASTView()
    ast_viewver.visit(ast_nodes)
    ast_viewver.ast_tree.show(key=False, line_type="ascii")


def get_str_ast(ast_nodes: ast_nodes.Program) -> str:
    ast_viewver = ASTView()
    ast_viewver.visit(ast_nodes)
    # Package doesn't allow you to return a string with sorted nodes, so you have to do this.
    # https://github.com/caesar0301/treelib/issues/111
    ast_viewver.ast_tree.save2file("temp", key=False, line_type="ascii") #
    result = open("temp").read()
    os.remove("temp")
    return result
