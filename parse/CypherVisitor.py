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
        print("I'm in Cypher now!")
        return self.visitChildren(ctx)


    def visitCreate(self, ctx:CypherParser.CreateContext):
        print("In a create statement.")
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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#xorExpression.
    def visitXorExpression(self, ctx:CypherParser.XorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#andExpression.
    def visitAndExpression(self, ctx:CypherParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#notExpression.
    def visitNotExpression(self, ctx:CypherParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#comparisonExpression.
    def visitComparisonExpression(self, ctx:CypherParser.ComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#addOrSubtractExpression.
    def visitAddOrSubtractExpression(self, ctx:CypherParser.AddOrSubtractExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#multiplyDivideModuloExpression.
    def visitMultiplyDivideModuloExpression(self, ctx:CypherParser.MultiplyDivideModuloExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#powerOfExpression.
    def visitPowerOfExpression(self, ctx:CypherParser.PowerOfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#unaryAddOrSubtractExpression.
    def visitUnaryAddOrSubtractExpression(self, ctx:CypherParser.UnaryAddOrSubtractExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#stringListNullOperatorExpression.
    def visitStringListNullOperatorExpression(self, ctx:CypherParser.StringListNullOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#propertyOrLabelsExpression.
    def visitPropertyOrLabelsExpression(self, ctx:CypherParser.PropertyOrLabelsExpressionContext):
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


del CypherParser