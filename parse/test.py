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
    visitor = CypherVisitor()
    visitor.visit(tree)


if __name__ == '__main__':
    main(sys.argv)