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
# If the simple flag is false, make a DummyNode instead.
def nodeInfoExtract(visitor, node, simple):
    # Get the variable associated with this if it exists
    variable_exists = False
    if node.variable() is not None:
        variable_exists = True
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
    if simple:
        node_to_add = SimpleNode()
    else: # dummy
        node_to_add = DummyNode()
    node_to_add.properties = properties
    node_to_add.labels = labels
    if variable_exists:
        node_to_add.varname = node_variable
    return node_to_add

# A helper which creates a SimpleRelationship, populating its attributes.
# The node holds a DummyNode that is the left side of the relationship.
# If the simple flag is false, creates a DummyRelationship instead.
def patternElementExtract(visitor, patternElement, node, simple):
    # TODO (BUG): Support relationships without labels
    rel = patternElement.relationshipPattern().relationshipDetail()
    # Get the variable associated with this if it exists
    variable_exists = False
    if rel.variable() is not None:
        variable_exists = True
        rel_variable = (rel.variable().symbolicName().getText())

    # Get the types of the relationship.
    types = []
    for relType in rel.relationshipTypes().relTypeName():
        types.append(relType.schemaName().symbolicName().getText())

    # Extract any properties we have to give the new relationships.
    if rel.properties() is not None:
        rel_properties = dict_from_mapLiteral(visitor, (rel.properties().mapLiteral()))
    else:
        rel_properties = {}

    # Get the node as a simple node
    rel_node = nodeInfoExtract(visitor, patternElement.nodePattern(), True)

    # Now we can create the relationship
    if simple:
        rel_to_add = SimpleRelationship(types, node, rel_node)
    else: # dummy
        rel_to_add = DummyRelationship(types, node, rel_node)
    rel_to_add.properties = rel_properties
    if variable_exists:
        rel_to_add.varname = rel_variable

    # Now for each of the two nodes, add this relationship.
    node.relationships.append(rel_to_add)
    rel_node.relationships.append(rel_to_add)

    return (rel_to_add, rel_node)


# This class defines a complete generic visitor for a parse tree produced by CypherParser.

class CypherVisitor(ParseTreeVisitor):
    def __init__(self):
        ###### CREATE STATEMENT RELEVANT STUFF:

        # Represents the relationships to be created (maybe later, the
        # relationships to return or something) and their properties/labels
        self.relationships_to_create = []

        # Represents the nodes and properties to be created on a CREATE command
        # The keys are the variable names bound to the nodes.
        # TODO: the following is out-of-date. We use dummies/simples now.
        # The values are 2-tuples; the first item is a list of relationships in
        # which this key lies, and the second item is a dictionary representing
        # the properties this node has (e.g. {"name": "Donnie"})
        self.nodes_to_create = []



        ###### MATCH STATEMENT RELEVANT STUFF:

        # Represents the nodes and properties to be matched on a MATCH command
        # They have the same structure as previous.
        self.nodes_to_match = []

        # Represents the relationship and node to be matched on a MATCH command
        # These will be the equivalent of the patternElementChain, or each node
        # that each relationship matches to.  They will be tuples of
        # (relationship, node)
        self.relationships_to_match = []



        ###### RETURN STATEMENT RELEVANT STUFF:

        # Keeps track of all seen variable names, and relates them to their
        # associated BasicNode/BasicRelationship. For example "CREATE (n)
        # RETURN n" would map {"n": BasicNode()}. This is important for RETURN
        # statements primarily.
        self.var_name_to_basic = {}

        # Represents the list of expressions to return. [TODO: figure out the
        # best way to do this.] For now, each element of this list will be a
        # 2-tuple: the first item is the printed column name associated with
        # the expression, and the second is a string that represents the
        # expression to evaluate. For example, "RETURN n.name AS hello" will
        # be in this list as ("hello", "n.name"). Another example: "RETURN
        # n.age + 100 * 2" will be in this list as ("", "n.age + 100 * 2").
        # Unfortunately, this off-loads evaluation of expressions to somebody
        # else, even though this antlr parser has a calculator...
        self.to_return = []


    # Visit a parse tree produced by CypherParser#cypher.
    def visitCypher(self, ctx:CypherParser.CypherContext):
        return self.visitChildren(ctx)


    def visitCreate(self, ctx:CypherParser.CreateContext):
        # Get to the good part. Should only have one patternPart.
        parts = ctx.pattern().patternPart(0).anonymousPatternPart().patternElement()

        # First get the first node. Always exists.
        curr_node = nodeInfoExtract(self, parts.nodePattern(), True)
        # Aside: update the variable name --> BasicNode association.
        self.var_name_to_basic[curr_node.varname] = curr_node

        # Each part in the element chain is associated with a
        # relationship and a node to create.
        for part in parts.patternElementChain():
            (rel, rel_node) = patternElementExtract(self, part, curr_node, True)
            # Aside: update the variable name --> BasicRelationship association.
            self.var_name_to_basic[rel_node.varname] = rel_node

            # Now that curr_node has updated to include the relationship, add
            # it to the list of nodes to create. Also add the relationship.
            self.nodes_to_create.append(curr_node)
            self.relationships_to_create.append(rel)
            # Update curr_node
            curr_node = rel_node
        # Make sure the last node is added as well
        self.nodes_to_create.append(curr_node)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#match_.
    def visitMatch_(self, ctx:CypherParser.Match_Context):
        # Get to the good part. Should only have one patternPart.
        # TODO: support more than one patternPart; that is, support queries
        # of the form "MATCH (n) --> (m), (p) --> (q)".
        parts = ctx.pattern().patternPart(0).anonymousPatternPart().patternElement()

        # First get the first node. Always exists.
        curr_node = nodeInfoExtract(self, parts.nodePattern(), False)
        # Aside: update the variable name --> BasicNode association.
        self.var_name_to_basic[curr_node.varname] = curr_node

        # Each part in the element chain is associated with a
        # relationship and a node to create.
        for part in parts.patternElementChain():
            (rel, rel_node) = patternElementExtract(self, part, curr_node, False)
            # Aside: update the variable name --> BasicRelationship association.
            self.var_name_to_basic[rel_node.varname] = rel_node

            # Now that curr_node has updated to include the relationship, add
            # it to the list of nodes to create. Also add the relationship.
            self.nodes_to_match.append(curr_node)
            self.relationships_to_match.append(rel)
            # Update curr_node
            curr_node = rel_node
        # Make sure the last node is added as well
        self.nodes_to_match.append(curr_node)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#return_.
    def visitReturn_(self, ctx:CypherParser.Return_Context):
        # Get to the items to return. returnBody should exist, otherwise we
        # would've thrown a parse error...
        items = ctx.returnBody().returnItems()

        # TODO: handle "RETURN *"
        for item in items.returnItem():
            # Should we name the column something?
            if item.variable():
                # Yes: this is an AS statement. (e.g. RETURN n AS name)
                colName = item.variable().symbolicName().getText()
            else:
                # No: the column header will just be the expression itself.
                colName = ""

            # The first element in this 2-tuple is the printed column name,
            # and the second is the expression to evaluate.
            self.to_return.append((colName, item.getText().split()[0]))


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