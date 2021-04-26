from symTable import *
import lexical_analysis
import grammatical_analysis
import global_classes

# initialize global
Off = 0
savedOff = 0
Level = -1
scope = [None] * SCOPESIZE
intPtr = None
charPtr = None
boolPtr = None

# 错误列表
ERROR = []

TOKEN = lexical_analysis.get_TOKEN()
ID_TABLE = lexical_analysis.get_ID_TABLE()
INIC_TABLE = lexical_analysis.get_INIC_TABLE()
KEY_WORDS = lexical_analysis.get_KEY_WORDS()


def error(row=0, column=0, message=''):
    global ERROR
    ERROR.append(global_classes.Error(row, column, message))


def analyse2(begin, end):
    if begin > end:
        error(row=begin, column=0, message='begin is bigger than end')
    start = begin
    stop = end
    while start < len(TOKEN) and TOKEN[start].get_rows() != begin:
        start += 1
    start += 1
    while stop < len(TOKEN) and TOKEN[stop].get_rows() != end:
        stop += 1
    while stop < len(TOKEN) and TOKEN[stop + 1].get_rows() == TOKEN[stop].get_rows():
        stop += 1

    end = stop
    i = start
    while i < len(TOKEN) and TOKEN[i].get_rows() < end and i < end:
        j = i
        kind = ""
        while j < len(TOKEN) and j < end and TOKEN[j].get_rows() < end and TOKEN[j].get_rows() == TOKEN[i].get_rows():
            item = TOKEN[j]
            if item.get_type() in KEY_WORDS:
                if item.get_type() == 'char' or item.get_type() == 'integer':
                    if kind == "":
                        kind = item.get_type()
                    elif kind != item.get_type():
                        error(row=item.get_rows(), column=item.get_columns(), message='The type is not matched!')
                        while j < end and TOKEN[j].get_rows() == TOKEN[i]:
                            j += 1
                        i = j - 1
                        # 跳回上一层循环，处理下一行
                        # break
                elif item.get_type() == 'if' or item.get_type() == 'while':
                    flag = isBool(j, end)
                    if flag is False:
                        error(row=item.get_rows(), column=item.get_columns(), message='The expression is not boolean!')
                    # if or while括号内有问题时不跳过，继续检查，判断是否有类型错误
            elif item.get_type() == 'INIC':
                content = INIC_TABLE[item.get_position()]
                if kind == "":
                    if content.isdigit:
                        kind = "integer"
                    elif content.isalpha:
                        kind = "char"
                constantment(j, end)

            elif item.get_type() == 'ID':
                name = ID_TABLE[item.get_position()]

                result, entry = FindEntry(name, 0)
                if result is False:
                    error(row=item.get_rows(), column=item.get_columns(), message='The identifier is not defined!')
                    while TOKEN[j].get_rows() < end and TOKEN[j].get_rows() == TOKEN[i]:
                        j += 1
                    i = j - 1
                    # 跳回上一层循环，处理下一行
                    # break
                if result and TOKEN[j + 1].get_type() == '(':
                    j = callstatement(j, end)
                    j -= 1
                if result and TOKEN[j + 1].get_type() == '[':
                    j = arraystatement(j)
                elif result and entry.attrIR.kind:
                    if kind == "":
                        kind = entry.attrIR.idtype
                    elif kind != entry.attrIR.idtype:
                        error(row=item.get_rows(), column=item.get_columns(), message='The type is not matched!')

            j += 1
        # 此时token[j]已经不是同一行，i改变，处理下一行
        i = j


def arraystatement(j):
    j += 2
    while j < len(TOKEN) and TOKEN[j].get_type() != ']':
        item = TOKEN[j]
        namej = ID_TABLE[item.get_position()]
        resultj, entryj = FindEntry(namej, 0)
        if item.get_type() == 'ID':
            if resultj is False:
                error(row=item.get_rows(), column=item.get_columns(), message='The identifier is not defined!')
            elif entryj.attrIR.idtype.kind != TypeKind.integer:
                error(row=item.get_rows(), column=item.get_columns(), message='The index is not integer!')
        elif item.get_type() == 'INIC' or item.get_type() in ['+', '-', '*', '/']:
            pass
        else:
            # print("===",item.get_type())
            error(row=item.get_rows(), column=item.get_columns(), message='The index is not integer!')
        j += 1
    return j


def isBool(j, end):
    row = TOKEN[j].get_rows()
    j += 1
    flag = False
    while TOKEN[j].get_rows() == row:
        if TOKEN[j].get_type() == '<' or TOKEN[j].get_type() == '=':
            flag = True
        j += 1

    if flag:
        return True
    return False


def callstatement(j, end):
    item = TOKEN[j]
    name = ID_TABLE[item.get_position()]
    result, entry = FindEntry(name, 0)
    if result is False:
        error(row=item.get_rows(), column=item.get_columns(), message='The function is not declared!')
        i = j
        while TOKEN[j].get_rows() < end and TOKEN[j].get_rows() == TOKEN[i].get_rows():
            j += 1
    else:
        j += 2
        param = entry.attrIR.More['ProcAttr']['param']
        i = 0
        while param is not None and i < len(param) and TOKEN[j].get_type() != ')':
            namej = ID_TABLE[item.get_position()]
            resultj, entryj = FindEntry(namej, 0)
            if resultj is False:
                error(row=item.get_rows(), column=item.get_columns(), message='The identifier is not defined!')
            elif entry.attrIR.idtype != param[i].attrIR.idtype:
                error(row=item.get_rows(), column=item.get_columns(), message='The param type is not matched!')
            i += 1
            j += 1
        if param is not None and i > len(param) and TOKEN[j].get_type() != ')':
            error(row=item.get_rows(), column=item.get_columns(), message='The param num is not matched!')
        if param is not None and i < len(param) and TOKEN[j].get_type() == ')':
            error(row=item.get_rows(), column=item.get_columns(), message='The param num is not matched!')
        while TOKEN[j].get_type() != ')':
            j += 1

        # 返回调用函数的最后一个token
    return j


def constantment(j, end):
    # print("constantment:")
    row = TOKEN[j].get_rows()
    i = j
    while TOKEN[j].get_rows() == row:
        if TOKEN[j].get_type() == ":=":
            error(row=TOKEN[j].get_rows(), column=TOKEN[j].get_columns(),
                  message='The left is not the variable identifier!')
        j += 1


# 初始化基本类型内部表示函数
def initialize():
    global scope, intPtr, charPtr, boolPtr
    intPtr = NewTy(TypeKind.integer)
    charPtr = NewTy(TypeKind.char)
    boolPtr = NewTy(TypeKind.bool)


# 类型分析处理函数
# t--TypeDecList
# deckind--TypeName
# t--FormList
# tt--TypeDef/FieldDecList
# deckind--TypeDef.son[0]--None,BaseType,StructureType
def TypeProcess(t, deckind):
    Ptr = None
    # 类型声明分析使用
    if deckind is None:
        Ptr = nameType(t)
    elif deckind == "StructureType":
        deckind = (((t.get_sons())[0].get_sons())[0].get_sons())[0].get_token().get_type()
        if deckind == "array":
            t = ((t.get_sons())[0].get_sons())[0]
            # t--ArrayType
            Ptr = arrayType(t)
        elif deckind == "record":
            Ptr = recordType(t)
    elif deckind == "BaseType":
        deckind = ((t.get_sons())[0].get_sons())[0].get_token().get_type()
        if deckind == "integer":
            Ptr = intPtr
        elif deckind == "char":
            Ptr = charPtr
    # 数组类型使用
    elif deckind == "integer":
        Ptr = intPtr
    elif deckind == "char":
        Ptr = charPtr
    # 记录类型使用
    elif deckind == "ArrayType":
        t = (t.get_sons())[0]
        # t--ArrayType
        Ptr = arrayType(t)
    return Ptr


# 自定义类型内部结构分析函数
# t--TypeDecList
# tt-TypeDef  type-t1,row
def nameType(t):
    Ptr = None
    entry = None
    type1 = ID_TABLE[(t.get_sons())[0].get_token().get_position()]
    row = (t.get_sons())[0].get_token().get_rows()
    column = (t.get_sons())[0].get_token().get_columns()
    present, entry = FindEntry(type1, entry)

    if present is True:
        if entry.attrIR.kind != IdKind.typeKind:
            error(row=row, column=column, message=type1 + " used before typed!")
        else:
            Ptr = entry.attrIR.idtype

    else:
        error(row=row, column=column, message=type1 + " type name is not declared!")

    return Ptr


# 数组类型内部表示处理函数
# t--TypeDecList
# tt--ArrayType--type,row,low,up,childtype
def arrayType(t):
    ptr0 = None
    ptr1 = None
    ptr = None

    row = (t.get_sons())[0].get_token().get_rows()
    column = (t.get_sons())[0].get_token().get_columns()
    low = INIC_TABLE[((t.get_sons())[2].get_sons())[0].get_token().get_position()]
    up = INIC_TABLE[((t.get_sons())[4].get_sons())[0].get_token().get_position()]
    childtype = ((t.get_sons())[7].get_sons())[0].get_token().get_type()
    if low > up:
        error(row=row, column=column, message=" array subscript error!")
    else:
        ptr0 = TypeProcess(t, DecKind.integer)
        ptr1 = TypeProcess(t, childtype)
        ptr = NewTy(TypeKind.array)
        ptr.size = (int(up) - int(low) + 1) * ptr1.size

        ptr.More['ArrayAttr']['indexTy'] = ptr0
        ptr.More['ArrayAttr']['elemTy'] = ptr1
        ptr.More['ArrayAttr']['low'] = low
        ptr.More['ArrayAttr']['up'] = up

    return ptr


# 处理记录类型的内部表示函数
# t--TypeDecList
# tt-TypeDef
def recordType(t):
    Ptr = NewTy(TypeKind.recordTy)
    t = (((t.get_sons())[0].get_sons())[0].get_sons())[1]
    Ptr2 = None
    Ptr1 = None
    body = None

    while t is not None:
        i = 0
        p = (t.get_sons())[1]
        # p--IdList
        type1 = ((t.get_sons())[0].get_sons())[0].get_token().get_type()
        while p is not None:
            Ptr2 = NewBody()
            if body is None:
                body = Ptr1 = Ptr2
            Ptr2.UnitType = TypeProcess(t, type1)

            Ptr2.Next = None

            if Ptr2 != Ptr1:
                Ptr2.off = Ptr1.off + Ptr1.UnitType.size
                Ptr1.Next = Ptr2
                Ptr1 = Ptr2
            p = ((p.get_sons())[1].get_sons())[1]

        t = ((t.get_sons())[3].get_sons())[0]
    Ptr.size = Ptr2.off + Ptr2.UnitType.size
    Ptr.More['body'] = body
    return Ptr


# 类型声明部分分析处理函数
# t--TypeDecList--name,row,type,TypeDef
def TypeDecPart(t):
    present = False
    entry = None

    attrIr = AttributeIR()
    attrIr.kind = IdKind.typeKind
    # p=((t.get_sons())[0].get_sons())[0];
    while t is not None:
        name1 = ID_TABLE[((t.get_sons())[0].get_sons())[0].get_token().get_position()]
        row = ((t.get_sons())[0].get_sons())[0].get_token().get_rows()
        column = ((t.get_sons())[0].get_sons())[0].get_token().get_columns()
        type1 = ((t.get_sons())[2].get_sons())[0].get_name()
        # type1--None,BaseType,StructureType
        present, attrIr, entry = Enter(name1, attrIr, entry)
        if present is not False:
            error(row=row, column=column, message=name1 + "is repeatedly declared!")
            entry = None
        else:
            entry.attrIR.idtype = TypeProcess((t.get_sons())[2], type1)
        if not ((t.get_sons())[4].get_sons()):
            t = None
        else:
            t = ((t.get_sons())[4].get_sons())[1]


# t--VarDecList
# t--ParamDecList
def varDecPart(t):
    VarDecList(t)


# 变量声明部分分析处理函数
# t--VarDecList
# t--ParamDecList
def VarDecList(t):
    global Off, Level, savedOff
    attrIr = AttributeIR()
    present = False
    entry = None

    while t is not None:
        attrIr.kind = IdKind.varKind
        i = 0
        # 过程声明使用
        if (t.get_sons())[0].get_name() == "Param":
            # 类型
            # t--ParamDecList
            type1 = (((t.get_sons())[0].get_sons())[0].get_sons())[0].get_name()
            p = ((t.get_sons())[0].get_sons())[1]
            while p is not None:
                attrIr.idtype = TypeProcess(((t.get_sons())[0].get_sons())[0], type1)
                attrIr.More['VarAttr']['access'] = AccessKind.indir
                attrIr.More['VarAttr']['level'] = Level
                attrIr.More['VarAttr']['off'] = Off
                row = (p.get_sons())[0].get_token().get_rows()
                column = (p.get_sons())[0].get_token().get_columns()
                name1 = ID_TABLE[(p.get_sons())[0].get_token().get_position()]
                Off += 1
                present, attrIr, entry = Enter(name1, attrIr, entry)
                if present is not False:
                    error(row=row, column=column, message=name1 + " is defined repeatedly!")
                if not ((p.get_sons())[1].get_sons()):
                    p = None
                else:
                    p = ((p.get_sons())[1].get_sons())[1]
            if (t.get_sons())[1].get_sons():
                t = ((t.get_sons())[1].get_sons())[1]
            else:
                t = None
        # 变量声明使用
        else:
            type1 = (((t.get_sons())[0]).get_sons())[0].get_name()
            p = (t.get_sons())[1]
            while p is not None:
                attrIr.idtype = TypeProcess((t.get_sons())[0], type1)
                attrIr.More['VarAttr']['access'] = AccessKind.dir
                attrIr.More['VarAttr']['level'] = Level
                name1 = ID_TABLE[(p.get_sons())[0].get_token().get_position()]
                row = (p.get_sons())[0].get_token().get_rows()
                column = (p.get_sons())[0].get_token().get_columns()
                if attrIr.idtype is not None:
                    attrIr.More['VarAttr']['off'] = Off
                    Off = Off + attrIr.idtype.size
                    present, attrIr, entry = Enter(name1, attrIr, entry)
                if present is not False:
                    error(row=row, column=column, message=name1 + " is defined repeatedly!")
                if not ((p.get_sons())[1].get_sons()):
                    p = None
                else:
                    p = ((p.get_sons())[1].get_sons())[1]
            if not ((t.get_sons())[3].get_sons()):
                t = None
            else:
                t = ((t.get_sons())[3].get_sons())[0]

    if Level == 0:
        pass
    else:
        savedOff = Off


# 过程声明部分分析处理函数
# t--ProcDec
def procDecPart(t):
    global Level
    r = t
    while t is not None:
        entry = HeadProcess(t)
        q = ((t.get_sons())[6].get_sons())[0]
        p = (q.get_sons())[0]
        if p.get_sons():
            TypeDecPart(((p.get_sons())[0].get_sons())[1])
        p = (q.get_sons())[1]
        if p.get_sons():
            varDecPart(((p.get_sons())[0].get_sons())[1])
        p = (q.get_sons())[2]
        if p.get_sons():
            procDecPart((p.get_sons())[0])
        entry.attrIR.More['ProcAttr']['nOff'] = savedOff
        entry.attrIR.More['ProcAttr']['mOff'] = entry.attrIR.More['ProcAttr']['nOff'] + entry.attrIR.More['ProcAttr'][
            'level'] + 1
        row1 = ((((t.get_sons())[7].get_sons())[0].get_sons())[0]).get_token().get_rows()
        row2 = ((((t.get_sons())[7].get_sons())[0].get_sons())[2]).get_token().get_rows()
        analyse2(row1, row2)
        if Level != -1:
            DestroyTable()
        if not ((t.get_sons())[8].get_sons()):
            t = None
        else:
            t = ((t.get_sons())[8].get_sons())[0]


# 过程声明头分析函数
# t--procDec
def HeadProcess(t):
    global Level

    attrIr = AttributeIR()
    present = False
    entry = None

    attrIr.kind = IdKind.procKind
    attrIr.idtype = None
    attrIr.More['ProcAttr']['level'] = Level + 1

    if t is not None:
        name1 = ID_TABLE[((t.get_sons())[1].get_sons())[0].get_token().get_position()]
        present, attrIr, entry = Enter(name1, attrIr, entry)

    entry.attrIR.More['ProcAttr']['param'] = ParaDecList(t)
    return entry


# 形参分析处理函数
# t--procDec
def ParaDecList(t):
    global Level, Off

    p = None
    Ptr1 = None
    head = None
    if t is not None:
        if (t.get_sons())[3].get_sons():
            p = ((t.get_sons())[3].get_sons())[0]
        # p--ParamDecList
        Level, off = CreatTable()

        varDecPart(p)
        Ptr0 = scope[Level]

        while Ptr0 is not None:
            Ptr2 = NewParam()
            if head is not None:
                head = Ptr1 = Ptr2
            Ptr2.entry = Ptr0
            Ptr2.next = None

            if Ptr2 != Ptr1:
                Ptr1.next = Ptr2
                Ptr1 = Ptr2

            Ptr0 = Ptr0.next

    return head


# 执行体部分分析处理函数
# t--StmList
def Body(t):
    # t=(t.get_sons())[0]
    # p = (t.get_sons())[0]
    while t.get_sons():
        statement((t.get_sons())[0])
        # (Stm)
        if not (t.get_sons()[1].get_sons()):
            break
        else:
            t = ((t.get_sons())[1].get_sons())[1]


def statement(t):
    pass


# 语义分析主函数
# t--Program
def semantic_analysis_run(t):
    global Level, Off
    # 创建新一层
    Level, Off = CreatTable()

    initialize()
    q = (t.get_sons())[1]
    p = (q.get_sons())[0]
    if p.get_sons():
        TypeDecPart(((p.get_sons())[0].get_sons())[1])
    p = (q.get_sons())[1]
    if p.get_sons():
        varDecPart(((p.get_sons())[0].get_sons())[1])
    p = (q.get_sons())[2]
    if p.get_sons():
        procDecPart((p.get_sons())[0])
    t = (t.get_sons())[2]
    # t--ProgramBody
    if (t.get_sons())[1].get_name() == "stmList":
        row1 = (t.get_sons())[0].get_token().get_rows()
        row2 = (t.get_sons())[2].get_token().get_rows()
        analyse2(row1, row2)
    if Level != -1:
        DestroyTable()


if __name__ == '__main__':
    root = grammatical_analysis.grammatical_analysis_run('test/program.txt')
    print('Semantic Analysis start... ')
    ERROR = grammatical_analysis.ERROR
    # grammatical_analysis.show_tree(root, 0)
    if ERROR:
        print('please check lexical or grammatical error')
        print('Semantic Analysis over! ')
    else:
        root = (root.get_sons())[0]
        semantic_analysis_run(root)
        PrintSymbTable()
        print('Semantic Analysis over! ')
