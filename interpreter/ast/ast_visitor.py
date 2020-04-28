import interpreter.ast.ast_nodes as nodes
import interpreter.ast.operators as operators
from interpreter.antlr.parser.JavaScriptParser import JavaScriptParser
from interpreter.antlr.parser.JavaScriptParserVisitor import JavaScriptParserVisitor


class AstVisitor(JavaScriptParserVisitor):
    def visitProgram(self, ctx: JavaScriptParser.ProgramContext):
        program_node = nodes.Program(ctx)
        for child in ctx.sourceElements().children:
            program_node.body.append(self.visit(child))
        return program_node

    def visitBlock(self, ctx: JavaScriptParser.BlockContext):
        block_node = nodes.BlockStatement(ctx)
        for child in ctx.statementList().children:
            block_node.body.append(self.visit(child))
        return block_node

    def visitVariableStatement(self, ctx: JavaScriptParser.VariableStatementContext):
        return self.visit(ctx.variableDeclarationList())

    def visitVariableDeclarationList(self, ctx: JavaScriptParser.VariableDeclarationListContext):
        variable_node = nodes.VariableDeclaration(ctx)
        variable_node.declarations.append(self.visit(ctx.variableDeclaration()))
        return variable_node

    def visitVariableDeclaration(self, ctx: JavaScriptParser.VariableDeclarationContext):
        declarator_node = nodes.VariableDeclarator(ctx, nodes.Identifier(ctx, ctx.Identifier().symbol.text()))
        return declarator_node

    def visitEmptyStatement(self, ctx: JavaScriptParser.EmptyStatementContext):
        return nodes.EmptyStatement(ctx)

    def visitExpressionStatement(self, ctx: JavaScriptParser.ExpressionStatementContext):
        return nodes.ExpressionStatement(ctx, self.visit(ctx.expressionSequence()))

    def visitIfStatement(self, ctx: JavaScriptParser.IfStatementContext):
        if_node = nodes.IfStatement(ctx, self.visit(ctx.expressionSequence()), self.visit(ctx.statement(0)))
        if ctx.Else() is not None:
            if_node.alternate = self.visit(ctx.statement(1))
        return if_node

    def visitWhileStatement(self, ctx: JavaScriptParser.WhileStatementContext):
        return nodes.WhileStatement(ctx, self.visit(ctx.expressionSequence()), self.visit(ctx.statement()))

    def visitContinueStatement(self, ctx: JavaScriptParser.ContinueStatementContext):
        return nodes.ContinueStatement(ctx)

    def visitBreakStatement(self, ctx: JavaScriptParser.BreakStatementContext):
        return nodes.BreakStatement(ctx)

    def visitReturnStatement(self, ctx: JavaScriptParser.ReturnStatementContext):
        return_node = nodes.ReturnStatement(ctx)
        if ctx.expressionSequence() is not None:
            return_node.argument = self.visit(ctx.expressionSequence())
        return return_node

    def visitFunctionDeclaration(self, ctx: JavaScriptParser.FunctionDeclarationContext):
        func_decl_node = nodes.FunctionDeclaration(ctx, self.visit(ctx.functionBody()),
                                                   nodes.Identifier(ctx, ctx.Identifier().symbol.text()))
        if ctx.formalParameterList() is not None:
            for identifier in ctx.formalParameterList().Identifier():
                func_decl_node.params.append(nodes.Identifier(ctx, identifier.symbol.text()))
        return func_decl_node

    def visitFunctionBody(self, ctx: JavaScriptParser.FunctionBodyContext):
        func_body_node = nodes.FunctionBody(ctx)
        for child in ctx.sourceElements().children:
            func_body_node.body.append(self.visit(child))
        return func_body_node

    def visitArrayLiteral(self, ctx: JavaScriptParser.ArrayLiteralContext):
        array_literal_node = nodes.ArrayExpression(ctx)
        if ctx.elementList() is not None:
            for element in ctx.elementList().children:
                if element is JavaScriptParser.SingleExpressionContext:
                    array_literal_node.elements.append(self.visit(element))
        return array_literal_node

    def visitObjectLiteral(self, ctx: JavaScriptParser.ObjectLiteralContext):
        object_node = nodes.ObjectExpression(ctx)
        assignments = ctx.propertyAssignment()
        for assign in assignments:
            object_node.elements.append(self.visit(assign))
        return object_node

    def visitPropertyExpressionAssignment(self, ctx: JavaScriptParser.PropertyExpressionAssignmentContext):
        return nodes.Property(ctx, self.visit(ctx.propertyName()), self.visit(ctx.singleExpression()))

    def visitPropertyName(self, ctx: JavaScriptParser.PropertyNameContext):
        if ctx.numericLiteral() is not None:
            return self.visit(ctx.numericLiteral())
        if ctx.identifierName() is not None:
            return self.visit(ctx.identifierName())
        return nodes.Literal(ctx, ctx.StringLiteral().symbol.text())

    def visitExpressionSequence(self, ctx: JavaScriptParser.ExpressionSequenceContext):
        sequence_node = nodes.SequenceExpression(ctx)
        for expression in ctx.singleExpression():
            sequence_node.expressions.append(self.visit(expression))
        return sequence_node

    def visitLogicalAndExpression(self, ctx: JavaScriptParser.LogicalAndExpressionContext):
        return nodes.LogicalExpression(ctx, operators.LogicalOperator.LOGICAL_AND, self.visit(ctx.singleExpression(0)),
                                       self.visit(ctx.singleExpression(1)))

    def visitObjectLiteralExpression(self, ctx: JavaScriptParser.ObjectLiteralExpressionContext):
        return self.visit(ctx.objectLiteral())

    def visitLogicalOrExpression(self, ctx: JavaScriptParser.LogicalOrExpressionContext):
        return nodes.LogicalExpression(ctx, operators.LogicalOperator.LOGICAL_OR, self.visit(ctx.singleExpression(0)),
                                       self.visit(ctx.singleExpression(1)))

    def visitNotExpression(self, ctx: JavaScriptParser.NotExpressionContext):
        return nodes.UnaryExpression(ctx, operators.UnaryOperator.LOGIC_NOT, self.visit(ctx.singleExpression()))

    def visitArgumentsExpression(self, ctx: JavaScriptParser.ArgumentsExpressionContext):
        call_node = nodes.CallExpression(ctx, self.visit(ctx.singleExpression()))
        if ctx.arguments() is not None:
            for arg in ctx.arguments().singleExpression():
                call_node.arguments.append(self.visit(arg))
        return call_node

    def visitFunctionExpression(self, ctx: JavaScriptParser.FunctionExpressionContext):
        func_exp_node = nodes.FunctionExpression(ctx, self.visit(ctx.functionBody()))
        if ctx.Identifier() is not None:
            func_exp_node.id = nodes.Identifier(ctx, ctx.Identifier().symbol.text())
        if ctx.formalParameterList() is not None:
            for arg_id in ctx.formalParameterList().formalParameterArg().Identifier():
                func_exp_node.params.append(nodes.Identifier(ctx, arg_id.symbol.text()))
        return func_exp_node

    def visitUnaryMinusExpression(self, ctx: JavaScriptParser.UnaryMinusExpressionContext):
        return nodes.UnaryExpression(ctx, operators.UnaryOperator.MINUS, self.visit(ctx.singleExpression()))

    def visitAssignmentExpression(self, ctx: JavaScriptParser.AssignmentExpressionContext):
        return nodes.AssignmentExpression(ctx, operators.AssignmentOperator.ASSIGN, self.visit(ctx.singleExpression(0)),
                                          self.visit(ctx.singleExpression(1)))

    def visitUnaryPlusExpression(self, ctx: JavaScriptParser.UnaryPlusExpressionContext):
        return nodes.UnaryExpression(ctx, operators.UnaryOperator.PLUS, self.visit(ctx.singleExpression()))

    def visitDeleteExpression(self, ctx: JavaScriptParser.DeleteExpressionContext):
        return nodes.UnaryExpression(ctx, operators.UnaryOperator.DELETE, self.visit(ctx.singleExpression()))

    def visitEqualityExpression(self, ctx: JavaScriptParser.EqualityExpressionContext):
        operator_str = ctx.children[1].getText()
        if operator_str == "==":
            unary_operator = operators.BinaryOperator.EQUAL
        elif operator_str == "!=":
            unary_operator = operators.BinaryOperator.UNEQUAL
        else:
            unary_operator = None
        return nodes.BinaryExpression(ctx, unary_operator, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitBitXOrExpression(self, ctx: JavaScriptParser.BitXOrExpressionContext):
        return nodes.BinaryExpression(ctx, operators.BinaryOperator.BIT_XOR, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitMultiplicativeExpression(self, ctx: JavaScriptParser.MultiplicativeExpressionContext):
        if ctx.children[1].getText() == "/":
            multi_operator = operators.BinaryOperator.DIVISION
        elif ctx.children[1].getText() == "*":
            multi_operator = operators.BinaryOperator.MULTIPLICATION
        elif ctx.children[1].getText() == "%":
            multi_operator = operators.BinaryOperator.REMAINDER
        else:
            multi_operator = None
        return nodes.BinaryExpression(ctx, multi_operator, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitBitShiftExpression(self, ctx: JavaScriptParser.BitShiftExpressionContext):
        if ctx.children[1].getText() == "<<":
            shift_operator = operators.BinaryOperator.LEFT_SHIFT
        elif ctx.children[1].getText() == ">>":
            shift_operator = operators.BinaryOperator.RIGHT_SHIFT
        elif ctx.children[1].getText() == ">>>":
            shift_operator = operators.BinaryOperator.ARITHMETIC_RIGHT_SHIFT
        else:
            shift_operator = None
        return nodes.BinaryExpression(ctx, shift_operator, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitParenthesizedExpression(self, ctx: JavaScriptParser.ParenthesizedExpressionContext):
        return self.visit(ctx.expressionSequence())

    def visitAdditiveExpression(self, ctx: JavaScriptParser.AdditiveExpressionContext):
        if ctx.children[1].getText() == "+":
            add_operator = operators.BinaryOperator.ADDITION
        elif ctx.children[1].getText() == "-":
            add_operator = operators.BinaryOperator.SUBTRACTION
        else:
            add_operator = None
        return nodes.BinaryExpression(ctx, add_operator, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitRelationalExpression(self, ctx: JavaScriptParser.RelationalExpressionContext):
        if ctx.children[1].getText() == "<":
            relational_operator = operators.BinaryOperator.LESS
        elif ctx.children[1].getText() == "<=":
            relational_operator = operators.BinaryOperator.LESS_OR_EQUAL
        elif ctx.children[1].getText() == ">":
            relational_operator = operators.BinaryOperator.GREATER
        elif ctx.children[1].getText() == ">=":
            relational_operator = operators.BinaryOperator.GREATER_OR_EQUAL
        else:
            relational_operator = None
        return nodes.BinaryExpression(ctx, relational_operator, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitBitNotExpression(self, ctx: JavaScriptParser.BitNotExpressionContext):
        return nodes.UnaryExpression(ctx, operators.UnaryOperator.BIT_NOT, self.visit(ctx.singleExpression()))

    def visitLiteralExpression(self, ctx: JavaScriptParser.LiteralExpressionContext):
        return self.visit(ctx.literal())

    def visitArrayLiteralExpression(self, ctx: JavaScriptParser.ArrayLiteralExpressionContext):
        return self.visit(ctx.arrayLiteral())

    def visitMemberDotExpression(self, ctx: JavaScriptParser.MemberDotExpressionContext):
        return nodes.MemberExpression(ctx, self.visit(ctx.singleExpression()), self.visit(ctx.identifierName()), False)

    def visitMemberIndexExpression(self, ctx: JavaScriptParser.MemberIndexExpressionContext):
        return nodes.MemberExpression(ctx, self.visit(ctx.singleExpression()), self.visit(ctx.expressionSequence()),
                                      True)

    def visitIdentifierExpression(self, ctx: JavaScriptParser.IdentifierExpressionContext):
        return nodes.Identifier(ctx, ctx.Identifier().symbol.text())

    def visitBitAndExpression(self, ctx: JavaScriptParser.BitAndExpressionContext):
        return nodes.BinaryExpression(ctx, operators.BinaryOperator.BIT_AND, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitBitOrExpression(self, ctx: JavaScriptParser.BitOrExpressionContext):
        return nodes.BinaryExpression(ctx, operators.BinaryOperator.BIT_OR, self.visit(ctx.singleExpression(0)),
                                      self.visit(ctx.singleExpression(1)))

    def visitLiteral(self, ctx: JavaScriptParser.LiteralContext):
        if ctx.StringLiteral() is not None:
            return nodes.Literal(ctx, ctx.StringLiteral().symbol.text())
        if ctx.NullLiteral() is not None:
            return nodes.Literal(ctx, None)
        return self.visit(ctx.numericLiteral())

    def visitNumericLiteral(self, ctx: JavaScriptParser.NumericLiteralContext):
        return nodes.Literal(ctx, float(ctx.DecimalLiteral().symbol.text()))

    def visitIdentifierName(self, ctx: JavaScriptParser.IdentifierNameContext):
        if ctx.reservedWord() is not None:
            return self.visit(ctx.reservedWord())
        return nodes.Identifier(ctx, ctx.Identifier().symbol.text())

    def visitReservedWord(self, ctx: JavaScriptParser.ReservedWordContext):
        if ctx.keyword() is not None:
            return self.visit(ctx.keyword())
        if ctx.NullLiteral() is not None:
            return nodes.Literal(ctx, None)
        return nodes.Literal(ctx, ctx.BooleanLiteral() == "true")

    def visitKeyword(self, ctx: JavaScriptParser.KeywordContext):
        return nodes.Identifier(ctx, ctx.getChild(0).symbol.text())
