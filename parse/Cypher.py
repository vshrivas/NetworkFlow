import sys
import antlr4
from CypherLexer import CypherLexer
from CypherParser import CypherParser
from CypherListener import CypherListener

def main(argv):
    # Set up antlr4 parser...
    input_stream = antlr4.FileStream(argv[1])
    lexer = CypherLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = CypherParser(stream)
    tree = parser.cypher()
    listener = CypherListener()
    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, tree)

    print("Printing node-variables and their new properties:")
    print(listener.to_create)

    # For now, just print the parse tree
    print("\nHere is the whole parse tree...")
    print(antlr4.tree.Trees.Trees.toStringTree(tree, None, parser))


if __name__ == '__main__':
    main(sys.argv)