import interpreter.parser


def read_answer_from_file(path_to_file):
    return open(path_to_file, "r").read()


def test_variables_parsing():
    file_path = "test_parser_files/variables.js"
    parsed_tuple = interpreter.parser.parse_file(file_path)
    parser = parsed_tuple[0]
    tree = parsed_tuple[1]
    assert tree.toStringTree(parser.ruleNames, parser) == read_answer_from_file("test_parser_files/variables.answer")


def test_fibo_parsing():
    file_path = "test_parser_files/fibo.js"
    parsed_tuple = interpreter.parser.parse_file(file_path)
    parser = parsed_tuple[0]
    tree = parsed_tuple[1]
    assert tree.toStringTree(parser.ruleNames, parser) == read_answer_from_file("test_parser_files/fibo.answer")