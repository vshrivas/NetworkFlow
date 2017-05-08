import sys
import antlr4
from CypherLexer import CypherLexer
from CypherParser import CypherParser
from CypherVisitor import CypherVisitor

def main(argv):
    # Set up antlr4 parser...
    input_stream = antlr4.FileStream(argv[1])
    lexer = CypherLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = CypherParser(stream)
    tree = parser.cypher()
    tree_string  = antlr4.tree.Trees.Trees.toStringTree(tree, None, parser)
    visitor = CypherVisitor()
    print("Here's the tree: \n", tree_string, "\n\n")
    print("In we go!")
    visitor.visit(tree)

    print("Printing node-variables and their new properties:")
    print(visitor.to_create)


if __name__ == '__main__':
    main(sys.argv)