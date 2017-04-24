import sys
import antlr4
from CypherLexer import CypherLexer
from CypherParser import CypherParser

def main(argv):
    # Set up antlr4 parser...
    input_stream = antlr4.FileStream(argv[1])
    lexer = CypherLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = CypherParser(stream)
    tree = parser.cypher()

    # For now, just print the parse tree
    print("Here it comes!")
    print(antlr4.tree.Trees.Trees.toStringTree(tree, None, parser))


if __name__ == '__main__':
    main(sys.argv)