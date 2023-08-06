import os
from lark import Lark, Tree, Token
import unittest

if os.environ.get("DEV_PBAT") == "1":
    base = os.path.dirname(__file__)
    path = os.path.join(base, "def.lark")
    with open(path, encoding='utf-8') as f:
        GRAMMAR = f.read()
else:
    GRAMMAR = """
start: "def" defname attr*

?attr: then | depends | shell

then.1: "then" NAME

depends: "depends" "on" NAME+

shell: "shell" NAME

defname: NAME

NAME: /[a-z0-9_-]+/i

WS: /[ \\t\\f\\r\\n]/+

%ignore WS
"""

parser = Lark(GRAMMAR)

def find_data(tree, data, trace = False):
    return [child for child in tree.children if hasattr(child, 'data') and child.data == data]

def parse_def(def_):
    name = None
    then = None
    depends = []
    shell = None
    tree = parser.parse(def_)

    for item in find_data(tree, 'defname'):
        name = item.children[0].value
    for item in find_data(tree, 'then'):
        then = item.children[0].value
    for item in find_data(tree, 'depends'):
        values = [ch.value for ch in item.children]
        depends += values
    for item in find_data(tree, 'shell'):
        shell = item.children[0].value

    return name, then, depends, shell

class TestParse(unittest.TestCase):
    def test1(self):
        def_ = 'def baz depends on foo bar then qux shell corge'
        expected = 'baz', 'qux', ['foo', 'bar'], 'corge'
        self.assertEqual(expected, parse_def(def_))
    def test2(self):
        def_ = 'def third depends on second'
        expected = 'third', None, ['second'], None
        self.assertEqual(expected, parse_def(def_))
    def test3(self):
        def_ = 'def second shell msys2'
        expected = 'second', None, [], 'msys2'
        self.assertEqual(expected, parse_def(def_))
    def test4(self):
        def_= 'def main then second'
        expected = 'main', 'second', [], None
        self.assertEqual(expected, parse_def(def_))

if __name__ == '__main__':
    unittest.main()