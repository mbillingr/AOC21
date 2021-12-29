import random


def main():
    with open('inputs/day24.txt') as fd:
        program = parse_assignments(fd, 'z')

    # create reference outputs to make sure my program transformations don't break anything
    digits = [[random.randint(1, 9) for _ in range(14)] for _ in range(1000)]
    refs = [evaluate(program, d) for d in digits]

    # run an optimization pass to get rid of a few branches and make the program more
    # compact in general. This speeds up branch expansion considerably.
    program = optimize(program)

    # replace equality checks with branches. The condition variables become constants
    # in each branch and enable further optimizations
    program = expand_branches(program)

    # optimize the branched program. Now it is possible to simplify expressions of the form
    #   (x * a + y) % a  => y
    #   (x * a + y) // a  => x
    program = optimize(program)

    # get rid of all registers and create a single expression.
    program = inline_variables(program)

    # the program should behave the same as the original program.
    for d, expected in zip(digits, refs):
        assert evaluate(program, d) == expected

    # convert the program into an expression that is True when the program would return zero.
    checker = is_zero(program)

    # simplify the checker
    checker = simplify_logic(checker)

    # find the largest input that satisfies the checker expression
    part1 = maximize(checker, [None]*14)
    print('Day 24, Part 1:', ''.join(map(str, part1)))

    # find the smallest input that satisfies the checker expression
    part2 = minimize(checker, [None]*14)
    print('Day 24, Part 2:', ''.join(map(str, part2)))


def parse_assignments(code, r_result):
    def next_input():
        nonlocal current_input
        i = current_input
        current_input += 1
        return i
    current_input = 0

    def assign(r, exp):
        assignments.append(('set', r, exp))
    assignments = [('set', 'w', 0), ('set', 'x', 0), ('set', 'y', 0), ('set', 'z', 0)]
    for line in code:
        line = list(line.split())
        try:
            line[2] = int(line[2])
        except IndexError:
            pass
        except ValueError:
            pass
        match line:
            case ['inp', r]:
                assign(r, ('in', next_input()))
            case ['add', a, b]:
                assign(a, add(a, b))
            case ['mul', a, b]:
                assign(a, mul(a, b))
            case ['div', a, b]:
                assign(a, div(a, b))
            case ['mod', a, b]:
                assign(a, mod(a, b))
            case ['eql', a, b]:
                assign(a, eql(a, b))
            case _:
                raise SyntaxError(line)
    expr = ('ret', r_result)
    for stmt in assignments[::-1]:
        expr = ('begin', stmt, expr)
    return expr


def evaluate(exp, inputs, register_values=None):
    if register_values is None:
        register_values = {}

    match exp:
        case ('begin', first, second):
            evaluate(first, inputs, register_values)
            return evaluate(second, inputs, register_values)
        case ('set', r, x):
            register_values[r] = evaluate(x, inputs, register_values)
        case ('ret', x): return evaluate(x, inputs, register_values)
        case int(i): return i
        case str(x): return register_values[x]
        case ('in', i): return inputs[i]

        case ('if', cond, yes, no):
            if evaluate(cond, inputs, register_values) == 1:
                return evaluate(yes, inputs, register_values)
            else:
                return evaluate(no, inputs, register_values)

        case (op, a, b):
            a = evaluate(a, inputs, register_values)
            b = evaluate(b, inputs, register_values)
            match op:
                case '+': return a + b
                case '-': return a - b
                case '*': return a * b
                case '/': return a // b
                case '%': return a % b
                case '==': return a == b
                case '!=': return a != b
                case _: raise NotImplementedError(op)
        case _: raise NotImplementedError(exp)


def optimize(exp):
    match exp:
        # unneeded assignment like z := z
        case('begin', ('set', r, z), rest) if r == z: return optimize(rest)

        # constant inlining
        case ('begin', ('set', c, int(a)), rest):
            return optimize(replace(rest, c, a))

        # negated equality check
        case ('begin', ('set', c, ('==', a, b)),
                       ('begin', ('set', z, ('==', x, 0)),
                                 rest)) if c == x:
            return optimize(('begin', ('set', z, ('!=', a, b)), rest))

        # immediately overwritten alias
        case ('begin', ('set', c, str(a)),
                       ('begin', ('set', z, (op, x, y)),
                                 rest)) if c == z:
            x = replace(x, c, a)
            y = replace(y, c, a)
            return optimize(('begin', ('set', z, (op, x, y)), rest))

        # irrefutable condition (assuming w always holds an input value in range 1...9)
        case ('begin', ('set', c, ('+', a, int(b))),
                       ('begin', ('set', z, ('==', x, 'w')),
                                 rest)) if b >= 10:
            return optimize(('begin', ('set', z, 0), rest))

        case ('begin', first, second):
            a = optimize(first)
            if a != first:
                return optimize(('begin', a, second))
            return ('begin', a, optimize(second))

        case ('set', var, val):
            return ('set', var, optimize(val))

        case ('if', cond, yes, no):
            return ('if', cond, optimize(yes), optimize(no))

        case ('+', 0, b): return b
        case ('+', a, 0): return a
        case ('+', int(a), int(b)): return a + b
        case ('*', 1, b): return b
        case ('*', a, 1): return a

        case ('*', 0, _): return 0
        case ('*', _, 0): return 0
        case ('*', int(a), int(b)): return a * b
        case ('%', 0, _): return 0
        case ('==', int(a), int(b)): return int(a == b)

        case _: return exp


def inline_variables(exp):
    match exp:
        case ('if', c, a, b):
            return ('if', c, inline_variables(a), inline_variables(b))
        case ('begin', ('set', var, ('!=', _, _)) as first, rest):
            return ('begin', first, inline_variables(rest))
        case ('begin', ('set', var, val), rest):
            return inline_variables(replace(rest, var, val))
        case ('begin', first, second):
            return ('begin', first, inline_variables(second))
        case _: return exp


def expand_branches(exp):
    match exp:
        case ('begin', ('set', var, ('=='|'!='as cmp, a, b)), rest):
            rest = expand_branches(rest)
            eq_branch = ('begin', ('set', var, 1), rest)
            ne_branch = ('begin', ('set', var, 0), rest)
            return ('if', (cmp, a, b), eq_branch, ne_branch)
        case ('begin', first, second):
            return ('begin', first, expand_branches(second))
        case _: return exp


def replace(exp, r, val):
    match exp:
        case int(_) | ('in', _): return exp
        case str(s):
            return val if s == r else s
        case ('ret', x):
            return ('ret', replace(x, r, val))
        case ('begin', ('set', var, a), rest) if var == r:
            a = replace(a, r, val)
            return ('begin', ('set', var, a), rest)
        case ('begin', first, second):
            return ('begin', replace(first, r, val), replace(second, r, val))
        case ('if', c, a, b):
            return ('if', replace(c, r, val), replace(a, r, val), replace(b, r, val))
        case ('+', a, int(b)):
            match replace(a, r, val):
                case ('+', c, int(d)): return ('+', c, b+d)
                case other: return ('+', other, b)
        case ('/', a, int(b)):
            match replace(a, r, val):
                case int(i): return i // b
                case ('in', _) if b > 9: return 0
                case ('+', ('*', x, m), k) if m == b and highest_possible_value(k) < b:
                    return x
                case other: return ('/', other, b)
        case ('%', a, int(b)):
            match replace(a, r, val):
                case int(i): return i % b
                case ('in', _) if b > 9: return val
                case ('+', ('*', _, m), x) if m == b:
                    return x
                case other: return ('%', other, b)
        case (op, a, b):
            return (op, replace(a, r, val), replace(b, r, val))
        case _: raise NotImplementedError(exp)


def highest_possible_value(exp):
    match exp:
        case int(i): return i
        case ('in', _): return 9
        case ('+', a, b): return highest_possible_value(a) + highest_possible_value(b)
        case _: raise NotImplementedError(exp)


def is_zero(exp):
    match exp:
        case 0: return True
        case int(_): return False
        case ('in', _): return False
        case ('if', c, a, b): return ('if', c, is_zero(a), is_zero(b))
        case ('ret', x): return is_zero(x)
        case ('+', a, b): return ('and', is_zero(a), is_zero(b))
        case ('*', a, b): return ('or', is_zero(a), is_zero(b))
        case _: raise NotImplementedError(exp)


def simplify_logic(exp):
    match exp:
        case bool(b): return b
        case ('if', ('!=', l, r), a, b):
            return simplify_logic(('if', ('==', l, r), b, a))
        case ('if', c, True, False): return c
        case ('if', c, a, False): return simplify_logic(('and', c, a))
        case ('if', _, a, b) if a == b: return a
        case ('if', c, a, b):
            a_ = simplify_logic(a)
            b_ = simplify_logic(b)
            if a_ == a and b_ == b:
                return exp
            else:
                return simplify_logic(('if', c, a_, b_))
        case ('and', bool(a), bool(b)): return a and b
        case ('and', a, True): return simplify_logic(a)
        case ('and', _, False): return False
        case ('and', a, b):
            a_ = simplify_logic(a)
            b_ = simplify_logic(b)
            if a_ == a and b_ == b:
                return exp
            else:
                return simplify_logic(('and', a_, b_))
        case ('or', bool(a), bool(b)): return a or b
        case ('or', a, False): return simplify_logic(a)
        case ('or', _, True): return False
        case ('or', a, b):
            a_ = simplify_logic(a)
            b_ = simplify_logic(b)
            if a_ == a and b_ == b:
                return exp
            else:
                return simplify_logic(('or', a_, b_))
        case ('==', _, _): return exp
        case _: raise NotImplementedError(exp)


def maximize(exp, inputs):
    match exp:
        case ('and', a, b):
            maximize(a, inputs)
            maximize(b, inputs)
        case ('==', ('+', ('in', a), d), ('in', b)):
            if d >= 0:
                inputs[b] = 9
                inputs[a] = 9 - d
            else:
                inputs[a] = 9
                inputs[b] = 9 + d
        case _: raise NotImplementedError(exp)
    return inputs


def minimize(exp, inputs):
    match exp:
        case ('and', a, b):
            minimize(a, inputs)
            minimize(b, inputs)
        case ('==', ('+', ('in', a), d), ('in', b)):
            if d >= 0:
                inputs[a] = 1
                inputs[b] = 1 + d
            else:
                inputs[a] = 1 - d
                inputs[b] = 1
        case _: raise NotImplementedError(exp)
    return inputs


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


def mul(a, b):
    match a, b:
        case _, 0: return 0
        case 0, _: return 0
        case a, 1: return a
        case 1, b: return b
        case int(a), int(b): return a * b
        case _: return ('*', a, b)


def div(a, b):
    match a, b:
        case a, 0: raise ValueError()
        case a, 1: return a
        case 0, _: return 0
        case int(a), int(b): return a // b
        case _: return ('/', a, b)


def mod(a, b):
    match a, b:
        case a, 0: raise ValueError()
        case a, 1: return 0
        case 0, _: return 0
        case int(a), int(b): return a % b
        case _: return ('%', a, b)


def eql(a, b):
    match a, b:
        case a, b if a == b: return 1
        case int(a), int(b): return int(a == b)
        case _: return ('==', a, b)


if __name__ == "__main__":
    main()
