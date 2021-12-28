from collections import deque
import itertools
from puzzle import Puzzle


class Day24(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 24, Part {part}")


class Part1(Day24):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        code = SSABuilder(input)
        code.compute_ranges()
        print(code.eval(code.get('z'), [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 0, 0, 0]))
        code.optimize(code.get('z'))
        print(code.eval(code.get('z'), [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5]))

        assignments = self.rename(code.assignments)

        self.make_rust(assignments)

        for r, exp in code.assignments.items():
            print(r, '=', exp)

        self.code = code

        #constraints = {r: None for r in self.code.assignments}
        #for solution in self.constrain(constraints, self.code.get('z'), 0):
        #    print(solution)
        #for solution in self.substitute({}, self.code.get('z'), 0):
        #    print('*', solution)

    def substitute(self, substitution, r, value):
        if r in substitution:
            if substitution[r] == value:
                # tautology
                yield substitution
            else:
                #contradiction
                return

        r = self.walk(substitution, r)
        value = self.walk(substitution, value)

        substitution = insert(substitution, r, value)

        match (self.code.lookup(r), value):
            case (('in', _), 0):
                return  # impossible
            case (('in', i), int(c)):
                yield insert(substitution, f'in{i}', c)
            case (('in', i), str(r)):
                substitution = insert(substitution, r, f'in{i}')
                for n in range(1, 10):
                    yield insert(substitution, f'in{i}', n)
            case (str(r), int(c)):
                yield from self.equals(substitution, r, c)
            case (('+', a, b), 0):
                # assuming all intermediate values are positive
                yield from conj(self.equals(substitution, b, 0),
                                self.equals(substitution, a, 0))
            case (('+', a, b), c):
                yield from self.equals(substitution, a, sub(c, b))
            case (('*', a, b), 0):
                yield from disj(self.equals(substitution, b, 0),
                                self.equals(substitution, a, 0))
            case (('*', a, b), c):
                yield from self.equals(substitution, a, div(c, b))
            case (('/', a, int(_)), 0):
                yield from self.equals(substitution, a, 0)
            case (('%', a, int(b)), c):
                for n in natural_numbers():
                    yield from self.equals(substitution, a, add(n * b, c))
            case (('!=', a, int(b)), 0):
                yield from self.equals(substitution, a, b)
            case (('!=', a, b), 0):
                yield from self.equals(substitution, b, a)
            case exp: raise NotImplementedError(exp, substitution)

    def equals(self, substitution, a0, b0):
        a = self.walk(substitution, a0)
        b = self.walk(substitution, b0)
        match a, b:
            case int(a), int(b) if a == b:
                yield substitution
            case int(a), int(b) if a != b:
                return
            case str(a), int(b):
                yield from self.substitute(substitution, a, b)
            case str(a), str(b):
                yield from self.substitute(substitution, a, b)
            case str(a), ('-', _, _):
                yield from self.substitute(substitution, a, b)
            case str(a), ('/', _, _):
                yield from self.substitute(substitution, a, b)
            case other: raise NotImplementedError(other, substitution)

    def walk(self, substitution, v):
        match v:
            case str(x):
                if x in substitution:
                    return self.walk(substitution, x)
                else:
                    return x
            case int(i): return i
            case ('-', a, b):
                a = self.walk(substitution, a)
                b = self.walk(substitution, b)
                if isinstance(a, int) and isinstance(b, int):
                    return a - b
                else:
                    return v
            case ('/', a, b):
                a = self.walk(substitution, a)
                b = self.walk(substitution, b)
                if isinstance(a, int) and isinstance(b, int):
                    return a // b
                else:
                    return v
            case _: raise NotImplementedError(v)

    def constrain(self, constraints, r, force):
        def add_constraint(r, constraint):
            match constraints[r], constraint:
                case (None, c):
                    result = c
                case other:
                    raise NotImplementedError(other)
            return constraints | {r: result}

        #constraints = add_constraint(r, constraint)
        constraints |= {r: ('==', force)}

        match (self.code.lookup(r), constraints[r]):
            case (('+', a, b), ('==', 0)):
                # assuming all intermediate values are positive
                yield from conj(self.constrain(constraints, b, 0),
                                self.constrain(constraints, a, 0))
            case (('*', a, b), ('==', 0)):
                yield from disj(self.constrain(constraints, b, 0),
                                self.constrain(constraints, a, 0))
            #case (('!=', 'x82', 'w14'), ('==', 0)):
            case exp: raise NotImplementedError(exp)

    def solve_backward(self, exp1, op, exp2):
        print(exp1, op, exp2)
        match exp1, op, exp2:
            case ('in', _), '==', b: return self.solve_backward(a, '==', ('do', exp1))
            case a, op, ('in', _): return self.solve_backward(a, op, ('do', exp2))
            case 0, '==', 0: return True
            case int(_), '==', 0: return False
            case 0, '==', int(_): return False
            case str(r), op, b: return self.solve_backward(self.assignments[r], op, b)
            case a, op, str(r): return self.solve_backward(a, op, self.assignments[r])
            case ('+', a, int(b)), '==', c:
                return self.solve_backward(a, '==', c - b)
            case ('+', int(a), b), '==', c:
                return self.solve_backward(b, '==', c - a)
            case ('+', a, b), '==', 0:
                return ('and',
                    self.solve_backward(b, '==', 0),
                    self.solve_backward(a, '==', 0))
            case ('+', a, int(b)), '==', ('do', c):
                return self.solve_backward(a, '==', ('do', ('-', c, b)))
            case ('*', a, b), '==', 0:
                return ('or',
                    self.solve_backward(b, '==', 0),
                    self.solve_backward(a, '==', 0))
            case ('/', a, int(b)), '==', 0:
                return self.solve_backward(a, "<", b)
            case ('%', a, int(b)), '==', ('do', c):
                return self.solve_backward(a, '==', ('do', ('%-inv', c, b)))
            case ('==', a, b), '==', 0:
                return self.solve_backward(a, '!=', b)
            case ('!=', a, b), '==', 0:
                return self.solve_backward(a, '==', b)
            case ('==', a, b), '!=', 0:
                return self.solve_backward(a, '==', b)

            case _: raise NotImplementedError(f'{exp1} {op} {exp2}')

    def rename(self, assignments):
        cmds = []
        for var, exp in assignments.items():
            match exp:
                case ('in', i):
                    pass
                case (op, str(a), str(b)):
                    exp = (op, a[0], b[0])
                case (op, str(a), b):
                    exp = (op, a[0], b)
                case (op, a, str(b)):
                    exp = (op, a, b[0])
                case (op, a, b):
                    exp = (op, a, b)
                case int(c): exp = c
                case str(r): exp = r[0];
                case _: raise NotImplementedError(exp)
            cmds.append((var[0], exp))
        return cmds

    def make_rust(self, assignments):
        cmds = []
        for var, exp in assignments:
            match exp:
                case ('in', i):
                    val = f'input[{i}]'
                case ('+', a, b):
                    val = f'{a} + {b}'
                case ('*', a, b):
                    val = f'{a} * {b}'
                case ('/', a, b):
                    val = f'{a} / {b}'
                case ('%', a, b):
                    val = f'{a} % {b}'
                case ('==', a, b):
                    val = f'if {a} == {b} {{ 1 }} else {{ 0 }}'
                case ('!=', a, b):
                    val = f'if {a} != {b} {{ 1 }} else {{ 0 }}'
                case int(c): val = c
                case str(r): val = r
                case _: raise NotImplementedError(exp)
            cmds.append(f'let {var} = {val};')
            print(cmds[-1])
        return cmds


class Analyze:
    def __init__(self, code, registers='wxyz'):
        self.registers = {r: 0 for r in registers}
        for line in code:
            line = list(line.split())
            try:
                line[2] = int(line[2])
            except IndexError:
                pass
            except ValueError:
                pass
            self.analyze(line)

    def analyze(self, line):
        match line:
            case ['inp', r]:
                self.assign(r, self.next_input())
            case ['add', a, int(b)]:
                self.assign(a, self.add(self.get(a), b))
            case ['add', a, b]:
                self.assign(a, self.add(self.get(a), self.get(b)))
            case ['mul', a, int(b)]:
                self.assign(a, self.mul(self.get(a), b))
            case ['mul', a, b]:
                self.assign(a, self.mul(self.get(a), self.get(b)))
            case ['div', a, int(b)]:
                self.assign(a, self.div(self.get(a), b))
            case ['div', a, b]:
                self.assign(a, self.div(self.get(a), self.get(b)))
            case ['mod', a, int(b)]:
                self.assign(a, self.mod(self.get(a), b))
            case ['mod', a, b]:
                self.assign(a, self.mod(self.get(a), self.get(b)))
            case ['eql', a, int(b)]:
                self.assign(a, self.eql(self.get(a), b))
            case ['eql', a, b]:
                self.assign(a, self.eql(self.get(a), self.get(b)))
            case _: raise SyntaxError(line)


class SSABuilder(Analyze):
    def __init__(self, code, registers='wxyz'):
        self.n_inputs = 0
        self.register_versions = {r: -1 for r in registers}
        self.assignments = {}
        for r in registers:
            self.assign(r, 0)
        super().__init__(code, registers)

    def eval(self, r_out, inputs):
        register_values = {}
        for r, exp in self.assignments.items():
            match exp:
                case int(i): val = i
                case str(x): val = register_values[x]
                case ('in', i): val = inputs[i]
                case ('+', a, int(b)): val = register_values[a] + b
                case ('+', a, b): val = register_values[a] + register_values[b]
                case ('*', a, int(b)): val = register_values[a] * b
                case ('*', int(a), b): val = a * register_values[b]
                case ('*', a, b): val = register_values[a] * register_values[b]
                case ('/', a, int(b)): val = register_values[a] // b
                case ('/', a, b): val = register_values[a] // register_values[b]
                case ('==', a, int(b)): val = 1 if register_values[a] == b else 0
                case ('==', a, b): val = 1 if register_values[a] == register_values[b] else 0
                case ('!=', a, int(b)): val = 1 if register_values[a] != b else 0
                case ('!=', a, b): val = 1 if register_values[a] != register_values[b] else 0
                case ('%', a, int(b)): val = register_values[a] % b
                case _: raise NotImplementedError(exp)
            register_values[r] = val
        return register_values[r_out]

    def optimize(self, r_result):
        assignments = None
        while self.assignments != assignments:
            assignments = self.assignments
            self.inline_trivial_assignments()
            self.fold_constants()
            self.peephole()
        self.remove_unused(r_result)

    def peephole(self):
        assignments = {}
        for r, exp in self.assignments.items():
            match self.expand(exp):
                case ('==', ('==', a, b), 0):
                    exp = ('!=', a, b)
                #case ('==', int(c), ('in', _)) if not 1 <= c <= 9 :
                #    exp = 0
                case ('!=', int(c), ('in', _)) if not 1 <= c <= 9 :
                    exp = 1
                case ('!=', ('+', _, c), ('in', _)) if c >= 10:
                    exp = 1
                case ('%', ('in', i), int(c)) if c > 10 :
                    exp = exp[1]
                case _: pass

            match self.expand(exp, 2):
                case ('%', ('+', ('*', _, f), b), g) if f == g:
                    exp = b
                case _: pass

            assignments[r] = exp
        self.assignments = assignments

    def expand(self, exp, n=1):
        match exp:
            case int(_): return exp
            case str(_): return self.lookup(exp)
            case ('in', _): return exp
            case (op, a, b) if n > 0: return (op, self.expand(self.lookup(a), n-1), self.expand(self.lookup(b), n-1))
            case _: return exp

    def lookup(self, x):
        match x:
            case int(_): return x
            case str(_): return self.assignments[x]
            case _: raise NotImplementedError(x)

    def fold_constants(self):
        assignments = {}
        for r, exp in self.assignments.items():
            match exp:
                case ('+', 0, b): exp = b
                case ('+', a, 0): exp = a
                case ('+', int(a), int(b)):
                    exp = a + b
                case ('*', 1, b): exp = b
                case ('*', a, 1): exp = a
                case ('*', 0, b): exp = 0
                case ('*', a, 0): exp = 0
                case ('*', int(a), int(b)):
                    exp = a + b
                case ('/', a, 1): exp = a
                case ('/', int(a), int(b)):
                    exp = a + b
                case ('%', int(a), int(b)):
                    exp = a % b
                case ('==', int(a), int(b)):
                    exp = 1 if a == b else 0
                case _: pass
            assignments[r] = exp
        self.assignments = assignments

    def inline_trivial_assignments(self):
        constants = {}
        for r, exp in self.assignments.items():
            match exp:
                case int(_) | str(_): constants[r] = exp

        assignments = {}
        for r, exp in self.assignments.items():
            match exp:
                case (*_,):
                    exp = tuple(constants[x] if x in constants else x for x in exp)
                case str(x) if x in constants:
                    exp = constants[x]
            assignments[r] = exp
        self.assignments = assignments

    def remove_unused(self, r_result):
        used = set()
        self.visit(r_result, used)
        self.assignments = {r: exp for r, exp in self.assignments.items() if r in used}
        print(len(used))

    def visit(self, key, visited=None, visitor=None):
        if visited is None:
            visited = set()
        self.visit_(key, visited)

    def visit_(self, key, visited):
        if key in visited:
            return
        visited.add(key)
        exp = self.assignments[key]
        match exp:
            case('in', _):
                pass
            case (_, int(a), int(b)):
                raise RuntimeError(exp)
            case (_, int(a), b):
                self.visit_(b, visited)
            case (_, a, int(b)):
                self.visit_(a, visited)
            case (_, a, b):
                self.visit_(a, visited)
                self.visit_(b, visited)
            case str(r):
                self.visit_(r, visited)
            case int(r):
                pass
            case _: raise NotImplementedError(f'visit {exp}')

    def compute_ranges(self):
        ranges = {i: (i, i) for i in range(-30, 30)}
        for var, exp in self.assignments.items():
            match exp:
                case ('in', i):
                    vals = (1, 9)
                case ('+', a, b):
                    vals = tuple(av + bv for av, bv in zip(ranges[a], ranges[b]))
                case ('*', a, b):
                    vals = tuple(av * bv for av, bv in zip(ranges[a], ranges[b]))
                case ('/', a, b):
                    vals = tuple(av // bv for av, bv in zip(ranges[a], ranges[b][::-1]))
                case ('%', a, int(b)):
                    vals = (0, b - 1)  # todo: range may be smaller depending on 'a'
                case ('==', a, b):
                    vals = (0, 1)
                case ('!=', a, b):
                    vals = (0, 1)
                case int(c):
                    vals = (c, c)
                case str(r):
                    vals = ranges[r]
                case _:
                    raise NotImplementedError(exp)
            ranges[var] = vals
            self.value_ranges = ranges
        return ranges

    def assign(self, r, x):
        i = self.register_versions[r] + 1
        self.register_versions[r] = i
        self.assignments[f'{r}{i}'] = x

    def get(self, r):
        return f'{r}{self.register_versions[r]}'

    def next_input(self):
        i = self.n_inputs
        self.n_inputs += 1
        return ('in', i)

    def add(self, x, y):
        match x, y:
            case x, 0: return x
            case 0, y: return y
            case int(x), int(y): return x + y
            case ('+', x, int(y)), int(z): return ('+', x, y + z)
            case ('+', int(x), y), int(z): return ('+', y, x + z)
            case _: return ('+', x, y)

    def mul(self, x, y):
        match x, y:
            case x, 0: return 0
            case 0, y: return 0
            case x, 1: return x
            case 1, y: return y
            case int(x), int(y): return x * y
            case ('*', x, int(y)), int(z): return ('*', x, y * z)
            case ('*', int(x), y), int(z): return ('*', y, x * z)
            case _: return ('*', x, y)

    def div(self, x, y):
        match x, y:
            case x, 1: return x
            case int(x), int(y): return x // y
            case ('/', x, int(y)), int(z): return ('/', x, y * z)
            case _: return ('/', x, y)

    def mod(self, x, y):
        match x, y:
            case x, 1: return 0
            case int(x), int(y): return x % y
            case _: return ('%', x, y)

    def eql(self, x, y):
        match x, y:
            case int(x), int(y): return 1 if x == y else 0
            case ('==', x, y), int(1): return ('==', x, y)
            case ('==', x, y), int(0): return ('!=', x, y)
            case _: return ('==', x, y)


def add(a, b):
    match a, b:
        case a, 0: return a
        case 0, b: return b
        case int(a), int(b): return a + b
        case _: return ('+', a, b)


def sub(a, b):
    match a, b:
        case a, 0: return a
        case 0, int(b): return -b
        case int(a), int(b): return a - b
        case _: return ('-', a, b)


def div(a, b):
    match a, b:
        case a, 0: raise ValueError()
        case a, 1: return a
        case 0, _: return 0
        case int(a), int(b): return a // b
        case _: return ('/', a, b)


def disj(*args):
    for a in args:
        yield from a


def conj(*args):
    for x in itertools.product(*args):
        substitution = {}
        for s in x:
            for k, v in s.items():
                assert k not in substitution
                substitution = insert(substitution, k, v)
        yield substitution


def insert(substitution, r, value):
    def replace(v):
        match v:
            case int(v): return v
            case str(v) if v == r: return value
            case _: raise NotImplementedError(v)

    sub_out = {r: value}
    for k, v in substitution.items():
        sub_out[k] = replace(v)
    return sub_out


def natural_numbers():
    n = 0
    while True:
        yield n
        n += 1


def main():
    #Part1().check(TEST1, 39)
    #Part1().check(EXAMPLE3, 39)
    Part1().run("inputs/day24.txt")


if __name__ == "__main__":
    EXAMPLE1 = """inp x
mul x -1"""

    EXAMPLE2 = """inp z
inp x
mul z 3
eql z x
"""

    EXAMPLE3 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""

    TEST1 = """inp w
eql w 3
eql w 0
inp z
eql z 3
eql z 0
mul z w"""

    main()
