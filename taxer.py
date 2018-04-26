import lexer
import sys

ATOM = 0
CONTENT = 1
LINE = 2

tokens = []


def check_atom(token, string):
    return token[ATOM] == string


def main(filepath):
    global tokens
    tokens = lexer.main(filepath)
    print(tokens)


def typebase(count):
    b1 = tokens[count][ATOM] in ['INT', 'DOUBLE', 'CHAR']
    b2 = check_atom(count, 'STRUCT') and check_atom(count + 1, 'ID')
    return (b1 or b2, count)


def decl_var(count):
    typebase = type_base(count)



def decl_func(count):
    pass


def decl_struct(count):
    if check_atom(tokens[count], 'STRUCT'):
        count += 1
    else:
        raise Exception("Invalid syntax at line %s" % tokens[count][LINE])

    if check_atom(tokens[count], 'ID'):
        count += 1
    else:
        raise Exception("Invalid syntax at line %s" % tokens[count][LINE])
    if check_atom(tokens[count], 'LACC'):
        count += 1
    elif check_atom(tokens[count], 'SEMICOLON'):
            return True
    while decl_var(count):
        count += 1
    if check_atom(tokens[count], 'RACC'):
        count += 1
    else:
        raise Exception("Invalid syntax at line %s" % tokens[count][LINE])
    if check_atom(tokens[count], 'SEMICOLON'):
        count += 1
    else:
        raise Exception("Invalid syntax at line %s" % tokens[count][LINE])
    return True


def unit(count):
    while tokens[count][ATOM] != 'END':
        if (decl_var(count) or
                decl_func(count) or decl_var(count)):
            count += 1
        else:
            raise Exception("Invalid syntax at line %s" % tokens[count][LINE])


if __name__ == '__main__':
    main(sys.argv[1])
