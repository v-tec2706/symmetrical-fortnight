

class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class assignSpec(Node):
    def __init__(self, _id, funName, argument):
        self.id = _id
        self.funName = funName
        self.argument = argument

class Assignment(Node):
    def __init__(self, _id, sign, var):
        self.id = _id
        self.sign = sign
        self.var = var

class Bracket(Node):
    def __init__(self, left, expr, right):
        self.left = left
        self.expr = expr
        self.right = right

class ExactPos(Node):
    def __init__(self, _id, num1, num2):
        self._id = _id
        self.num1 = num1
        self.num2 = num2

class VarAssignment(Node):
    def __init__(self, _id, var):
        self._id = _id
        self.var = var

class TwoVarOperation(Node):
    def __init__(self, var1, operand,  var2):
        self.var1 = var1
        self.operand = operand
        self.var2 = var2

class OperationAssignment(Node):
    def __init__(self, _id, operation):
        self._id = _id
        self.operation = operation


class Error(Node):
    def __init__(self):
        pass
