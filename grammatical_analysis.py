import lexical_analysis
import global_classes

# 错误列表
ERROR = []

# 语法树
SYNTAX_TREE = None  # 根节点
TREE_POINT = None

# toke序列
TOKEN = []
TOKEN_POINT = 0


def grammatical_analysis_run(filename):
    global ERROR, TOKEN
    global SYNTAX_TREE, TREE_POINT
    SYNTAX_TREE = global_classes.Node(token=global_classes.Token('TreeRoot', -1, -1, -1), father=None)
    TREE_POINT = SYNTAX_TREE
    lexical_analysis.lexical_analysis_run(filename=filename)
    print('Lexical Analysis over!')
    print('grammatical analysis start...')
    ERROR = lexical_analysis.get_ERROR()
    if ERROR:
        print('please check the lexical error!')
        print('grammatical analysis over')
        return None
    TOKEN = lexical_analysis.get_TOKEN()

    Program()

    file_tree = open(file='tree.txt', mode='w')
    strin = write_tree(node=SYNTAX_TREE, depth=0)
    file_tree.write(strin)
    file_tree.close()

    file_tree_total = open('tree_total.txt', 'w')
    strin = write_tree_total(node=SYNTAX_TREE, depth=0)
    file_tree_total.write(strin)
    file_tree_total.close()
    print('grammatical analysis over')
    return SYNTAX_TREE


def write_tree(node, depth):
    """
    将树写入文件中
    :return: string
    """
    strin = ''
    if not (node.get_sons()) and (node.get_token() is None):
        return ''
    for i in range(0, depth):
        strin += '    |'
    strin += '----'
    if not (node.get_token()):
        strin += node.get_name() + '\n'
    else:
        strin += node.get_token().get_type() + '\n'
    if node.get_sons():
        for son in node.get_sons():
            strin += write_tree(son, depth + 1)
    return strin


def write_tree_total(node, depth):
    """
    :param depth:
    :return:
    """
    strin = ''
    for i in range(0, depth):
        strin += '\t'
    if not (node.get_token()):
        strin += node.get_name() + '\n'
    else:
        strin += node.get_token().get_type() + '\n'
    if node.get_sons():
        for son in node.get_sons():
            strin += write_tree_total(son, depth + 1)
    return strin


def show(node, depth):
    print('------SYNTAX TREE------')
    show_tree(node, depth)


def show_tree(node, depth):
    for i in range(0, depth):
        print('\t|', end='')
    print('----', end='')
    if node.get_token() is None:
        print(node.get_name())
    else:
        print(node.get_token().get_type())
    for son in node.get_sons():
        show_tree(son, depth + 1)


def add_tree_node(strin):
    """
    添加节点名称
    :param strin:
    :return:
    """
    global TREE_POINT
    TREE_POINT.add_son(strin=strin, father=TREE_POINT)
    TREE_POINT = TREE_POINT.get_son(strin=strin)


def add_token():
    global TOKEN, TOKEN_POINT
    global TREE_POINT
    TREE_POINT.add_token_son(token=TOKEN[TOKEN_POINT], father=TREE_POINT)
    TOKEN_POINT += 1


def back():
    global TREE_POINT
    TREE_POINT = TREE_POINT.get_father()


def match(strin):
    global TOKEN, TOKEN_POINT
    return strin == TOKEN[TOKEN_POINT].get_type()


def error(message):
    global ERROR
    global TOKEN, TOKEN_POINT
    ERROR.append(global_classes.Error(rows=TOKEN[TOKEN_POINT].get_rows(), columns=TOKEN[TOKEN_POINT].get_columns(),
                                      message=message))


def Program():
    """
    Program::=ProgramHead  DeclarePart  ProgramBody
    :return:
    """
    add_tree_node(strin='Program')
    if match(strin='program'):
        ProgramHead()
        DeclarePart()
        ProgramBody()
    else:
        error(message='program error')
        return None
    back()


def ProgramHead():
    """
    ProgramHead::=	PROGRAM	ProgramName
    :return:
    """
    add_tree_node(strin='ProgramHead')
    if match(strin='program'):
        add_token()
        ProgramName()
    else:
        error(message='Program Head matching error')
        return None
    back()


def ProgramName():
    """
    ProgramName::= ID
    :return:
    """
    add_tree_node(strin='ProgramName')
    if match(strin='ID'):
        add_token()
    else:
        error(message='Program Name error')
        return None
    back()


def DeclarePart():
    """
    DeclarePart	::=	TypeDecpart  VarDecpart  ProcDecpart
    :return:
    """
    add_tree_node(strin='DeclarePart')
    if match(strin='type') or match(strin='var') or match(strin='procedure') or match(strin='begin'):
        TypeDecpart()
        VarDecpart()
        ProcDecpart()
    else:
        error(message='Declare Part error')
        return None
    back()


def TypeDecpart():
    """
    TypeDec ::= null | TypeDec
    :return:
    """
    add_tree_node(strin='TypeDecpart')
    if match(strin='var') or match(strin='procedure') or match(strin='begin'):
        pass
    elif match(strin='type'):
        TypeDec()
    else:
        error(message='Type Dec part error')
        return None
    back()


def TypeDec():
    """
    TypeDeclaration::= 	TYPE	TypeDecList
    :return:
    """
    add_tree_node(strin='TypeDec')
    if match(strin='type'):
        add_token()
        TypeDecList()
    else:
        error(message='Type Dec error')
        return
    back()


def TypeDecList():
    """
    TypeDecList::= TypeId = TypeDef ; TypeDecMore
    :return:
    """
    add_tree_node(strin='TypeDecList')
    if match(strin='ID'):
        TypeId()
        add_token()
        TypeDef()
        add_token()
        TypeDecMore()
    else:
        error(message='Type Dec List error')
        return None
    back()


def TypeDecMore():
    """
    TypeDecMore	::=  null | TypeDecList
    :return:
    """
    add_tree_node(strin='TypeDecMore')
    if match(strin='var') or match(strin='procedure') or match(strin='begin'):
        pass
    elif match(strin='type'):
        add_token()
        TypeDecList()
    else:
        error(message='Type Definition error')
    back()


def TypeId():
    """
    TypeId::= ID
    :return:
    """
    add_tree_node('TypeId')
    if match('ID'):
        add_token()
    else:
        error('Type Id error')
        return None
    back()


def TypeDef():
    """
    TypeDef::= BaseType| StructureType | ID
    :return:
    """
    add_tree_node('TypeDef')
    if match('integer') or match('char'):
        BaseType()
    elif match('array') or match('record'):
        StructureType()
    elif match('ID'):
        add_token()
    else:
        error('Type error')
    back()


def BaseType():
    """
    BaseType::=	INTEGER | CHAR
    :return:
    """
    add_tree_node('BaseType')
    if match('integer'):
        add_token()
    elif match('char'):
        add_token()
    else:
        error('Base Type error')
    back()


def StructureType():
    """
    StructureType::= ArrayType | RecType
    :return:
    """
    add_tree_node('StructureType')
    if match('array'):
        ArrayType()
    elif match('record'):
        RecType()
    else:
        error('Structure Type error')
    back()


def ArrayType():
    """
    ArrayType::=ARRAY [low..top ] OF BaseType
    :return:
    """
    add_tree_node('ArrayType')
    if match('array'):
        add_token()
        add_token()
        Low()
        add_token()
        Top()
        add_token()
        add_token()
        BaseType()
    else:
        error('Array Type error')
    back()


def Low():
    """
    Low ::=  INTC
    :return:
    """
    add_tree_node('Low')
    if match('INIC'):
        add_token()
    else:
        error('Array Low Type error')
    back()


def Top():
    """
    Top ::=	INTC
    :return:
    """
    add_tree_node('Top')
    if match('INIC'):
        add_token()
    else:
        error('Array Top Type error')
    back()


def RecType():
    """
    RecType	::=	RECORD  FieldDecList    END
    :return:
    """
    add_tree_node('RecType')
    if match('record'):
        add_token()
        FieldDecList()
        add_token()
    else:
        error('Record type error')
    back()


def FieldDecList():
    """
    FieldDecList::=	BaseType  IdList ; FieldDecMore	| ArrayType IdList ; FieldDecMore
    :return:
    """
    add_tree_node('FieldDecList')
    if match('integer') or match('char'):
        BaseType()
        IdList()
        add_token()
        FieldDecMore()
    elif match('array'):
        ArrayType()
        IdList()
        add_token()
        FieldDecMore()
    else:
        error("Field Dec List error")
    back()


def IdList():
    """
    IdList	::= ID  IdMore
    :return:
    """
    add_tree_node('IdList')
    if match('ID'):
        add_token()
        IdMore()
    else:
        error('Id List error')
    back()


def IdMore():
    """
    IdMore	::=	 null | , IdList
    :return:
    """
    add_tree_node('IdMore')
    if match(';'):
        pass
    elif match(','):
        add_token()
        IdList()
    else:
        error('Id More error')
    back()


def FieldDecMore():
    """
    FieldDecMore	::=	null | FieldDecList
    :return:
    """
    add_tree_node('FieldDecMore')
    if match('end'):
        pass
    elif match('integer') or match('char') or match('array'):
        FieldDecList()
    else:
        error('Field Dec More error')
    back()


def VarDecpart():
    """
    VarDecpart	::=	null | VarDec
    :return:
    """
    add_tree_node('VarDecpart')
    if match('procedure') or match('begin'):
        pass
    elif match('var'):
        VarDec()
    else:
        error('Var Dec Part error')
    back()


def VarDec():
    """
    VarDec	::=	VAR  VarDecList
    :return:
    """
    add_tree_node('VarDeclaration')
    if match('var'):
        add_token()
        VarDecList()
    else:
        error('Var Dec error')
    back()


def VarDecList():
    """
    VarDecList ::= TypeDef	VarIdList ;  VarDecMore
    :return:
    """
    add_tree_node('VarDecList')
    if match('integer') or match('char') or match('array') or match('record') or match('ID'):
        TypeDef()
        VarIdList()
        add_token()
        VarDecMore()
    else:
        error('Var Dec List error')
    back()


def VarIdList():
    """
    VarIdList::=id  VarIdMore
    :return:
    """
    add_tree_node('VarIdList')
    if match('ID'):
        add_token()
        VarIdMore()
    else:
        error('Var Id List error')
    back()


def VarIdMore():
    """
    VarIdMore	::=	null| , VarIdList
    :return:
    """
    add_tree_node('VarIdMore')
    if match(';'):
        pass
    elif match(','):
        add_token()
        VarIdList()
    else:
        error('Var Id More error')
    back()


def VarDecMore():
    """
    VarDecMore	::= null |VarDecList
    :return:
    """
    add_tree_node('VarDecMore')
    if match('procedure') or match('begin'):
        pass
    elif match('integer') or match('char') or match('array') or match('record') or match('ID'):
        VarDecList()
    else:
        error('Var Dec More error')
    back()


def ProcDecpart():
    """
    ProcDecpart	::=	 null 	 | ProcDec
    :return:
    """
    add_tree_node('ProDecpart')
    if match('begin'):
        pass
    elif match('procedure'):
        ProcDec()
    else:
        error('Proc Dec error')
    back()


def ProcDec():
    """
    ProcDec::=PROCEDURE ProcName(ParamList);ProcDecPart ProcBody ProcDecMore
    :return:
    """
    add_tree_node('ProcDec')
    if match('procedure'):
        add_token()
        ProcName()
        add_token()
        ParamList()
        add_token()
        add_token()
        ProcDecPart()
        ProcBody()
        ProcDecMore()
    else:
        error('Proc Declaration error')
    back()


def ProcDecPart():
    """
    ProcDecPart	::=	DeclarePart
    :return:
    """
    add_tree_node('ProcDecPart')
    if match('type') or match('var') or match('Procedure') or match('begin'):
        DeclarePart()
    else:
        error('Proc Dec Part error')
    back()


def ProcBody():
    """
    ProcBody		::=	ProgramBody
    :return:
    """
    add_tree_node('ProBody')
    if match('begin'):
        ProgramBody()
    else:
        error('Proc Body error')
    back()


def ProcDecMore():
    """
    ProcDecMore::= null | ProcDec
    :return:
    """
    add_tree_node('ProcDecMore')
    if match('procedure'):
        ProcDec()
    elif match('begin'):
        pass
    else:
        error('Proc Dec More error')
    back()


def ParamList():
    """
    ParamList	::=	 null	| ParamDecList
    :return:
    """
    add_tree_node('ParamList')
    if match(')'):
        pass
    elif match('integer') or match('char') or match('array') or match('record') or match('ID'):
        ParamDecList()
    else:
        error('Param List error')
    back()


def ParamDecList():
    """
    ParamDecList::=	 Param  ParamMore
    :return:
    """
    add_tree_node('ParamDecList')
    if match('integer') or match('char') or match('array') or match('record') or match('ID'):
        Param()
        ParamMore()
    else:
        error('Param Dec List error')
    back()


def Param():
    """
    Param ::= TypeDef FormList | VAR TypeDef FormList
    :return:
    """
    add_tree_node('Param')
    if match('integer') or match('char') or match('array') or match('record') or match('ID'):
        TypeDef()
        FormList()
    elif match('var'):
        add_token()
        TypeDef()
        FormList()
    else:
        error('Param error')
    back()


def FormList():
    """
    FormList::= ID  FidMore
    :return:
    """
    add_tree_node('FormList')
    if match('ID'):
        add_token()
        FidMore()
    else:
        error('Form List error')
    back()


def FidMore():
    """
    FidMore	::=	 null | , FormList
    :return:
    """
    add_tree_node('FidMore')
    if match(')') or match(';'):
        pass
    elif match(','):
        add_token()
        FormList()
    else:
        error('Fid More error')
    back()


def ParamMore():
    """
    ParamMore	::=	null | ; ParamDecList
    :return:
    """
    add_tree_node('ParamMore')
    if match(')'):
        pass
    elif match(';'):
        add_token()
        ParamDecList()
    else:
        error('Param More error')
    back()


def ProcName():
    """
    ProcName::=	ID
    :return:
    """
    add_tree_node('ProcName')
    if match('ID'):
        add_token()
    else:
        error('Proc Name error')
    back()


def ProgramBody():
    """
    ProgramBody	::=	BEGIN  StmList END
    :return:
    """
    add_tree_node('ProgramBody')
    if match('begin'):
        add_token()
        StmList()
        add_token()
    else:
        error('Program Body error')
    back()


def StmList():
    """
    StmList	::=	Stm	StmMore
    :return:
    """
    add_tree_node('StmList')
    if match('if') or match('while') or match('read') or match('write') or match(
            'ID') or match('do'):
        Stm()
        StmMore()
    elif match('end') or match('endwh'):
        pass
    else:
        error('Stm List error')
    back()


def StmMore():
    """
    StmMore	::=	null| ;  StmList
    :return:
    """
    add_tree_node('StmMore')
    if match('end') or match('else') or match('fi') or match('endwh'):
        pass
    elif match(';'):
        add_token()
        StmList()
    else:
        error('Stm More error')
    back()


def Stm():
    """
    Stm		::=	ConditionalStm| LoopStm| InputStm|OutputStm| ReturnStm| ID AssCall
    :return:
    """
    add_tree_node('Stm')
    if match('if'):
        ConditionalStm()
    elif match('while'):
        LoopStm()
    elif match('read'):
        InputStm()
    elif match('write'):
        OutputStm()
    elif match('return'):
        ReturnStm()
    elif match('ID'):
        add_token()
        AssCall()
    else:
        error('Stm error')
    back()


def ConditionalStm():
    """
    ConditionalStm ::= IF RelExp THEN StmList ELSE StmList FI
    :return:
    """
    add_tree_node('ConditionalStm')
    if match('if'):
        add_token()
        RelExp()
        add_token()
        StmList()
        add_token()
        StmList()
        add_token()
    else:
        error('Conditional Stm error')
    back()


def RelExp():
    """
    RelExp	::=  Exp  OtherRelE
    :return:
    """
    add_tree_node('RelExp')
    if match('(') or match('ID') or match('INIC'):
        Exp()
        OtherRelE()
    else:
        error('Rel Exp error')
    back()


def Exp():
    """
    Exp	::=  Term   OtherTerm
    :return:
    """
    add_tree_node('Exp')
    if match('(') or match('ID') or match('INIC'):
        Term()
        OtherTerm()
    else:
        error('Exp error')
    back()


def Term():
    """
    Term::=  Factor  OtherFactor
    :return:
    """
    add_tree_node('Term')
    if match('(') or match('INIC') or match('ID'):
        Factor()
        OtherFactor()
    else:
        error('Term error')
    back()


def OtherFactor():
    """
    OtherFactor ::= null | MultOp Term
    :return:
    """
    add_tree_node('OtherFactor')
    if match('+') or match('-') or match(')') or match(']') or match('do') or match('then') \
            or match('<') or match('=') or match('>') or match(',') or match(';') or match('end') \
            or match('else') or match('fi') or match('endwh'):
        pass
    elif match('*') or match('/'):
        MultOp()
        Term()
    else:
        error('Other Factor error')
    back()


def MultOp():
    """
    MultOp	::=  	* 	|  /
    :return:
    """
    add_tree_node('MulOp')
    if match('*') or match('/'):
        add_token()
    else:
        error('MultOp error')
    back()


def Factor():
    """
    Factor::= (Exp) | INTC | Variable
    :return:
    """
    add_tree_node('Factor')
    if match('('):
        add_token()
        Exp()
        add_token()
    elif match('INIC'):
        add_token()
    elif match('ID'):
        Variable()
    else:
        error('Factor error')
    back()


def Variable():
    """
    Variable::=   ID   VariMore
    :return:
    """
    add_tree_node('Variable')
    if match('ID'):
        add_token()
        VariMore()
    else:
        error('Variable error')
    back()


def VariMore():
    """
    VariMore::= null |[Exp]|.FieldVar
    :return:
    """
    add_tree_node('VariMore')
    if match('+') or match('-') or match('*') or match('/') or match(')') or match(']') \
            or match('do') or match('then') or match('<') or match('=') or match('>') \
            or match(',') or match(';') or match('end') or match('else') or match('fi') \
            or match('endwh') or match(':='):
        pass
    elif match('['):
        add_token()
        Exp()
        add_token()
    elif match('.'):
        add_token()
        FieldVar()
    else:
        error('Vari More error')
    back()


def FieldVar():
    """
    FieldVar::=  ID   FieldVarMore
    :return:
    """
    add_tree_node('FieldVar')
    if match('ID'):
        add_token()
        FieldVarMore()
    else:
        error('Field Var error')
    back()


def FieldVarMore():
    """
    FieldVarMore::= null 	| [ Exp  ]
    :return:
    """
    add_tree_node('FieldVarMore')
    if match('+') or match('-') or match('*') or match('/') or match(')') or match(']') \
            or match('do') or match('then') or match('<') or match('=') or match('>') \
            or match(',') or match(';') or match('end') or match('else') or match('fi') \
            or match('endwh') or match(':='):
        pass
    elif match('['):
        add_token()
        Exp()
        add_token()
    else:
        error('Field Var More error')
    back()


def OtherTerm():
    """
    OtherTerm::= null | AddOp   Exp
    :return:
    """
    add_tree_node('OtherTerm')
    if match(')') or match(']') or match('do') or match('then') or match('<') or match('=') or match('>') \
            or match(',') or match(';') or match('end') or match('else') or match('fi') or match('endwh'):
        pass
    elif match('+') or match('-'):
        AddOp()
        Exp()
    else:
        error('Other Term error')
    back()


def AddOp():
    """
    AddOp	::=   + | -
    :return:
    """
    add_tree_node('AddOp')
    if match('+') or match('-'):
        add_token()
    else:
        error('Add Op error')
    back()


def OtherRelE():
    """
    OtherRelE	::=  CmpOp   Exp
    :return:
    """
    add_tree_node('OtherRelE')
    if match('<') or match('>') or match('='):
        CmpOp()
        Exp()
    else:
        error('Other Rel E error')
    back()


def CmpOp():
    """
    CmpOp::=   <  |  =  |  >
    :return:
    """
    add_tree_node('CmpOp')
    if match('<') or match('>') or match('='):
        add_token()
    else:
        error('Cmp Op error')
    back()


def LoopStm():
    """
    LoopStm::= WHILE RelExp DO StmList ENDWH
    :return:
    """
    add_tree_node('LoopStm')
    if match('while'):
        add_token()
        RelExp()
        add_token()
        StmList()
        add_token()
    else:
        error('Loop Stm error')
    back()


def InputStm():
    """
    InputStm::=	READ ( Invar)
    :return:
    """
    add_tree_node('InputStm')
    if match('read'):
        add_token()
        add_token()
        Invar()
        add_token()
    else:
        error('Input Stm error')
    back()


def Invar():
    """
    Invar 		::=   ID
    :return:
    """
    add_tree_node('Invar')
    if match('ID'):
        add_token()
    else:
        error('Invar error')
    back()


def OutputStm():
    """
    OutputStm::=	WRITE( Exp )
    :return:
    """
    add_tree_node('OutputStm')
    if match('write'):
        add_token()
        add_token()
        Exp()
        add_token()
    else:
        error('Output Stm error')
    back()


def ReturnStm():
    """
    ReturnStm::=	RETURN ( Exp )
    :return:
    """
    add_tree_node('ReturnStm')
    if match('return'):
        add_token()
    else:
        error('Return Stm error')
    back()


def AssCall():
    """
    AssCall	::=  AssignmentRest| CallStmRest
    :return:
    """
    add_tree_node('AssCall')
    if match('.') or match('[') or match(':='):
        AssignmentRest()
    elif match('('):
        CallStmRest()
    else:
        error('Ass Call error')
    back()


def CallStmRest():
    """
    CallStmRest	::=	( ActParamList )
    :return:
    """
    add_tree_node('CallStmRest')
    if match('('):
        add_token()
        ActParamList()
        add_token()
    else:
        error('Call Stm Rest error')
    back()


def ActParamList():
    """
    ActParamList::=null | Exp  ActParamMore
    :return:
    """
    add_tree_node('ActParamList')
    if match(')'):
        pass
    elif match('(') or match('INIC') or match('ID'):
        Exp()
        ActParamMore()
    else:
        error('Act Param List error')
    back()


def ActParamMore():
    """
    ActParamMore::=null| ,  ActParamList
    :return:
    """
    add_tree_node('ActParmMore')
    if match(','):
        add_token()
        ActParamList()
    elif match(')'):
        pass
    else:
        error('Act Param More error')
    back()


def AssignmentRest():
    """
    AssignmentRest	::= VariMore	:= Exp
    :return:
    """
    add_tree_node('AssignmentRest')
    if match('.') or match('[') or match(':='):
        VariMore()
        add_token()
        Exp()
    else:
        error('Assignment error')
    back()


def get_ERROR():
    global ERROR
    return ERROR


if __name__ == "__main__":
    grammatical_analysis_run('test/program.txt')
    show(SYNTAX_TREE, 0)
