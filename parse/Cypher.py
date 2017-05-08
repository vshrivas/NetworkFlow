#import sys
import antlr4
from .CypherLexer import CypherLexer
from .CypherParser import CypherParser
from .CypherVisitor import CypherVisitor

def parse(query):
    # Set up antlr4 parser...
    input_stream = antlr4.InputStream(query)
    lexer = CypherLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = CypherParser(stream)
    tree = parser.cypher()
    tree_string  = antlr4.tree.Trees.Trees.toStringTree(tree, None, parser)
    visitor = CypherVisitor()

    # # Here lie some helpful print statements. Bring them back as you
    # # figure out more things to parse:
    # print("Here's the tree: \n", tree_string, "\n\n")

    visitor.visit(tree)

    # For now, return the nodes and the properties to be created.
    print("Trying to create this dict:")
    return visitor.to_create
