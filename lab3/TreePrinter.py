from __future__ import print_function
import AST

level = 0

def getIndent():
    global level
    indentStr = ""
    for i in range(level):
        indentStr += "| "
    return indentStr

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.assignSpec)
    def printTree(self, indent = 0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + "=\n"+ getIndent() + str(self.id) + "\n" + getIndent() + str(self.funName) + "\n" + getIndent() + "| " + str(self.argument)
        return result

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + str(self.sign) + "\n" + getIndent() + str(self.id) + "\n" + getIndent() + str(
            self.var)
        level -= 1
        return result

    @addToClass(AST.VarAssignment)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + "=\n" + getIndent() + str(self._id) + "\n" + getIndent() + str(self.var)
        return result


    @addToClass(AST.Bracket)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + str(self.left) + "\n" + self.expr.printTree() + "\n" + tmp + str(
            self.right)
        level -= 1
        return result

    @addToClass(AST.TwoVarOperation)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + str(self.operand) + "\n" + getIndent()+ self.var1.printTree() + "\n" + getIndent() + self.var2.printTree()
        level -= 1
        return result

    @addToClass(AST.SingleVarOperation)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        if self.operand == "\'":
            operand = "TRANSPOSE"
        else:
            operand = str(self.operand)
        result = operand + "\n" + getIndent() + self.var1.printTree()
        level -= 1
        return result

    @addToClass(AST.OperationAssignment)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp +str(self.sign) + "\n" + getIndent() + str(self._id) + "\n" + self.operation.printTree()
        level -= 1
        return result


    @addToClass(AST.Vectors)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        for e in self.vectors:
                result = result + e.printTree()
        return result



    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = getIndent() + "VECTOR\n"
        result = result +self.elements.printTree()
        level -= 1
        return result

    @addToClass(AST.Elements)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        for e in self.elements:
            result += getIndent() + str(e) + "\n"
        level -= 1
        return result


    @addToClass(AST.VectorAssignment)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + "=\n" + getIndent() + str(self._id) + "\n" + getIndent() + "VECTOR\n" + self.vector.printTree()
        level -= 1
        return result

    @addToClass(AST.ExactPos)
    def printTree(self, indent=0):
        global level
        result = ""
        level += 1
        result = getIndent() + str(self._id) + "\n" + getIndent() + str(self.num1) + "\n" + getIndent() + str(self.num2)
        level -= 1
        return result

    @addToClass(AST.ExactPosVal)
    def printTree(self, indent=0):
        global level
        result = ""
        level += 1
        tmp = getIndent()
        result = "=\n" + getIndent() + "REF\n"+ self.exactpos.printTree() + "\n" + tmp + str(self.val)
        level -= 1
        return result

    @addToClass(AST.Var)
    def printTree(self, indent=0):
        result = str(self.val)
        return result

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + str(self.operand) + "\n" + getIndent() + self.left.printTree() + "\n" + getIndent() + self.right.printTree()
        level -= 1
        return result


    @addToClass(AST.IfWhile)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        if self.operation == "if":
            then = tmp + "THEN\n"
        else:
            then = ""
        result = tmp + str(self.operation).upper() + "\n" + self.condition.printTree() + "\n" + then + self.expr.printTree()
        level -= 1
        return result

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + str("IF") + "\n" + self.condition.printTree()+ "\n" + getIndent() + "THEN\n" + self.expr1.printTree()+ "\n" + getIndent() +"ELSE\n" + self.expr2.printTree()
        level -= 1
        return result

    @addToClass(AST.Else)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + "ELSE\n"+ self.expr.printTree()
        level -= 1
        return result

    @addToClass(AST.For)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + "FOR\n"+ getIndent() + str(self._id) + "\n" +\
                 getIndent() + "RANGE\n" +\
                getIndent() + "| "+ self.rangeFrom.printTree()+ "\n" +\
                getIndent() + "| " + self.rangeTo.printTree() + "\n" +\
                self.expr.printTree()
        level -= 1
        return result

    @addToClass(AST.SimpleFun)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + str(self.function).upper()
        level -= 1
        return result

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp + "RETURN\n" + getIndent() + self.expression.printTree()
        level -= 1
        return result

    @addToClass(AST.Content)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        for e in self.content:
            result += getIndent() + str(e.printTree()) + "\n" #.printTree()
        level -= 1
        return result

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result += tmp + "PRINT\n" + self.content.printTree()
        level -= 1
        return result

    @addToClass(AST.Instructions)
    def printTree(self):
        global level
        result = ""
        x = ""
        for i in self.instrs:
            level = 0
            result += x + i.printTree()
            x = "\n"
        return result

    # @addToClass(AST.String)
    # def printTree(self, indent=0):
    #     global level
    #     result = ""
    #     tmp = getIndent()
    #     level += 1
    #     result += getIndent() + str(self.content)
    #     level -= 1
    #     return result


    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        pass


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
