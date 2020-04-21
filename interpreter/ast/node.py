import antlr4


class Position:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column


class SourceLocation:
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end


class Node:
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.location = SourceLocation(Position(ctx.start.line, ctx.start.column),
                                       Position(ctx.stop.line, ctx.stop.column))
