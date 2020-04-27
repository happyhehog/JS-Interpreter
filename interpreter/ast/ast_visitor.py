import interpreter.ast.ast_nodes as nodes
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
        declarator_node = nodes.VariableDeclarator(ctx, nodes.Identifier(ctx, ctx.Identifier().symbol.text))
        return declarator_node

    def visitEmptyStatement(self, ctx: JavaScriptParser.EmptyStatementContext):
        return nodes.EmptyStatement(ctx)

    def visitIfStatement(self, ctx: JavaScriptParser.IfStatementContext):
        if_node = nodes.IfStatement(ctx, nodes.Expression(self.visit(ctx.expressionSequence())),
                                    nodes.Statement(self.visit(ctx.statement(0))))
        if ctx.Else() is not None:
            if_node.alternate = nodes.Statement(ctx.statement(1))
        return if_node

    def visitWhileStatement(self, ctx: JavaScriptParser.WhileStatementContext):
        return nodes.WhileStatement(ctx, nodes.Expression(self.visit(ctx.expressionSequence())),
                                    nodes.Statement(self.visit(ctx.statement())))

    def visitContinueStatement(self, ctx: JavaScriptParser.ContinueStatementContext):
        return nodes.ContinueStatement(ctx)

    def visitBreakStatement(self, ctx: JavaScriptParser.BreakStatementContext):
        return nodes.BreakStatement(ctx)

    def visitReturnStatement(self, ctx: JavaScriptParser.ReturnStatementContext):
        return_node = nodes.ReturnStatement(ctx)
        if ctx.expressionSequence() is not None:
            return_node.argument = nodes.Expression(self.visit(ctx.expressionSequence()))
        return return_node

    def visitFunctionDeclaration(self, ctx: JavaScriptParser.FunctionDeclarationContext):
        func_decl_node = nodes.FunctionDeclaration(ctx, nodes.FunctionBody(self.visit(ctx.functionBody())),
                                                   nodes.Identifier(ctx, ctx.Identifier().symbol.text))
        if ctx.formalParameterList() is not None:
            for identifier in ctx.formalParameterList().Identifier():
                func_decl_node.params.append(nodes.Identifier(ctx, identifier.symbol.text))
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
                    array_literal_node.elements.append(nodes.Expression(self.visit(element)))
        return array_literal_node

    def visitObjectLiteral(self, ctx: JavaScriptParser.ObjectLiteralContext):
        object_node = nodes.ObjectExpression(ctx)
        assignments = ctx.propertyAssignment()
        for assign in assignments:
            object_node.elements.append(self.visit(assign))
        return object_node

    def visitPropertyExpressionAssignment(self, ctx: JavaScriptParser.PropertyExpressionAssignmentContext):
        return nodes.Property(ctx, nodes.Expression(self.visit(ctx.propertyName())),
                              nodes.Expression(self.visit(ctx.singleExpression())))

    def visitPropertyName(self, ctx: JavaScriptParser.PropertyNameContext):
        if ctx.numericLiteral() is not None:
            return self.visit(ctx.numericLiteral())
        if ctx.identifierName() is not None:
            return self.visit(ctx.identifierName())
        return nodes.Literal(ctx, ctx.StringLiteral().symbol.text)

    def visitExpressionSequence(self, ctx: JavaScriptParser.ExpressionSequenceContext):
        sequence_node = nodes.SequenceExpression(ctx)
        for expression in ctx.singleExpression():
            sequence_node.expressions.append(self.visit(expression))
        return sequence_node
