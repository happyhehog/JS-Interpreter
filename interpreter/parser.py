import antlr4
from interpreter.antlr.lexer.JavaScriptLexer import JavaScriptLexer
from interpreter.antlr.parser.JavaScriptParser import JavaScriptParser


def parse_file(path_to_file: str):
    input_stream = antlr4.FileStream(path_to_file)
    lexer = JavaScriptLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = JavaScriptParser(token_stream)
    tree = parser.program()
    return tree

