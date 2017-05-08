# Generated from Cypher.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CypherParser import CypherParser
else:
    from CypherParser import CypherParser

def dict_from_mapLiteral(visitor, ctx:CypherParser.MapLiteralContext):
    d = {}
    for (propertyName, expression) in zip(ctx.propertyKeyName(), ctx.expression()):
        d[propertyName.getText()] = visitor.visitExpression(expression)
    return d

# This class defines a complete generic visitor for a parse tree produced by CypherParser.

class CypherVisitor(ParseTreeVisitor):
    def __init__(self):
        # Represents the nodes and properties to be created on a CREATE command
        self.to_create = {}

    # Visit a parse tree produced by CypherParser#cypher.
    def visitCypher(self, ctx:CypherParser.CypherContext):
        return self.visitChildren(ctx)


    def visitCreate(self, ctx:CypherParser.CreateContext):
        for part in ctx.pattern().patternPart():
            # TODO: Error catching.
            node = part.anonymousPatternPart().patternElement().nodePattern()
            node_variable = (node.variable().symbolicName().getText())
            properties = dict_from_mapLiteral(self, (node.properties().mapLiteral()))
            # Add this node to the list, and move on.
            self.to_create[node_variable] = properties
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CypherParser#expression.
    def visitExpression(self, ctx:CypherParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#orExpression.
    def visitOrExpression(self, ctx:CypherParser.OrExpressionContext):
        if len(ctx.xorExpression()) == 1:
            return self.visitXorExpression(ctx.xorExpression(0))
        else:
            # TODO: Ensure that arguments are booleans.
            return any(map(self.visitXorExpression, ctx.xorExpression()))


    # Visit a parse tree produced by CypherParser#xorExpression.
    def visitXorExpression(self, ctx:CypherParser.XorExpressionContext):
        if len(ctx.andExpression()) == 1:
            return self.visitAndExpression(ctx.andExpression(0))
        else:
            # XOR only makes sense if it has exactly two arguments, if not one.
            assert(len(ctx.andExpression()) == 2)
            return self.visitAndExpression(ctx.andExpression(0)) \
                        != self.visitAndExpression(ctx.andExpression(1))



    # Visit a parse tree produced by CypherParser#andExpression.
    def visitAndExpression(self, ctx:CypherParser.AndExpressionContext):
        if len(ctx.notExpression()) == 1:
            return self.visitNotExpression(ctx.notExpression(0))
        else:
            # TODO: Ensure that arguments are booleans.
            return all(map(self.visitNotExpression, ctx.notExpression()))


    # Visit a parse tree produced by CypherParser#notExpression.
    def visitNotExpression(self, ctx:CypherParser.NotExpressionContext):
        result = self.visitComparisonExpression(ctx.comparisonExpression())
        num_nots = len(ctx.NOT())
        if num_nots == 0:
            return result
        elif num_nots % 2 == 1:
            return not result
        else:
            return result


    # Visit a parse tree produced by CypherParser#comparisonExpression.
    def visitComparisonExpression(self, ctx:CypherParser.ComparisonExpressionContext):
        lhs = self.visitAddOrSubtractExpression(ctx.addOrSubtractExpression())
        partial = ctx.partialComparisonExpression()
        if partial:
            assert(len(partial) == 1)
            rhs = self.visitAddOrSubtractExpression(partial[0].addOrSubtractExpression())
            comp = partial[0].getChild(0).getText()
            if comp == '=':
                return lhs == rhs
            elif comp == '<>':
                return lhs != rhs
            elif comp == '<':
                return lhs < rhs
            elif comp == '>':
                return lhs > rhs
            elif comp == '<=':
                return lhs <= rhs
            elif comp == '>=':
                return lhs >= rhs
            else:
                assert(False, "Unrecognized comparison token %s", comp) # :(
        else:
            return lhs


    # Visit a parse tree produced by CypherParser#addOrSubtractExpression.
    def visitAddOrSubtractExpression(self, ctx:CypherParser.AddOrSubtractExpressionContext):
        # Here is the first expression's value. Note that if there is no
        # subsequent adding or subtracting, this will immediately be returned.
        res = self.visitMultiplyDivideModuloExpression(ctx.multiplyDivideModuloExpression(0))

        # The expression is formatted something like "1 + 2 - 3 + 5...".
        # The problem here is that "ctx.getChildren()" will include whitespace
        # blocks as children as well, screwing up indexing. We have to extract
        # all the pluses and minuses, since those are what we care about, and
        # let horrible errors plague our way if the indexing doesn't work
        # thereafter. For non-malicious input, this should work.

        # Extract all the pluses and minuses.
        ops = list(filter(lambda x: x in ['+', '-'],
                          [child.getText() for child in ctx.getChildren()]))

        # Go through each expression, adding or subtracting its value.
        # We do the [1:] list slice because we want to remove the first
        # expression, which we currently are calling "res".
        for (i, expr) in enumerate(ctx.multiplyDivideModuloExpression()[1:]):
            # Thanks to our previous filtering, we know that the desired
            # operation lives at ops[i].
            op = ops[i]
            if op == '+':
                res += self.visitMultiplyDivideModuloExpression(expr)
            elif op == '-':
                res -= self.visitMultiplyDivideModuloExpression(expr)
            else:
                assert(False)
        return res


    # Visit a parse tree produced by CypherParser#multiplyDivideModuloExpression.
    def visitMultiplyDivideModuloExpression(self, ctx:CypherParser.MultiplyDivideModuloExpressionContext):
        # For info on how this all works, see visitAddOrSubtractExpression.

        res = self.visitPowerOfExpression(ctx.powerOfExpression(0))

        ops = list(filter(lambda x: x in ['*', '/', '%'],
                          [child.getText() for child in ctx.getChildren()]))


        for (i, expr) in enumerate(ctx.powerOfExpression()[1:]):
            op = ops[i]
            if op == '*':
                res *= self.visitPowerOfExpression(expr)
            elif op == '/':
                res /= self.visitPowerOfExpression(expr)
            elif op == '%':
                res %= self.visitPowerOfExpression(expr)
            else:
                assert(False)
        return res


    # Visit a parse tree produced by CypherParser#powerOfExpression.
    def visitPowerOfExpression(self, ctx:CypherParser.PowerOfExpressionContext):
        res = self.visitUnaryAddOrSubtractExpression(ctx.unaryAddOrSubtractExpression(0))

        # See visitAddOrSubtractExpression to see why we do the list slicing.
        for expr in ctx.unaryAddOrSubtractExpression()[1:]:
            res **= visitUnaryAddOrSubtractExpression(expr)

        return res


    # Visit a parse tree produced by CypherParser#unaryAddOrSubtractExpression.
    def visitUnaryAddOrSubtractExpression(self, ctx:CypherParser.UnaryAddOrSubtractExpressionContext):
        res = self.visitStringListNullOperatorExpression(ctx.stringListNullOperatorExpression())

        if (list([child.getText() for child in ctx.getChildren()]).count('-')) % 2 == 0:
            return res
        else:
            return -res


    # Visit a parse tree produced by CypherParser#stringListNullOperatorExpression.
    def visitStringListNullOperatorExpression(self, ctx:CypherParser.StringListNullOperatorExpressionContext):
        # TODO: All the string/list/NULL-involving expressions :)
        return self.visitPropertyOrLabelsExpression(ctx.propertyOrLabelsExpression(0))


    # Visit a parse tree produced by CypherParser#propertyOrLabelsExpression.
    def visitPropertyOrLabelsExpression(self, ctx:CypherParser.PropertyOrLabelsExpressionContext):
        # TODO
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#atom.
    def visitAtom(self, ctx:CypherParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#literal.
    def visitLiteral(self, ctx:CypherParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:CypherParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#listLiteral.
    def visitListLiteral(self, ctx:CypherParser.ListLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#partialComparisonExpression.
    def visitPartialComparisonExpression(self, ctx:CypherParser.PartialComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#parenthesizedExpression.
    def visitParenthesizedExpression(self, ctx:CypherParser.ParenthesizedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#relationshipsPattern.
    def visitRelationshipsPattern(self, ctx:CypherParser.RelationshipsPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#filterExpression.
    def visitFilterExpression(self, ctx:CypherParser.FilterExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#integerLiteral.
    def visitIntegerLiteral(self, ctx:CypherParser.IntegerLiteralContext):
        return int(ctx.getText())


    # Visit a parse tree produced by CypherParser#doubleLiteral.
    def visitDoubleLiteral(self, ctx:CypherParser.DoubleLiteralContext):
        return float(ctx.getText())


    # Visit a parse tree produced by CypherParser#literal.
    def visitLiteral(self, ctx:CypherParser.LiteralContext):
        if ctx.StringLiteral():
            # The list slicing strips out the quote characters at the beginning
            # and the end.
            return ctx.StringLiteral().getText()[1:-1]
        else:
            return self.visitChildren(ctx)


del CypherParser