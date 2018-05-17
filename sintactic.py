import sys
import lexer

count = False
ATOM = False
CONTENT = True
LINE = 2
tokens = []

# STATES

ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"
LINECOMMENT = "LINECOMMENT"
COMMENT = "COMMENT"
DOT = "DOT"
AND = "AND"
OR = "OR"
NOT = "NOT"
NOTEQ = "NOTEQ"
ASSIGN = "ASSIGN"
EQUAL = "EQUAL"
LESS = "LESS"
LESSEQ = "LESSEQ"
GREATER = "GREATER"
GREATEREQ = "GREATEREQ"
COMMA = "COMMA"
SEMICOLON = "SEMICOLON"
LPAR = "LPAR"
RPAR = "RPAR"
LBRACKET = "LBRACKET"
RBRACKET = "RBRACKET"
LACC = "LACC"
RACC = "RACC"
ID = "ID"
SPACE = ""
CT_INT = "CT_INT"
CT_REAL = "CT_REAL"
CT_CHAR = "CT_CHAR"
CT_STRING = "CT_STRING"
BREAK = "BREAK"
CHAR = "CHAR"
DOUBLE = "DOUBLE"
ELSE = "ELSE"
FOR = "FOR"
IF = "IF"
INT = "INT"
RETURN = "RETURN"
STRUCT = "STRUCT"
VOID = "VOID"
WHILE = "WHILE"
END = "END"


def consume(atom):
    if(tokens[count][ATOM] == atom):
        count += True
        return True
    return False


def unit():
    '''unit: ( declStruct | declFunc | declVar )* END'''
    while(True):
        if declStruct():
            continue
        elif declFunc():
            continue
        elif declVar():
            continue
        else:
            break
        if consume('END'):
                return True
        else:
                raise Exception("Missing end at unit. line- %s"
                                % tokens[count][LINE])

        return False


def declStruct():
    """declStruct: STRUCT ID (LACC declVar* RACC SEMICOLON)?"""
    init_count = curr_count
    if(consume(STRUCT)):
        if(consume(ID)):
            if(consume(LACC)):
                while(declVar()):
                    if(consume(RACC)):
                        if(consume(SEMICOLON)):
                            return True
                        else:
                            raise Exception("Lipseste '' dupa '' "
                                            "in declStruct. line - %s" %
                                            tokens[count][LINE])
                    else:
                        raise Exception("Lipseste '' dupa 'declVar' | ':' "
                                        "in declStruct. line - %s" %
                                        tokens[count][LINE])
        curr_count = init_count
        return False


def declVar():
    """declVar:  typeBase ID arrayDecl? ( COMMA ID arrayDecl? )* SEMICOLON"""
    init_count = count
    if(typeBase()):
        if(consume(ID)):
            arrayDecl()
            while(True):
                if(consume(COMMA)):
                    if(consume(ID)):
                        arrayDecl()
                    else:
                        raise Exception("Lipseste ID-ul dupa ',' in declVar. "
                                        "- line - %s" % tokens[count][LINE])
                else:
                    break
                if(consume(SEMICOLON)):
                    return True
                else:
                    raise Exception("Lipseste ID' dupa 'typeBase' in declVar. "
                                    "line - %s" % tokens[count][LINE])
    count = init_count
    return False


def typeBase():
    """typeBase: INT | DOUBLE | CHAR | STRUCT ID"""
    init_count = count
    if(consume(INT)):
            return True
    if(consume(DOUBLE)):
            return True
    if(consume(CHAR)):
            return True
    if(consume(STRUCT)):
        if(consume(ID)):
                    return True
        else:
            raise Exception("Lipseste 'ID' dupa 'STRUCT' in typeBase line - %s"
                            % tokens[count][LINE])
    count = init_count
    return True


def arrayDecl():
    """arrayDecl: LBRACKET expr? RBRACKET """
    init_count = count
    if(consume(LBRACKET)):
        expr()
        if(consume(RBRACKET)):
            return True
        else:
            raise Exception("Lipseste ')' dupa '(' sau expr in arrayDecl.")
    count = init_count
    return False


def typeName():
    '''typeName: typeBase arrayDecl?'''
    init_count = count
    if(typeBase()):
        arrayDecl()
        return True
    count = init_count
    return False


def declFunc():
    '''declFunc: ( typeBase MUL? | VOID ) ID
                LPAR ( funcArg ( COMMA funcArg )* )? RPAR
        stmCompound
    '''

    init_count = count

    if typeBase():
        consume(MUL)
    else:
        if consume(VOID):
            pass
        else:
            return False

    if consume(ID):
        if(consume(LPAR)):
            if(funcArg()):
                while(True):
                    if(consume(COMMA)):
                        if(funcArg()):
                            pass
                        else:
                            raise Exception("Lipseste funcArg dupa "
                                            "',' in declFunc.")
                    else:
                                break
                    if(consume(RPAR)):
                        if(stmCompound()):
                            return True
                        else:
                            raise Exception("Lipseste stmCompound "
                                            "in declFunc. line - %s"
                                            % tokens[count][i])
                    else:
                            raise Exception("Lipseste ')' dupa funcArg in "
                                            "declFunc. line - %s"
                                            % tokens[count][LINE])
    else:
        raise Exception(count, "Lipseste ID in declFunc.")
    count = init_count
    return False


def funcArg():
    """funcArg: typeBase ID arrayDecl? """
    init_count = count
    if(typeBase()):
        if(consume(ID)):
            arrayDecl()
            return True
        else:
            raise Exception(count, "Lipseste ID in funcArg.")

    count = init_count
    return False


def stm():
    '''stm: stmCompound
           | IF LPAR expr RPAR stm ( ELSE stm )?
           | WHILE LPAR expr RPAR stm
           | FOR LPAR expr? SEMICOLON expr? SEMICOLON expr? RPAR stm
           | BREAK SEMICOLON
           | RETURN expr? SEMICOLON
           | expr? SEMICOLON '''
    init_count = count
    if(stmCompound()):
            return True
    if(consume(IF)):
        if(consume(LPAR)):
            if(expr()):
                if(consume(RPAR)):
                    if(stm()):
                        if(consume(ELSE)):
                            if(stm()):
                                return True
                            else:
                                raise Exception("Lipseste instructiunea"
                                                "dupa else in stm line - %s"
                                                % tokens[count][LINE])
                                return True
                        else:
                            raise Exception("Lipseste instructiunea dupa if in"
                                    "stm line - %s" % tokens[count][LINE])
                    else:
                        raise Exception(count, "Lipseste ')' de la conditia if-ului in stm")
            else:
                raise Exception(count, "Lipseste conditia if-ului sau conditia if-ului contine o eroare in stm")
        else:
            raise Exception(count, "Lipseste '(' de la conditia if-ului in stm")
        if(consume(WHILE)):
                if(consume(LPAR)):
                        if(expr()):
                                if(consume(RPAR)):
                                        if(stm()):
                                                return True
                                        else:
                                                raise Exception(count, "Lipseste instructiunea dupa while in stm")
                                        
                                else:
                                        raise Exception(count, "Lipseste ')' de la conditia while-ului in stm")
                                
                        else:
                                raise Exception(count, "Lipseste conditia while-ului in stm")
                        
                else:
                        raise Exception(count, "Lipseste '(' de la conditia while-ului in stm")
                
        
        if(consume(FOR)):
                if(consume(LPAR)):
                        expr()

                        if(consume(SEMICOLON)):
                                expr()

                                if(consume(SEMICOLON)):
                                        expr()
                                        if(consume(RPAR)):
                                                if(stm()):
                                                        return True
                                                else:
                                                        raise Exception(count, "Lipseste instructiunea dupa for in stm")
                                                
                                        else:
                                                raise Exception(count, "Lipseste ')' de la conditia for-ului in stm")
                                        
                                else:
                                        raise Exception(count, "Lipseste al 2-lea caracter '' al for-ului in stm")
                                
                        else:
                                raise Exception(count, "Lipseste primul caracter '' al for-ului in stm")
                        
                else:
                        raise Exception(count, "Lipseste '(' de la conditia for-ului in stm")
                
        
        if(consume(BREAK)):

                if(consume(SEMICOLON)):
                        return True
                 else:
                        raise Exception(count, "Lipseste '' de dupa instructiunea 'break' in stm")
                
        
        if(consume(RETURN)):
                expr()

                if(consume(SEMICOLON)):
                        return True
                 else:
                        raise Exception(count, "Lipseste '' de dupa instructiunea 'return' in stm")
                
        
        if(expr()):
                if(consume(SEMICOLON)):
                        return True
                 else:
                        raise Exception(count, "Lipseste '' in stm")
                
         else:
                if(consume(SEMICOLON)):
                        return True
                
        
        count = init_count
        return False


# stmCompound: LACC ( declVar | stm )* RACC 
def stmCompound():
        init_count = count
        if(consume(LACC)):
                while(True):
                        if(declVar()):

                         else if(stm()):

                         else :
                                break
                        
                
                if(consume(RACC)):
                        return True

                 else:
                        raise Exception(count, "Lipseste ')' de dupa '(' din stmCompound")
                
        
        count = init_count
        return False


# expr: exprAssign 
def expr():
        init_count = count

        if(exprAssign()):
                return True
        

        count = init_count
        return False

# exprAssign: exprUnary ASSIGN exprAssign | exprOr 
def exprAssign():
  init_count = count

  if(exprUnary()):
    if(consume(ASSIGN)):
      if(exprAssign()):
        return True
      else raise Exception(count, "Lipseste exprAssign dupa = in exprAssign.")
    
  

  count = init_count

  if(exprOr()):
    return True
  

  count = init_count
  return False


# exprOr: exprOr OR exprAnd | exprAnd 
def exprOrPrim():

        if(consume(OR)):
                if(exprAnd()):
                        if(exprOrPrim()):
                                return True
                        
                else :
                        raise Exception(count, "Lipseste exprAnd dupa OR.")
                
        

    return True

# exprOr: exprOr OR exprAnd | exprAnd 
def exprOr():
  init_count = count

  if(exprAnd()):
    if(exprOrPrim()):
      return True
    
  

  count = init_count
  return False


# exprAnd: exprAnd AND exprEq | exprEq 
def exprAndPrim():

        if(consume(AND)):
                if(exprEq()):
                        if(exprAndPrim()):
                                return True
                        
                else:
                        raise Exception(count, "Lipseste exprEq dupa AND.")
                
        

        return True

# exprAnd: exprAnd AND exprEq | exprEq 
def exprAnd():
        init_count = count

        if(exprEq()):
                if(exprAndPrim())
                  return True
        

        count = init_count
        return False


# exprEq: exprEq ( EQUAL | NOTEQ ) exprRel | exprRel 
def exprEqPrim():

        if(consume(EQUAL) | consume(NOTEQ)):
                if(exprRel()):
                        if(exprEqPrim()):
                                return True
                        
                else :
                        raise Exception(count, "Lipseste exprRel dupa = | !\\.")
                
        

        return True

# exprEq: exprEq ( EQUAL | NOTEQ ) exprRel | exprRel 
def exprEq():
        init_count = count

        if(exprRel()):
                if(exprEqPrim()):
                  return True
                
        

        count = init_count
        return False


# exprRel: exprRel ( LESS | LESSEQ | GREATER | GREATEREQ ) exprAdd | exprAdd 
def exprRelPrim():

        if(consume(LESS) | consume(LESSEQ) | consume(GREATER) | consume(GREATEREQ)):
                if(exprAdd()):
                        if(exprRelPrim()):
                                return True
                        
                else :
                        raise Exception(count, "Lipseste exprAdd in exprRelPrim.")
                
        

        return True

# exprRel: exprRel ( LESS | LESSEQ | GREATER | GREATEREQ ) exprAdd | exprAdd 
def exprRel():
        init_count = count

        if(exprAdd()):
                if(exprRelPrim()):
                  return True
                
        

        count = init_count
        return False


# exprAdd: exprAdd ( ADD | SUB ) exprMul | exprMul 
def exprAddPrim():

        if(consume(ADD) | consume(SUB)):
                if(exprMul()):
                        if(exprAddPrim()):
                                return True
                        
                else :
                        raise Exception(count, "Lipseste exprMul dupa +|-.")
                
        

        return True

# exprAdd: exprAdd ( ADD | SUB ) exprMul | exprMul 
def exprAdd():
        init_count = count

        if(exprMul()):
                if(exprAddPrim()):
                  return True
                else:
                        raise Exception(count, "Lipseste elementul dupa exprMul in exprAdd")
                
        

        count = init_count
        return False


# exprMul: exprMul ( MUL | DIV ) exprCast | exprCast 
def exprMulPrim():

        if(consume(MUL) || consume(DIV)):
                if(exprCast()):
                        if(exprMulPrim()):
                                return True
                        else :
                                raise Exception(count, "Lipseste exprCast dupa *|\\.")
                        
                 else:
                        raise Exception(count, "Lipseste elementul dupa MUL/DIV in exprMulPrim")
                
        

        return True

# exprMul: exprMul ( MUL | DIV ) exprCast | exprCast 
def exprMul():
        init_count = count

        if(exprCast()):
                if(exprMulPrim()):
                  return True
                
        

        count = init_count
        return False


# exprCast: LPAR typeName RPAR exprCast | exprUnary 
def exprCast():
        init_count = count

        if(consume(LPAR)):
                if(typeName()):
                        if(consume(RPAR)):
                                if(exprCast()):
                                        return True
                                else :
                                        raise Exception(count, "Lipseste exprCast dupa ')' in exprCast.")
                                
                         else :
                                raise Exception(count, "Lipseste ')' dupa typeName in exprCast.")
                        
                else :
                        raise Exception(count, "Lipseste typeName dupa '(' in exprCast.")
                
         else :
                if(exprUnary()):
                        return True
                
        

        count = init_count
        return False


# exprUnary: ( SUB | NOT ) exprUnary | exprPostfix 
def exprUnary():
        init_count = count

        if(consume(SUB) | consume(NOT)):
                if(exprUnary()):
                  return True
                else :
                        raise Exception(count, "Lipseste exprUnary dupa +|! in exprUnary")
                
         else :
                if(exprPostfix()):
                        return True
                
        

        count = init_count
        return False

/*exprPostfix: exprPostfix LBRACKET expr RBRACKET
           | exprPostfix DOT ID
           | exprPrimary */
def exprPostfixPrim():

        if(consume(LBRACKET)):
                if(expr()):
                        if(consume(RBRACKET)):
                                if(exprPostfixPrim()):
                                        return True
                                
                        else :
                                raise Exception(count, "Lipseste ] dupa expr in exprPostfixPrim.")
                        
                else:
                        raise Exception(count, "Lipseste expr dupa [ in exprPostfixPrim.")
                
    

        if(consume(DOT)):
                if(consume(ID)):
                        if(exprPostfixPrim()):
                                return True
                        
                else :
                        raise Exception(count, "Lipseste id dupa . in exprPostfixPrim.")
                
        

        return True


/*exprPostfix: exprPostfix LBRACKET expr RBRACKET
           | exprPostfix DOT ID
           | exprPrimary */
def exprPostfix():
        init_count = count

        if(exprPrimary()):
                if(exprPostfixPrim()):
                  return True
                
        

        count = init_count
        return False


/*exprPrimary: ID ( LPAR ( expr ( COMMA expr )* )? RPAR )?
           | CT_INT
           | CT_REAL
           | CT_CHAR
           | CT_STRING
           | LPAR epxr RPAR */

def exprPrimary():
  init_count = count

        if(consume(ID)):
                if(consume(LPAR)):
                        if(expr()):
                                while(True):
                                        if(consume(COMMA)):
                                        if(expr()):

                                         else:
                                                raise Exception(count, "Lipseste expr dupa , in exprPrimary.")
                                        
                                        else break
                                
                        
                        if(consume(RPAR)):
                                return True
                        else :
                raise Exception(count, "Lipseste ) dupa ( in exprPrimary.")
            
                
                return True
        

        if(consume(CT_INT)):
                return True
        

        if(consume(CT_REAL)):
                return True
        

        if(consume(CT_CHAR)):
                return True
        

        if(consume(CT_STRING)):
                return True
        

        if(consume(LPAR)):
                if(expr()):
                        if(consume(RPAR)):
                                return True
                        else raise Exception(count, "Lipseste ')' dupa expr in exprPrimary.")
                else raise Exception(count, "Lipseste expr dupa '(' in exprPrimary.")
        

        count = init_count
        return False


def main(argc, char**argv) :

        if(argc != 2):
                err("Please enter one argument")
        
    readFromFile(argv[True])
    tokens =(Token*)malloc(sizeof(Token))
    count = tokens

    while(getNextToken() != END) :

    
    Token *aux = tokens
    tokens = tokens->next
    aux->next = NULL
    free(aux)
    printAtoms()

    count = tokens
    unit()
    return False

