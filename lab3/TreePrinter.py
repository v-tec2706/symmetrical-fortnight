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
        result = tmp + str(self.operand) + "\n" + getIndent()+ str(self.var1) + "\n" + getIndent() + str(self.var2)
        level -= 1
        return result

    @addToClass(AST.OperationAssignment)
    def printTree(self, indent=0):
        global level
        result = ""
        tmp = getIndent()
        level += 1
        result = tmp +"=\n" + getIndent() + str(self._id) + "\n" + self.operation.printTree()
        level -= 1
        return result

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        pass


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
