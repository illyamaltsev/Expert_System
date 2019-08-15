import sys

from utils.reader import read_all
from utils.lexer import lex
from utils.parser import parse, build_graph
from utils.drawer import draw_graph


def main(argc, argv):
    filename = 'test.txt'
    f_content = read_all(filename)
    tokens = lex(f_content)
    parsed = parse(tokens)

    graph = build_graph(parsed["graph_body"])
    draw_graph(graph, parsed["rules"])


main(len(sys.argv), sys.argv)
