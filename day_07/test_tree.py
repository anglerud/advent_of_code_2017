"""
                gyxo
              /     
         ugml - ebii
       /      \     
      |         jptl
      |        
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |             
      |         ktlj
       \      /     
         fwft - cntj
              \     
                xhth
"""
import io
import operator

import tree


test_data = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""


def test_program_from_line_alone() -> None:
    """Test a program not holding anyone up."""
    p = tree.Program.from_line('cntj (57)')
    assert p.name == 'cntj'
    assert p.weight == 57


def test_program__from_line_stack() -> None:
    """ """
    p = tree.Program.from_line('ugml (68) -> gyxo, ebii, jptl')
    assert p.name == 'ugml'
    assert p.weight == 68


def test_first_layer() -> None:
    """ """
    programs = tree.load(io.StringIO(test_data))
    base = programs['tknk']
    holds = list(map(operator.attrgetter('name'), base.holds))

    assert list(sorted(holds)) == ['fwft', 'padx', 'ugml']


def test_second_layer() -> None:
    """ """
    programs = tree.load(io.StringIO(test_data))
    base = programs['ugml']
    holds = list(map(operator.attrgetter('name'), base.holds))

    assert list(sorted(holds)) == ['ebii', 'gyxo', 'jptl']


def test_top_layer() -> None:
    """ """
    programs = tree.load(io.StringIO(test_data))
    base = programs['gyxo']
    holds = list(map(operator.attrgetter('name'), base.holds))

    assert list(sorted(holds)) == []


def test_find_bottom_of_tree() -> None:
    """ """
    programs = tree.load(io.StringIO(test_data))
    assert tree.find_bottom_of_tree(programs).name == 'tknk'


def test_find_imbalanced_program() -> None:
    """ """
    programs = tree.load(io.StringIO(test_data))
    print(programs)
    bottom = tree.find_bottom_of_tree(programs)

    program, weight = tree.find_wrong_weight(bottom)
    assert program.name == 'ugml'
    assert weight == 60

