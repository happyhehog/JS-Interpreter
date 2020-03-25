import antlr4
from interpreter.antlr.lexer.JavaScriptLexer import JavaScriptLexer


def get_tokens_text(tokens):
    tokens_text = []
    for t in tokens:
        tokens_text.append(t.text)
    tokens_text = tuple(tokens_text)
    return tokens_text


def test_arithmetic_expression():
    lexer = JavaScriptLexer(antlr4.InputStream("a = 2 + 2;"))
    tokens = lexer.getAllTokens()
    tokens_text = get_tokens_text(tokens)
    assert len(tokens) == 10
    assert tokens_text == ("a", " ", "=", " ", "2", " ", "+", " ", "2", ";")


def test_function():
    lexer = JavaScriptLexer(antlr4.InputStream("function func(n) {\nvar a = 10\nprint(a + n);\n}"))
    tokens = lexer.getAllTokens()
    tokens_text = get_tokens_text(tokens)
    assert len(tokens) == 28
    assert (tokens_text[0], tokens_text[7], tokens_text[9], tokens_text[11], tokens_text[17], tokens_text[25]) == \
           ("function", "{", "var", "a", "print", ";")
