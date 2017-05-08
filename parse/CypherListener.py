# Generated from Cypher.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CypherParser import CypherParser
else:
    from CypherParser import CypherParser
from CypherListenerBase import CypherListenerBase

def dict_from_mapLiteral(ctx:CypherParser.MapLiteralContext):
    d = {}
    for (propertyName, expression) in zip(ctx.propertyKeyName(), ctx.expression()):
        # TODO: Convert everything to visitors, and then evaluate the expression
        # by calling "visitExpression".
        d[propertyName.getText()] = expression.getText()
    return d

# This class defines a complete listener for a parse tree produced by CypherParser.
class CypherListener(CypherListenerBase):
    def __init__(self):
        # Represents the nodes and properties to be created on a CREATE command
        self.to_create = {}

    def enterCypher(self, ctx:CypherParser.CypherContext):
        print("Hello! I am going to parse now.")

    def exitCypher(self, ctx:CypherParser.CypherContext):
        print("All done!")

    def enterCreate(self, ctx:CypherParser.CreateContext):
        for part in ctx.pattern().patternPart():
            # TODO: Error catching.
            node = part.anonymousPatternPart().patternElement().nodePattern()
            node_variable = (node.variable().symbolicName().getText())
            properties = dict_from_mapLiteral((node.properties().mapLiteral()))

            # Add this node to the list, and move on.
            self.to_create[node_variable] = properties