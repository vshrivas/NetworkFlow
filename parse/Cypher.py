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


    # Print the tree.
    print("Here comes the tree...")
    openParens = 0
    for char in tree_string:
        if char == '(':
            print("\n", end="")
            openParens += 1
            print("." * openParens, end="")
        elif char == ')':
            openParens -= 1
        else:
            print(char, end="")
    print("\n", end="")

    # Visit it all!
    visitor.visit(tree)

    # Package everything up nicely and pass it to the database to make it all.
    create_return = {
        "relationships": visitor.relationships,
        "nodes": visitor.nodes_to_create,
    }

    return create_return
