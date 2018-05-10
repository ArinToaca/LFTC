import lexer
import sys

count = 0
ATOM = 0
CONTENT = 1
LINE = 2
tokens = []
def consume(atom):
    if(tokens[count][ATOM] == atom):
        count += 1
        return True
    return False

# unit: ( declStruct | declFunc | declVar )* END ;
def unit():

    while(True):
        if(declStruct()):
	    else if(declFunc()):
                else if(declVar()):
            else break
        if(consume(END)):
		return True
        else:
		raise Exception("Missing end at unit. line- %s" % tokens[count][LINE])

 	return False

# declStruct: STRUCT ID (LACC declVar* RACC SEMICOLON)? ;
def declStruct():
    init_count = curr_count
    if(consume(STRUCT)):
        if(consume(ID)):
            if(consume(LACC)):
                while(declVar()):
                    if(consume(RACC)):
                        if(consume(SEMICOLON)):
			    return True
			else:
			    raise Exception("Lipseste ';' dupa '}' in declStruct. line - %s" % tokens[count][LINE])
                    else:
		        raise Exception("Lipseste '}' dupa 'declVar' | '{' in declStruct. line - %s" % tokens[count][LINE])
	curr_count = init_count
	return False
# declVar:  typeBase ID arrayDecl? ( COMMA ID arrayDecl? )* SEMICOLON ;
def declVar():
    init_count= count
    if(typeBase()):
        if(consume(ID)):
            arrayDecl();
            while(True):
                if(consume(COMMA)):
                    if(consume(ID)):
                        arrayDecl()
                    else:
                        raise Exception("Lipseste ID-ul dupa ',' in declVar. - line - %s" % tokens[count][LINE])
                else:
                    break
                if(consume(SEMICOLON)):
                    return True
                else:
                    raise Exception("Lipseste ID' dupa 'typeBase' in declVar. line - %s" % tokens[count][LINE]);
    count = init_count;
    return False

# typeBase: INT | DOUBLE | CHAR | STRUCT ID ;
def typeBase():
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
            raise Exception("Lipseste 'ID' dupa 'STRUCT' in typeBase.")
    count = init_count
    return True
}

# arrayDecl: LBRACKET expr? RBRACKET ;
def arrayDecl():
	init_count = count
        if(consume(LBRACKET)):
	    expr()
            if(consume(RBRACKET)):
	        return True
            else:
		raise Exception("Lipseste ')' dupa '(' sau expr in arrayDecl.")
	count = init_count
	return False
# typeName: typeBase arrayDecl? ;
def typeName():
	init_count = count
        if(typeBase()):
	    arrayDecl()
	    return True
	count = init_count 
	return False

/*
declFunc: ( typeBase MUL? | VOID ) ID
                        LPAR ( funcArg ( COMMA funcArg )* )? RPAR
                        stmCompound ;
*/
int declFunc(){
	Token *initTk = currToken;

	if(typeBase()){
		consume(MUL);
	} else{
		if(consume(VOID)){
		} else{
			return 0;
		}
	}

	if(consume(ID)){
		if(consume(LPAR)){
			if(funcArg()){
				while(1){
					if(consume(COMMA)){
						if(funcArg()){

						} else {
							tokenError(currToken, "Lipseste funcArg dupa ',' in declFunc.");
						}
					} else{
						break;
					}
				}
			}
			if(consume(RPAR)){
				if(stmCompound()){
					return 1;
				} else{
					tokenError(currToken, "Lipseste stmCompound in declFunc.");
				}
			} else{
				tokenError(currToken, "Lipseste ')' dupa funcArg in declFunc.");
			}
		}
	} else{
		tokenError(currToken, "Lipseste ID in declFunc.");
	}

	currToken = initTk;
	return 0;
}
// funcArg: typeBase ID arrayDecl? ;
int funcArg(){
	Token *initTk = currToken;

	if(typeBase()){
		if(consume(ID)){
			arrayDecl();
			return 1;
		} else{
			tokenError(currToken, "Lipseste ID in funcArg.");
		}
	}
	currToken = initTk;
	return 0;
}

/*stm: stmCompound
           | IF LPAR expr RPAR stm ( ELSE stm )?
           | WHILE LPAR expr RPAR stm
           | FOR LPAR expr? SEMICOLON expr? SEMICOLON expr? RPAR stm
           | BREAK SEMICOLON
           | RETURN expr? SEMICOLON
           | expr? SEMICOLON ;*/
int stm(){
	Token *initTk = currToken;
	if(stmCompound()){
		return 1;
	}
	if(consume(IF)){
		if(consume(LPAR)){
			if(expr()){
				if(consume(RPAR)){
					if(stm()){
						if(consume(ELSE)){
							if(stm()){
								return 1;
							} else {
								tokenError(currToken, "Lipseste instructiunea dupa else in stm");
							}
						}
						return 1;
					} else{
						tokenError(currToken, "Lipseste instructiunea dupa if in stm");
					}
				} else {
					tokenError(currToken, "Lipseste ')' de la conditia if-ului in stm");
				}
			} else{
				tokenError(currToken, "Lipseste conditia if-ului sau conditia if-ului contine o eroare in stm");
			}
		} else{
			tokenError(currToken, "Lipseste '(' de la conditia if-ului in stm");
		}
	}
	if(consume(WHILE)){
		if(consume(LPAR)){
			if(expr()){
				if(consume(RPAR)){
					if(stm()){
						return 1;
					}else{
						tokenError(currToken, "Lipseste instructiunea dupa while in stm");
					}
				}else{
					tokenError(currToken, "Lipseste ')' de la conditia while-ului in stm");
				}
			}else{
				tokenError(currToken, "Lipseste conditia while-ului in stm");
			}
		}else{
			tokenError(currToken, "Lipseste '(' de la conditia while-ului in stm");
		}
	}
	if(consume(FOR)){
		if(consume(LPAR)){
			expr();

			if(consume(SEMICOLON)){
				expr();

				if(consume(SEMICOLON)){
					expr();
					if(consume(RPAR)){
						if(stm()){
							return 1;
						}else{
							tokenError(currToken, "Lipseste instructiunea dupa for in stm");
						}
					}else{
						tokenError(currToken, "Lipseste ')' de la conditia for-ului in stm");
					}
				}else{
					tokenError(currToken, "Lipseste al 2-lea caracter ';' al for-ului in stm");
				}
			}else{
				tokenError(currToken, "Lipseste primul caracter ';' al for-ului in stm");
			}
		}else{
			tokenError(currToken, "Lipseste '(' de la conditia for-ului in stm");
		}
	}
	if(consume(BREAK)){

		if(consume(SEMICOLON)){
			return 1;
		} else{
			tokenError(currToken, "Lipseste ';' de dupa instructiunea 'break' in stm");
		}
	}
	if(consume(RETURN)){
		expr();

		if(consume(SEMICOLON)){
			return 1;
		} else{
			tokenError(currToken, "Lipseste ';' de dupa instructiunea 'return' in stm");
		}
	}
	if(expr()){
		if(consume(SEMICOLON)){
			return 1;
		} else{
			tokenError(currToken, "Lipseste ';' in stm");
		}
	} else{
		if(consume(SEMICOLON)){
			return 1;
		}
	}
	currToken = initTk;
	return 0;
}

//stmCompound: LACC ( declVar | stm )* RACC ;
int stmCompound(){
	Token *initTk = currToken;
	if(consume(LACC)){
		while(1){
			if(declVar()){

			} else if(stm()){

			} else {
				break;
			}
		}
		if(consume(RACC)){
			return 1;

		} else{
			tokenError(currToken, "Lipseste ')' de dupa '(' din stmCompound");
		}
	}
	currToken = initTk;
	return 0;
}

//expr: exprAssign ;
int expr(){
	Token *initTk = currToken;

	if(exprAssign()){
		return 1;
	}

	currToken = initTk;
	return 0;
}
//exprAssign: exprUnary ASSIGN exprAssign | exprOr ;
int exprAssign(){
  Token *initTk = currToken;

  if(exprUnary()){
    if(consume(ASSIGN)){
      if(exprAssign()){
	return 1;
      }else tokenError(currToken, "Lipseste exprAssign dupa = in exprAssign.");
    }
  }

  currToken = initTk;

  if(exprOr()){
    return 1;
  }

  currToken = initTk;
  return 0;
}

//exprOr: exprOr OR exprAnd | exprAnd ;
int exprOrPrim(){

	if(consume(OR)){
		if(exprAnd()){
	 		if(exprOrPrim()){
				return 1;
	  		}
		}else {
			tokenError(currToken, "Lipseste exprAnd dupa OR.");
		}
	}

    return 1;
}
//exprOr: exprOr OR exprAnd | exprAnd ;
int exprOr(){
  Token *initTk = currToken;

  if(exprAnd()){
    if(exprOrPrim()){
      return 1;
    }
  }

  currToken = initTk;
  return 0;
}

//exprAnd: exprAnd AND exprEq | exprEq ;
int exprAndPrim(){

	if(consume(AND)){
		if(exprEq()){
	  		if(exprAndPrim()){
				return 1;
		  	}
		}else{
			tokenError(currToken, "Lipseste exprEq dupa AND.");
		}
	}

	return 1;
}
//exprAnd: exprAnd AND exprEq | exprEq ;
int exprAnd(){
	Token *initTk = currToken;

	if(exprEq()){
		if(exprAndPrim())
		  return 1;
	}

	currToken = initTk;
	return 0;
}

//exprEq: exprEq ( EQUAL | NOTEQ ) exprRel | exprRel ;
int exprEqPrim(){

	if(consume(EQUAL) | consume(NOTEQ)){
		if(exprRel()){
	  		if(exprEqPrim()){
				return 1;
		  	}
		}else {
			tokenError(currToken, "Lipseste exprRel dupa = | !\\.");
		}
	}

	return 1;
}
//exprEq: exprEq ( EQUAL | NOTEQ ) exprRel | exprRel ;
int exprEq(){
	Token *initTk = currToken;

	if(exprRel()){
		if(exprEqPrim()){
		  return 1;
		}
	}

	currToken = initTk;
	return 0;
}

//exprRel: exprRel ( LESS | LESSEQ | GREATER | GREATEREQ ) exprAdd | exprAdd ;
int exprRelPrim(){

	if(consume(LESS) | consume(LESSEQ) | consume(GREATER) | consume(GREATEREQ)){
		if(exprAdd()){
	  		if(exprRelPrim()){
				return 1;
		  	}
		}else {
			tokenError(currToken, "Lipseste exprAdd in exprRelPrim.");
		}
	}

	return 1;
}
//exprRel: exprRel ( LESS | LESSEQ | GREATER | GREATEREQ ) exprAdd | exprAdd ;
int exprRel(){
	Token *initTk = currToken;

	if(exprAdd()){
		if(exprRelPrim()){
		  return 1;
		}
	}

	currToken = initTk;
	return 0;
}

//exprAdd: exprAdd ( ADD | SUB ) exprMul | exprMul ;
int exprAddPrim(){

	if(consume(ADD) | consume(SUB)){
		if(exprMul()){
	  		if(exprAddPrim()){
				return 1;
			}
		}else {
			tokenError(currToken, "Lipseste exprMul dupa +|-.");
		}
	}

	return 1;
}
//exprAdd: exprAdd ( ADD | SUB ) exprMul | exprMul ;
int exprAdd(){
	Token *initTk = currToken;

	if(exprMul()){
		if(exprAddPrim()){
		  return 1;
		}else{
			tokenError(currToken, "Lipseste elementul dupa exprMul in exprAdd");
		}
	}

	currToken = initTk;
	return 0;
}

//exprMul: exprMul ( MUL | DIV ) exprCast | exprCast ;
int exprMulPrim(){

	if(consume(MUL) || consume(DIV)){
		if(exprCast()){
	  		if(exprMulPrim()){
				return 1;
			}else {
				tokenError(currToken, "Lipseste exprCast dupa *|\\.");
			}
		} else{
			tokenError(currToken, "Lipseste elementul dupa MUL/DIV in exprMulPrim");
		}
	}

	return 1;
}
//exprMul: exprMul ( MUL | DIV ) exprCast | exprCast ;
int exprMul(){
	Token *initTk = currToken;

	if(exprCast()){
		if(exprMulPrim()){
		  return 1;
		}
	}

	currToken = initTk;
	return 0;
}

//exprCast: LPAR typeName RPAR exprCast | exprUnary ;
int exprCast(){
	Token *initTk = currToken;

	if(consume(LPAR)){
		if(typeName()){
			if(consume(RPAR)){
				if(exprCast()){
			  		return 1;
				}else {
					tokenError(currToken, "Lipseste exprCast dupa ')' in exprCast.");
				}
			} else {
				tokenError(currToken, "Lipseste ')' dupa typeName in exprCast.");
			}
		}else {
			tokenError(currToken, "Lipseste typeName dupa '(' in exprCast.");
		}
	} else {
		if(exprUnary()){
			return 1;
		}
	}

	currToken = initTk;
	return 0;
}

//exprUnary: ( SUB | NOT ) exprUnary | exprPostfix ;
int exprUnary(){
	Token *initTk = currToken;

	if(consume(SUB) | consume(NOT)){
		if(exprUnary()){
		  return 1;
		}else {
			tokenError(currToken, "Lipseste exprUnary dupa +|! in exprUnary");
		}
	} else {
		if(exprPostfix()){
			return 1;
		}
	}

	currToken = initTk;
	return 0;
}
/*exprPostfix: exprPostfix LBRACKET expr RBRACKET
           | exprPostfix DOT ID
           | exprPrimary ;*/
int exprPostfixPrim(){

	if(consume(LBRACKET)){
		if(expr()){
  			if(consume(RBRACKET)){
				if(exprPostfixPrim()){
	  				return 1;
				}
	  		}else {
	  			tokenError(currToken, "Lipseste ] dupa expr in exprPostfixPrim.");
	  		}
		}else{
			tokenError(currToken, "Lipseste expr dupa [ in exprPostfixPrim.");
		}
    }

	if(consume(DOT)){
		if(consume(ID)){
	  		if(exprPostfixPrim()){
				return 1;
	  		}
		}else {
			tokenError(currToken, "Lipseste id dupa . in exprPostfixPrim.");
		}
	}

	return 1;
}

/*exprPostfix: exprPostfix LBRACKET expr RBRACKET
           | exprPostfix DOT ID
           | exprPrimary ;*/
int exprPostfix(){
	Token *initTk = currToken;

	if(exprPrimary()){
		if(exprPostfixPrim()){
		  return 1;
		}
	}

	currToken = initTk;
	return 0;
}

/*exprPrimary: ID ( LPAR ( expr ( COMMA expr )* )? RPAR )?
           | CT_INT
           | CT_REAL
           | CT_CHAR
           | CT_STRING
           | LPAR epxr RPAR ;*/

int exprPrimary(){
  Token *initTk = currToken;

	if(consume(ID)){
		if(consume(LPAR)){
			if(expr()){
				while(1){
	  				if(consume(COMMA)){
	    				if(expr()){

	    				} else{
	    					tokenError(currToken, "Lipseste expr dupa , in exprPrimary.");
	    				}
	  				}else break;
				}
	 		}
	  		if(consume(RPAR)){
				return 1;
	  		}else {
                tokenError(currToken, "Lipseste ) dupa ( in exprPrimary.");
            }
		}
		return 1;
	}

	if(consume(CT_INT)){
		return 1;
	}

	if(consume(CT_REAL)){
		return 1;
	}

	if(consume(CT_CHAR)){
		return 1;
	}

	if(consume(CT_STRING)){
		return 1;
	}

	if(consume(LPAR)){
		if(expr()){
			if(consume(RPAR)){
				return 1;
		  	}else tokenError(currToken, "Lipseste ')' dupa expr in exprPrimary.");
		}else tokenError(currToken, "Lipseste expr dupa '(' in exprPrimary.");
	}

	currToken = initTk;
	return 0;
}

int main(int argc, char**argv) {

	if(argc != 2){
		err("Please enter one argument");
	}
    readFromFile(argv[1]);
    tokens =(Token*)malloc(sizeof(Token));
    currToken = tokens;

    while(getNextToken() != END) {

    }
    Token *aux = tokens;
    tokens = tokens->next;
    aux->next = NULL;
    free(aux);
    printAtoms();

    currToken = tokens;
    unit();
    return 0;
}
