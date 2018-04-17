import sys
import re
import time
import copy
tokens = []
pStartCh = 0
pCrtCh = 0
s = ''
ch = ''
line = 0
state = 0


def convert(aString):
    if aString.startswith("0x") or aString.startswith("0X"):
        return int(aString, 16)
    elif aString.startswith("0"):
        return int(aString, 8)
    else:
        return int(aString)


def getnexttoken():
    global pStartCh
    global pCrtCh
    global tokens
    global s
    global line
    global state
    ch = s[pCrtCh]
    while(1):
        ch = s[pCrtCh]
        print("#%r char=%r(%r) pCrtCh=%r:\n" % (state, ch, ord(ch), pCrtCh))
        if state == 0:
            if(ch == ' ' or ch == '\t' or ch == '\r'):
                pCrtCh += 1
                break
            elif(ch == '\n'):
                pCrtCh += 1
                line += 1
                break
            elif (ch.isalpha() or ch == '_'):
                pStartCh = pCrtCh
                pCrtCh += 1
                state = 1
                break
            elif(ch >= '1' and ch <= '9'):
                pCrtCh += 1
                state = 3
                break
            elif(ch == '0'):
                pCrtCh += 1
                state = 5
                break
            elif(ch == '\''):
                pCrtCh += 1
                state = 16
                break
            elif(ch == '\"'):
                pCrtCh += 1
                state = 20
                break
            elif(ch == ','):
                pCrtCh += 1
                state = 23
                break
            elif(ch == ';'):
                pCrtCh += 1
                state = 24
                break
            elif(ch == '('):
                pCrtCh += 1
                state = 25
                break
            elif(ch == ')'):
                pCrtCh += 1
                state = 26
                break
            elif(ch == '['):
                pCrtCh += 1
                state = 27
                break
            elif(ch == ']'):
                pCrtCh += 1
                state = 28
                break
            elif(ch == '{'):
                pCrtCh += 1
                state = 29
                break
            elif(ch == '}'):
                pCrtCh += 1
                state = 30
                break
            elif(ch == '+'):
                pCrtCh += 1
                state = 31
                break
            elif(ch == '-'):
                pCrtCh += 1
                state = 32
                break
            elif(ch == '*'):
                pCrtCh += 1
                state = 33
                break
            elif(ch == '/'):
                pCrtCh += 1
                state = 34
                break
            elif(ch == '.'):
                pCrtCh += 1
                state = 35
                break
            elif(ch == '&'):
                pCrtCh += 1
                state = 36
                break
            elif(ch == '|'):
                pCrtCh += 1
                state = 38
                break
            elif(ch == '!'):
                pCrtCh += 1
                state = 40
                break
            elif(ch == '='):
                pCrtCh += 1
                state = 43
                break
            elif(ch == '<'):
                pCrtCh += 1
                state = 46
                break
            elif(ch == '>'):
                pCrtCh += 1
                state = 49
                break
            # END
            elif(ch == 0):
                tokens.append(('END', '', line))
                return tokens[-1]
            else:
                pCrtCh += 1
                break
            break
        if state == 1:
            if(ch.isalnum() or ch == '_'):
                pCrtCh += 1
            else:
                state = 2
            break
        if state == 2:
            nCh = pCrtCh-pStartCh
            if(nCh == 5 and s[pStartCh:(pCrtCh)] == "break"):
                tokens.append(('BREAK', '', line))
                pStartCh = pCrtCh
                state = 0
            elif(nCh == 4 and s[pStartCh:(pCrtCh)] == "char"):
                tokens.append(('CHAR', '', line))
                pStartCh = pCrtCh
                state = 0
            elif(nCh == 6 and s[pStartCh:(pCrtCh)] == "double"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('DOUBLE', '', line))
            elif(nCh == 4 and s[pStartCh:(pCrtCh)] == "else"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('ELSE', '', line))
            elif(nCh == 3 and s[pStartCh:(pCrtCh)] == "for"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('FOR', '', line))
            elif(nCh == 2 and s[pStartCh:(pCrtCh)] == "if"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('IF', '', line))
            elif(nCh == 3 and s[pStartCh:(pCrtCh)] == "int"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('INT', '', line))
            elif(nCh == 6 and s[pStartCh:(pCrtCh)] == "return"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('RETURN', '', line))
            elif(nCh == 6 and s[pStartCh:(pCrtCh)] == "struct"):
                pStartCh = pCrtCh
                tokens.append(('STRUCT', '', line))
                state = 0
            elif(nCh == 4 and s[pStartCh:(pCrtCh)] == "void"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('VOID', '', line))
            elif(nCh == 5 and s[pStartCh:(pCrtCh)] == "while"):
                pStartCh = pCrtCh
                state = 0
                tokens.append(('WHILE', '', line))
            else:
                tokens.append(('ID', s[pStartCh:(pCrtCh)], line))
                state = 0
                pStartCh = pCrtCh
            return tokens[-1]

        if state == 3:
            if(ch.isdigit()):
                pCrtCh += 1
            elif(ch == 'e' or ch == 'E'):
                pCrtCh += 1
                state = 12
            elif ch == '.':
                pCrtCh += 1
                state = 10
            else: 
                state = 4
            break
        if state == 4:
            tokens.append(('CT_INT', convert(s[(pStartCh-1):(pCrtCh)]), line))
            state = 0
            pStartCh = pCrtCh
            return tokens[-1]
        if state == 5:
            if(ch == 'x'):
                pCrtCh += 1
                state = 7
            elif (ch == '8' or ch == '9'):
                pCrtCh += 1
                state = 9
            else:
                state = 6
            break
        if state == 6:
            if(ch >= '0' and ch <= '7'):
                pCrtCh += 1
            elif(ch == '.'):
                pCrtCh += 1
                state = 10
            elif(ch == '8' or ch == '9'):
                pCrtCh += 1
                state = 9
            elif(ch == 'e' or ch == 'E'):
                pCrtCh += 1
                state = 12
            else:
                state = 4
                break
        if state == 7:
            if(ch.isdigit() or ch >= 'a' and ch <= 'f' or
                    ch >= 'A' and ch <= 'F'):
                pCrtCh += 1
                state = 8
                break
        if state == 8:
            if(ch.isdigit() or (ch >= 'a' and ch <= 'f') or
                    (ch >= 'A' and ch <= 'F')):
                pCrtCh += 1
            else:
                state = 4
            break
        if state == 9:
            if(ch.isdigit()):
                pCrtCh += 1
            elif(ch == 'e' or ch == 'E'):
                pCrtCh += 1
                state = 12
            elif(ch == '.'):
                pCrtCh += 1
                state = 10
            break
        if state == 10:
            if(ch.isdigit()):
                pCrtCh += 1
                state = 11
            break
        if state == 11:
            if(ch.isdigit()):
                pCrtCh += 1
            elif(ch == 'e' or ch == 'E'):
                pCrtCh += 1
                state = 12
            else:
                state = 15
            break

        if state == 12:
            if(ch == '+' or ch == '-'):
                    pCrtCh += 1
                    state = 13
            else:
                    state = 13
            break
        if state == 13:
            if(ch.isdigit()):
                pCrtCh += 1
                state = 14
            break

        if state == 14:
            if(ch.isdigit()):
                pCrtCh += 1
            else:
                state = 15
            break
        if state == 15:
            tokens.append(('CT_REAL', float(s[(pStartCh-1):(pCrtCh)]), line))
            pStartCh = pCrtCh+1
            state = 0
            return tokens[-1]

        if state == 16:
            if(ch == '\\'):
                pCrtCh += 1
                state = 17
            elif(ch != '\'' or ch != '\\'):
                pCrtCh += 1
                state = 18
            break
        if state == 17:
            if(ch == 'a' or ch == 'b' or ch == 'f' or ch == 'n' or ch == 'r' or
                    ch == 't' or ch == 'v' or ch == '\'' or ch == '?' or
                    ch == '\"' or ch == '\\' or ch == '0'):
                pCrtCh += 1
                state = 18
            break
        if state == 18:
            if(ch == '\''):
                pCrtCh += 1
                state = 19
            break

        if state == 19:
            char_string = s[pStartCh-1:pCrtCh]
            char_string = char_string.replace('\\\\', '\\')
            char_string = char_string.replace('\'', '')
            print('!!!!!!!!!', char_string)
            tokens.append(('CT_CHAR', ord(char_string), line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 20:
            if(ch == '\"'):
                pCrtCh += 1
                state = 22
            elif(ch == '\\'):
                pCrtCh += 1
                state = 21
            elif(ch != '\"' or ch != '\\'):
                pCrtCh += 1
            break

        if state == 21:
            if(ch == 'a' or ch == 'b' or ch == 'f' or ch == 'n' or ch == 'r' or
                    ch == 't' or ch == 'v' or ch == '\'' or ch == '?' or
                    ch == '\"' or ch == '\\' or ch == '0'):
                pCrtCh += 1
                state = 20
            break
        if state == 22:
            stringy = s[(pStartCh-1):(pCrtCh)]
            stringy = stringy.replace('\\\'', '')
            stringy = stringy.replace('\\\"', '')
            tokens.append(('CT_STRING', stringy, line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]

        if state == 23:
            tokens.append(('COMMA', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 24:
            tokens.append(('SEMICOLON', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 25:
            tokens.append(('LPAR', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]

        if state == 26:
            tokens.append(('RPAR', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]

        if state == 27:
            tokens.append(('LBRACKET', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 28:
            tokens.append(('RBRACKET', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 29:
            tokens.append(('LACC', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 30:
            tokens.append(('RACC', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 31:
            tokens.append(('ADD', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 32:
            tokens.append(('SUB', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 33:
            tokens.append(('MUL', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 34:
            if(ch == '/'):
                pCrtCh += 1
                state = 53
            elif(ch == '*'):
                pCrtCh += 1
                state = 54
            else:
                state = 52
            break
        if state == 35:
            tokens.append(('DOT', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 36:
            if(ch == '&'):
                pCrtCh += 1
                state = 37
            break
        if state == 37:
            tokens.append(('AND', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 38:
            if(ch == '|'):
                pCrtCh += 1
                state = 39
            break
        if state == 39:
            tokens.append(('OR', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 40:
            if(ch == '='):
                pCrtCh += 1
                state = 42
            else:
                state = 41
            break
        if state == 41:
            tokens.append(('NOT', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]

        if state == 42:
            tokens.append(('NOTEQ', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 43:
            if(ch == '='):
                pCrtCh += 1
                state = 44
            else:
                state = 45
            break

        if state == 44:
            tokens.append(('EQUAL', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]

        if state == 45:
            tokens.append(('ASSIGN', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 46:
            if(ch == '='):
                pCrtCh += 1
                state = 47
            else:
                state = 48
            break

        if state == 47:
            tokens.append(('LESSEQ', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 48:
            tokens.append('LESS', '', line)
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 49:
            if(ch == '='):
                pCrtCh += 1
                state = 50
            else:
                state = 51
            break
        if state == 50:
            tokens.append(('GREATEREQ', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 51:
            tokens.append(('GREATER', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 52:
            tokens.append(('DIV', '', line))
            pStartCh = pCrtCh + 1
            state = 0
            return tokens[-1]
        if state == 53:
            if(ch == '\n' or ch == '\r' or ch == '\0'):
                state = 0
            else:
                pCrtCh += 1
            break
        if state == 54:
            if(ch == '*'):
                pCrtCh += 1
                state = 55
            elif(ch == '\n'):
                line += 1
                pCrtCh += 1
            else:
                pCrtCh += 1
            break
        if state == 55:
            if(ch == '*'):
                pCrtCh += 1
            elif(ch == '/'):
                pCrtCh += 1
                state = 0
            elif(ch == '\n'):
                pCrtCh += 1
                line += 1
            else:
                state = 54
                pCrtCh += 1
            break


def main(filepath):
    global s
    with open(filepath) as fisier:
        sir = fisier.readlines()
        for el in sir:
            s += el
    global pCrtCh
    global pStartCh
    global ch
    length = len(s)
    while pCrtCh < length - 1:
        getnexttoken()
    tokens.append(('END', '', line))


if __name__ == '__main__':
    main(sys.argv[1])
    for token in tokens:
        print("atom=%s " % token[0], end='')
        if token[1]:
            if type(token[1]) == str:
                stringer = token[1].replace('\\t', '\t')
                stringer = stringer.replace('\\n', '\n')
                print("content=%s " % stringer, end='')
            else:
                print("content=%s " % token[1], end='')
        else:
            print("", end='')
        try:
            print('line=%s' % token[2])
        except:
            print("EXCEPTIE LA %s" % token)
