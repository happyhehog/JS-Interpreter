import antlr4
from interpreter.ast.node import Node
import interpreter.ast.operators as operators


class Expression(Node):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        super().__init__(ctx)


class Statement(Node):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        super().__init__(ctx)


class Declaration(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        super().__init__(ctx)


class Identifier(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, name: str):
        self.name = name
        super().__init__(ctx)


class Literal(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, value):
        self.value = value
        super().__init__(ctx)


class Program(Node):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.body = []
        super().__init__(ctx)


class BlockStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.body = []
        super().__init__(ctx)


class FunctionBody(BlockStatement):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        super().__init__(ctx)


class Function:
    def __init__(self):
        self.id = None
        self.params = []
        self.body = None


class ExpressionStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext, expression: Expression):
        self.expression = expression
        super().__init__(ctx)


class EmptyStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        super().__init__(ctx)


class ReturnStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.argument = None
        super().__init__(ctx)


class BreakStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        super().__init__(ctx)


class ContinueStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        super().__init__(ctx)


class IfStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext, test: Expression, consequent: Statement):
        self.alternate = None
        self.test = test
        self.consequent = consequent
        super().__init__(ctx)


class WhileStatement(Statement):
    def __init__(self, ctx: antlr4.ParserRuleContext, test: Expression, body: Statement):
        self.test = test
        self.body = body
        super().__init__(ctx)


class FunctionDeclaration(Declaration, Function):
    def __init__(self, ctx: antlr4.ParserRuleContext, body: FunctionBody, id: Identifier):
        self.body = body
        self.id = id
        self.params = []
        super().__init__(ctx)


class VariableDeclarator(Node):
    def __init__(self, ctx: antlr4.ParserRuleContext, id: Identifier):
        self.id = id
        self.init = None
        super().__init__(ctx)


class VariableDeclaration(Declaration):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.declarations = []
        super().__init__(ctx)


class ArrayExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.elements = []
        super().__init__(ctx)


class Property(Node):
    def __init__(self, ctx: antlr4.ParserRuleContext, key: Expression, value: Expression):
        self.key = key
        self.value = value
        super().__init__(ctx)


class ObjectExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.elements = []
        super().__init__(ctx)


class FunctionExpression(Expression, Function):
    def __init__(self, ctx: antlr4.ParserRuleContext, body: FunctionBody):
        self.body = body
        self.id = None
        self.params = []
        super().__init__(ctx)


class UnaryExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, operator: operators.UnaryOperator, argument: Expression):
        self.operator = operator
        self.argument = argument
        super().__init__(ctx)


class BinaryExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, operator: operators.BinaryOperator, left: Expression,
                 right: Expression):
        self.operator = operator
        self.left = left
        self.right = right
        super().__init__(ctx)


class AssignmentExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, operator: operators.AssignmentOperator, left: Expression,
                 right: Expression):
        self.operator = operator
        self.left = left
        self.right = right
        super().__init__(ctx)


class LogicalExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, operator: operators.LogicalOperator, left: Expression,
                 right: Expression):
        self.operator = operator
        self.left = left
        self.right = right
        super().__init__(ctx)


class MemberExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, object: Expression, property: Expression, computed: bool):
        self.object = object
        self.property = property
        self.computed = computed
        super().__init__(ctx)


class CallExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext, callee: Expression):
        self.callee = callee
        self.arguments = []
        super().__init__(ctx)


class SequenceExpression(Expression):
    def __init__(self, ctx: antlr4.ParserRuleContext):
        self.expressions = []
        super().__init__(ctx)
