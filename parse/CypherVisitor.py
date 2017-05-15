# Generated from Cypher.g4 by ANTLR 4.7
from antlr4 import *
from .SimpleTypes import *

if __name__ is not None and "." in __name__:
    from .CypherParser import CypherParser
else:
    from CypherParser import CypherParser

def dict_from_mapLiteral(visitor, ctx:CypherParser.MapLiteralContext):
    d = {}
    for (propertyName, expression) in zip(ctx.propertyKeyName(), ctx.expression()):
        d[propertyName.getText()] = visitor.visitExpression(expression)
    return d

# A helper which creates a SimpleNode, populating its attributes.
def nodeInfoExtract(visitor, node):
    node_variable = (node.variable().symbolicName().getText())

    # Extract any properties we must give this new node.
    if node.properties() is not None:
        properties = dict_from_mapLiteral(visitor, (node.properties().mapLiteral()))
    else:
        properties = {}

    # Extract any labels we must give the node.
    if node.nodeLabels() is not None:
        labels = [label.labelName().getText()
                  for label in node.nodeLabels().nodeLabel()]
    else:
        labels = []

    # Give this node back to the parent, who will add it to the list.
    node_to_add = SimpleNode(node_variable)
    node_to_add.properties = properties
    node_to_add.labels = labels
    return node_to_add

# This class defines a complete generic visitor for a parse tree produced by CypherParser.

class CypherVisitor(ParseTreeVisitor):
    def __init__(self):
        # Represents the relationships to be created (maybe later, the
        # relationships to return or something) and their properties/labels
        self.relationships = []

        # Represents the nodes and properties to be created on a CREATE command
        # The keys are the variable names bound to the nodes.
        # The values are 2-tuples; the first item is a list of relationships in
        # which this key lies, and the second item is a dictionary representing
        # the properties this node has (e.g. {"name": "Donnie"})
        self.nodes_to_create = []

    # Visit a parse tree produced by CypherParser#cypher.
    def visitCypher(self, ctx:CypherParser.CypherContext):
        return self.visitChildren(ctx)


    def visitCreate(self, ctx:CypherParser.CreateContext):
        # Each pattern part is associated with a particular node to create.
        for part in ctx.pattern().patternPart():
            # There are two possibilities.

            # Either this patternPart is a node, which must then be created,
            # or it represents a relationship that connects two nodes.


            # In the relationship case, there are two subcases.

            # Either all of the nodes mentioned in the relationship are brand
            # new (that is, they are not known variables), in which case they
            # must be created, or some of the nodes are not new, in which case
            # they must be looked up in the variable list. (We do not yet
            # support variables.)


            # First, we need to tell whether this part has a relationship!
            if part.anonymousPatternPart().patternElement().patternElementChain():
                detail = part.anonymousPatternPart().patternElement().patternElementChain()[0] \
                             .relationshipPattern().relationshipDetail()

                # Get the label associated with the relationship
                relationshipLabel = detail.relationshipTypes().relTypeName()[0] \
                                          .schemaName().symbolicName().getText()

                # Get any properties associated with the relationship
                if detail.properties() is not None:
                    rel_properties = dict_from_mapLiteral(self, (detail.properties().mapLiteral()))
                else:
                    rel_properties = {}

                # We will use this marker to tell whether we need to construct
                # relationships and nodes in a special way or not.
                isRelationship = True
            else:
                isRelationship = False


            # Need to get the variable associated with the node(s) in question.
            # If we're creating a relationship, there are two nodes to get.
            # If not, just one.
            element = part.anonymousPatternPart().patternElement()
            if isRelationship:
                nodes = [
                        element.nodePattern(), # left-hand node
                        element.patternElementChain()[0].nodePattern() # right-hand node
                ]
            else:
                nodes = [
                        element.nodePattern(), # left-hand node is the only node
                ]

            # We need to extract all the info we can from the node(s) we
            # have just procured. Call a helper function to do this, and
            # write down the node(s).
            nodes_to_create = [nodeInfoExtract(self, node) for node in nodes]

            # If we're making a relationship, we need to create one.
            if isRelationship:
                relationship = SimpleRelationship(relationshipLabel,
                                        nodes_to_create[0], nodes_to_create[1])
                relationship.properties = rel_properties
                self.relationships.append(relationship)
                # We also need to make sure the nodes know the relationships
                # that they are a part of. This, of course, generates a
                # reference cycle, but that's ok...
                for node_to_create in nodes_to_create:
                    node_to_create.relationships.append(relationship)

            # Done! Just add it (or them) to our create-list and move on...
            for node in nodes_to_create:
                self.nodes_to_create.append(node)

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