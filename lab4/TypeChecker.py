#!/usr/bin/python

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        print("UNKNOWN STRUCTURE")
        error_found = 1


class TypeChecker(NodeVisitor):

    declared_variables = {}
    matrix_vector_len = {}
    matrix_vector_num = {}

    loop_number = 0
    vector_len = -1
    vector_num = 0
    possible_to_compare = [('int','int'),('int','float'),('float','int'),('float','float'),('str','str')]

    not_declared_err_num = 0

    def reset(self):
        self.vector_len = -1
        self.vector_num = 0
        self.not_declared_err_num = 0

    def visit_Instructions(self, node):
        for ins in node.instrs:
            self.visit(ins)
            self.reset()
            print("--------")


    def visit_VectorAssignment(self, node):
        self.visit(node.vector)
        self.matrix_vector_len[node._id] = self.vector_len
        self.matrix_vector_num[node._id] = self.vector_num


    def visit_assignSpec(self, node):
        if len(node.argument.elements) < 2:
            self.matrix_vector_len[node.id] = int(node.argument.elements[0])
        else:
            self.matrix_vector_len[node.id] = int(node.argument.elements[1])
        self.matrix_vector_num[node.id] = len(node.argument.elements)
        for e in node.argument.elements:
            if not isinstance(e, int):
                print("special functions argument must be integer!")


    def visit_IfWhile(self, node):
        self.loop_number += 1
        self.visit(node.condition)
        self.visit(node.expr)
        self.loop_number -= 1


    def visit_For(self, node):
        self.loop_number += 1
        self.visit(node.expr)
        self.loop_number -= 1

    def visit_SimpleFun(self, node):
        if self.loop_number <= 0:
            print("used outside loop: ", str(node.function).upper())
            self.error_found = 1

    def visit_Vectors(self, node):
        self.vector_num += 1
        for e in node.vectors:
            self.visit(e)

    def visit_Vector(self, node):
        self.visit(node.elements)

    def visit_Elements(self, node):
        if self.vector_num == 0:
            self.vector_num += 1
        if self.vector_len == -1:
            self.vector_len = len(node.elements)
        else:
            if len(node.elements) != self.vector_len:
                print("Vector sizes must be equal!")

    def visit_ExactPos(self, node):
        if node._id not in self.matrix_vector_len.keys():
            print("not defined: ", node._id)

    def visit_ExactPosVal(self, node):
        self.visit(node.exactpos)
        if len(node.exactpos.indexes.elements) != (self.matrix_vector_num.get(node.exactpos._id)):
            print("improper indexes values! expected: ", self.matrix_vector_num.get(node.exactpos._id))
        for e in node.exactpos.indexes.elements:
            if e >= self.matrix_vector_len.get(node.exactpos._id) or e < 0:
                print("out of range assignment! .. -> ", e, "..")

    def visit_VarAssignment(self, node):
        self.declared_variables[node._id] = node.var

    def checkType(self,x):
        if isinstance(x,str):
            return 'str'
        if isinstance(x,float):
            return 'float'
        if isinstance(x,int):
            return 'int'
        else:
            return 'null'


    def visit_Condition(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if self.not_declared_err_num == 0:
            if node.left.val in self.declared_variables:
                left_type = self.checkType(self.declared_variables.get(node.left.val))
            else:
                left_type = self.checkType(node.left.val)

            if node.right.val in self.declared_variables:
                right_type = self.checkType(self.declared_variables.get(node.right.val))
            else:
                right_type = self.checkType(node.right.val)
        if (right_type, left_type) not in self.possible_to_compare:
            print("cannot compare different types!")


    def visit_TwoVarOperation(self, node):

        self.visit(node.var1)
        self.visit(node.var2)

        if node.operand in ['+','-','*','/']:
            if (node.var1.val not in self.matrix_vector_len.keys()) != (node.var2.val not in self.matrix_vector_len.keys()):
                print("improper arguments types!")
        elif node.operand in ['.+','.-','.*','./']:
            if node.var1.val not in self.matrix_vector_len.keys() or node.var2.val not in self.matrix_vector_len.keys():
                print("dot operation requires matrix arguments! ")

        if self.matrix_vector_len.get(node.var1.val) != self.matrix_vector_len.get(node.var2.val):
            print("vectors length must match! ")
        if self.matrix_vector_num.get(node.var1.val) != self.matrix_vector_num.get(node.var2.val):
            print("number of nested vectors must match! ")

    def visit_OperationAssignment(self,node):
        self.declared_variables[node._id] = node.operation
        self.visit(node.operation)


    def visit_Var(self, node):
        if node.val not in self.declared_variables and node.val not in self.matrix_vector_len.keys() and isinstance(node.val,str):
            print("not declared! ", node.val)
            self.not_declared_err_num += 1


    def visit_Return(self,node):
        self.visit(node.expression)

    def visit_Print(self, node):
        self.visit(node.content)