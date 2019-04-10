

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

class ExactPosVal(Node):
    def __init__(self, exactPos, val):
        self.exactpos = exactPos
        self.val = val


class VarAssignment(Node):
    def __init__(self, _id, var):
        self._id = _id
        self.var = var

class TwoVarOperation(Node):
    def __init__(self, var1, operand,  var2):
        self.var1 = var1
        self.operand = operand
        self.var2 = var2

class SingleVarOperation(Node):
    def __init__(self, var1, operand):
        self.var1 = var1
        self.operand = operand


class OperationAssignment(Node):
    def __init__(self, _id, sign, operation):
        self._id = _id
        self.sign = sign
        self.operation = operation

class Vectors(Node):
    def __init__(self, vectors):
        self.vectors = [vectors]

class Var(Node):
    def __init__(self, val):
        self.val = val


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements

class VectorAssignment(Node):
    def __init__(self, _id, vector):
        self._id = _id
        self.vector = vector

class Condition(Node):
    def __init__(self,left, operand, right):
        self.left = left
        self.operand = operand
        self.right = right

class IfWhile(Node):
    def __init__(self,operation, condition, expr):
        self.operation = operation
        self.condition = condition
        self.expr = expr

class IfElse(Node):
    def __init__(self, condition, expr1, expr2):
        self.expr1 = expr1
        self.condition = condition
        self.expr2 = expr2

class Else(Node):
    def __init__(self, expr):
       self.expr = expr

class For(Node):
    def __init__(self, _id, rangeFrom, rangeTo, expr):
        self._id = _id
        self.rangeFrom = rangeFrom
        self.rangeTo = rangeTo
        self.expr = expr

class SimpleFun(Node):
    def __init__(self, function):
        self.function = function

class Return(Node):
    def __init__(self, expression):
        self.expression = expression

class Content(Node):
    def __init__(self, content):
        self.content = [content]

class String(Node):
    def __init__(self, content):
        self.content = content

class Print(Node):
    def __init__(self, content):
        self.content = content


class Elements(Node):
    def __init__(self, elements):
        self.elements = [elements]

class Instructions(Node):
    def __init__(self, instr):
        self.instrs = [instr]

class Error(Node):
    def __init__(self):
        pass
