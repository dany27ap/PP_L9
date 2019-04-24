from P3.Logger import Log
import copy

class Token:
    def __init__(self, token, term):
        self.token = token
        self.term = term

    # suprascrisa de Operator si Operand
    def IsNonTerm(self):
        pass

    def GetData(self):
        return self.token


class Operator(Token):
    def __init__(self, token):
        super().__init__(token, False)
        if token in ['+', '-']:
            self.priority = 1
        elif token in ['*', '/']:
            self.priority = 2
        else:
            self.priority = 0

    def get_priority(self):
        return self.priority

    def IsNonTerm(self):
        return True


class Operand(Token):
    def __init__(self, token):
        super().__init__(token, True)

    def IsNonTerm(self):  # operanzii intr-un arbore AST sunt TERMINALI (noduri frunza)
        return False


class AST:
    def __init__(self):
        self.Left = None # membru de tip AST
        self.Right = None # membru de tip AST
        self.Data = None # membru de tip Token

    # aceasta functie trebuie modificata pentru a permite prioritati intre operatori
    # hint: daca un operator cu prioritate mai mare (*) este mai aproape de radacina in
    # AST fata de un operator nou cu prioritate mai mica, se inverseaza sub-arborii
    def add_ast_node(self, token):
        if token.IsNonTerm():
            if self.Left is None and self.Right is None and self.Data is None:
                print('Expresia nu poate sa inceapa cu un operator!!!')
                # raise Exception('Wrong expression')
                return
            elif self.Left is None and self.Right is None:
                self.Left = AST()
                self.Left.Data = self.Data
                self.Data = token
            elif self.Left is not None and self.Right is None:
                print('Eroare de sintaxa: Aveti 2 operatori consecutivi!')
                # raise Exception('Wrong expression')
                return
            elif self.Left is not None and self.Right is not None:
                if self.Data.get_priority() < token.get_priority():
                    temp = AST()
                    temp.Data = token
                    temp.Left = self.Right
                    self.Right = temp
                else:
                    temp = copy.copy(self)
                    self.Data = token
                    self.Left = temp
                    self.Right = None
                # self.Right.add_ast_node(token)
        else:
            if self.Left is None and self.Right is None and self.Data is None:
                self.Data = token
            elif self.Left is None and self.Right is None:
                print('Eroare de sintaxa: Aveti 2 operanzi consecutivi!')
                # raise Exception('Wrong expression')
            elif self.Left is not None and self.Right is not None:
                self.Right.add_ast_node(token)
            elif self.Left is not None and self.Right is None:
                self.Right = AST()
                self.Right.Data = token

    # suport pentru a accepta visitatori
    def AcceptVisitor(self, printvisitor):
        return printvisitor.visit(self)


class ASTBuilder:
    Left = None
    Right = None

    def __init__(self, expresie, ast):
        self.expresie = expresie
        self.sym = []
        self.Parse()
        self.ListSymbols()
        self.ast = ast
        for tok in self.sym:
            self.ast.add_ast_node(tok)

    def Parse(self):
        nr = 0
        was_nr = False
        for chr in self.expresie:
            if '0' <= chr <= '9':
                nr *= 10
                nr += int(chr)
                was_nr = True
            elif chr in ['+', '-', '*', '/']:
                if was_nr:
                    self.sym += [Operand(nr)]
                    was_nr = False
                    nr = 0
                self.sym += [Operator(chr)]
        if was_nr:
            self.sym += [Operand(nr)]
            was_nr = False
            nr = 0

    def ListSymbols(self):

        print('Din expresia data am extras urmatoarele elemente:')
        for item in self.sym:
            if item.IsNonTerm():
                print(item.GetData(), '\t->\tOperator')
            else:
                print(item.GetData(), '\t->\tOperand')


class PrintVisitor:

    def visit(self, ast):
        pass


class VisitPreOrdine(PrintVisitor):

    def visit(self, ast):
        print(ast.Data.GetData(), end=" ")
        if ast.Left is not None:
            self.visit(ast.Left)
        if ast.Right is not None:
            self.visit(ast.Right)


class VisitPostOrdine(PrintVisitor):

    def visit(self, ast):
        if ast is None:
            return
        self.visit(ast.Left)
        self.visit(ast.Right)
        print(ast.Data.GetData(), end=" ")
        Log.get_instanta().write(str(ast.Data.GetData()))


class VisitInOrdine(PrintVisitor):

    def visit(self, ast):
        if ast is None:
            return
        self.visit(ast.Left)
        print(ast.Data.GetData(), end=" ")
        self.visit(ast.Right)


class VisitCalculation(PrintVisitor):

    def visit(self, ast):
        if ast.Right is None and ast.Left is None:
            return ast.Data.GetData()
        else:
            op = ast.Data.GetData()
            right = self.visit(ast.Right)
            left = self.visit(ast.Left)
            if op is '+':
                return right + left
            if op is '-':
                return left - right
            if op is '*':
                return right * left
            if op is '/':
                return left / right

def main():
    ast = AST()
    expression_math = "1+2*2-2"
    expression_ast = ASTBuilder(expression_math, ast)
    pre = VisitPreOrdine()
    inord = VisitInOrdine()
    post = VisitPostOrdine()
    calcul = VisitCalculation()

    ast.AcceptVisitor(pre)
    print()
    ast.AcceptVisitor(post)
    print()
    ast.AcceptVisitor(inord)
    print()
    result = ast.AcceptVisitor(calcul)
    print(str(expression_math) + " = " + str(result))


if __name__ == "__main__":
    Log = Log('pom.txt')
    main()