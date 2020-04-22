from enum import Enum


class UnaryOperator(Enum):
    MINUS = "-"
    PLUS = "+"
    LOGIC_NOT = "!"
    BIT_NOT = "~"
    DELETE = "delete"


class BinaryOperator(Enum):
    EQUAL = "=="
    UNEQUAL = "!="
    LESS = "<"
    LESS_OR_EQUAL = "<="
    GREATER = ">"
    GREATER_OR_EQUAL = ">="
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    ARITHMETIC_RIGHT_SHIFT = ">>>"
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
    REMAINDER = "%"
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_AND = "&"


class AssignmentOperator(Enum):
    ASSIGN = "="


class LogicalOperator(Enum):
    LOGICAL_OR = "||"
    LOGICAL_AND = "&&"
