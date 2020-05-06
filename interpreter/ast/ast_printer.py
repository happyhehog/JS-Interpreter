import typing

from treelib import Tree

import interpreter.ast.ast_nodes as ast_nodes


class ASTPrinter:
    def __init__(self):
        self.ast_tree = Tree()

    def __get_base_node_info(self, node: ast_nodes.Node) -> str:
        location = "(" + str(node.location.start.line) + ":" + str(node.location.start.column) + ")"
        return type(node).__name__ + " " + location

    def __get_name_value_string(self, name: str, value) -> str:
        return " [" + name + ": " + value + "]"

    @typing.overload
    def visit(self, node: ast_nodes.Program, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.Literal, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.Identifier, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.BlockStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.FunctionBody, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.ExpressionStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.EmptyStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.ReturnStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.BreakStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.ContinueStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.IfStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.WhileStatement, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.FunctionDeclaration, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.VariableDeclarator, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.VariableDeclaration, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.ArrayExpression, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.Property, parent_str: str = None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.ObjectExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.FunctionExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.UnaryExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.BinaryExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.AssignmentExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.LogicalExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.MemberExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.CallExpression, parent_str=None) -> typing.NoReturn:
        ...

    @typing.overload
    def visit(self, node: ast_nodes.SequenceExpression, parent_str=None) -> typing.NoReturn:
        ...

    def visit(self, node, parent_str: str = None):
        if node is None:
            return

        if isinstance(node, ast_nodes.Program):
            node_str = self.__get_base_node_info(node)
            self.ast_tree.create_node(node_str, node_str)
            if node.body is not None:
                for prog_body_node in node.body:
                    self.visit(prog_body_node, node_str)
            return

        if isinstance(node, ast_nodes.Literal):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Value", str(node.value))
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            return

        if isinstance(node, ast_nodes.Identifier):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Name", str(node.name))
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            return

        if isinstance(node, ast_nodes.BlockStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            for block_body_node in node.body:
                self.visit(block_body_node, node_str)
            return

        if isinstance(node, ast_nodes.FunctionBody):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            for func_body_node in node.body:
                self.visit(func_body_node, node_str)
            return

        if isinstance(node, ast_nodes.ExpressionStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.expression, node_str)
            return

        if isinstance(node, ast_nodes.EmptyStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            return

        if isinstance(node, ast_nodes.ReturnStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            if node.argument is not None:
                self.visit(node.argument, node_str)
            return

        if isinstance(node, ast_nodes.BreakStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            return

        if isinstance(node, ast_nodes.ContinueStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            return

        if isinstance(node, ast_nodes.IfStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            if node.alternate is not None:
                self.visit(node.alternate, node_str)
                self.visit(node.test, node_str)
                self.visit(node.consequent, node_str)
            else:
                self.visit(node.test, node_str)
                self.visit(node.consequent, node_str)
            return

        if isinstance(node, ast_nodes.WhileStatement):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.test, node_str)
            self.visit(node.body, node_str)
            return

        if isinstance(node, ast_nodes.FunctionDeclaration):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Name", node.id.name)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            if node.id is not None:
                self.visit(node.id, node_str)
                self.visit(node.body, node_str)
            else:
                self.visit(node.body, node_str)
            return

        if isinstance(node, ast_nodes.VariableDeclarator):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            if node.init is not None:
                self.visit(node.id, node_str)
                self.visit(node.init, node_str)
            else:
                self.visit(node.id, node_str)
            return

        if isinstance(node, ast_nodes.VariableDeclaration):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            for declaration in node.declarations:
                self.visit(declaration, node_str)
            return

        if isinstance(node, ast_nodes.ArrayExpression):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            for element in node.elements:
                self.visit(element, node_str)
            return

        if isinstance(node, ast_nodes.Property):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.key, node_str)
            self.visit(node.value, node_str)
            return

        if isinstance(node, ast_nodes.ObjectExpression):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            for element in node.elements:
                self.visit(element, node_str)
            return

        if isinstance(node, ast_nodes.FunctionExpression):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Name", node.id.name)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            if node.id is not None:
                self.visit(node.id, node_str)
                self.visit(node.body, node_str)
            else:
                self.visit(node.body, node_str)
            return

        if isinstance(node, ast_nodes.UnaryExpression):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Operator", node.operator.value)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.argument, node_str)
            return

        if isinstance(node, ast_nodes.BinaryExpression):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Operator", node.operator.value)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.left, node_str)
            self.visit(node.right, node_str)
            return

        if isinstance(node, ast_nodes.AssignmentExpression):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Operator", node.operator.value)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.left, node_str)
            self.visit(node.right, node_str)
            return

        if isinstance(node, ast_nodes.LogicalExpression):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Operator", node.operator.value)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.left, node_str)
            self.visit(node.right, node_str)
            return

        if isinstance(node, ast_nodes.MemberExpression):
            node_str = self.__get_base_node_info(node) + self.__get_name_value_string("Computed([]/.)",
                                                                                      str(node.computed))
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.object, node_str)
            self.visit(node.property, node_str)
            return

        if isinstance(node, ast_nodes.CallExpression):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            self.visit(node.callee, node_str)
            for arg in node.arguments:
                self.visit(arg, node_str)
            return

        if isinstance(node, ast_nodes.SequenceExpression):
            node_str = self.__get_base_node_info(node)
            if parent_str is not None:
                self.ast_tree.create_node(node_str, node_str, parent=parent_str)
            for exp in node.expressions:
                self.visit(exp, node_str)
            return
