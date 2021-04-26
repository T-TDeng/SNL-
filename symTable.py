from Table import *
import semantic_analysis


def printInLine(word):
    print(word, end="")


def printTab(num):
    i = 0
    while i < num:
        printInLine(" ")
        i += 1


def PrintOneLayer(level, file_symbTable):
    t = semantic_analysis.scope[level]
    strin = "\n -------SymbTable in level " + str(level) + " ---------\n"
    file_symbTable.write(strin)
    printInLine(strin)
    while t is not None:
        strin = t.idName + ":  "
        file_symbTable.write(strin)
        printInLine(strin)
        Attrib = t.attrIR
        if Attrib.idtype is not None:
            if Attrib.idtype.kind == TypeKind.integer:
                file_symbTable.write("integer  ")
                printInLine("integer  ")
            elif Attrib.idtype.kind == TypeKind.char:
                file_symbTable.write("char  ")
                printInLine("char  ")
            elif Attrib.idtype.kind == TypeKind.array:
                file_symbTable.write("array  ")
                printInLine("array  ")
            elif Attrib.idtype.kind == TypeKind.record:
                file_symbTable.write("record  ")
                printInLine("record  ")
            else:
                file_symbTable.write("error type!  ")
                printInLine("error type!  ")

        if Attrib.kind == IdKind.typeKind:
            file_symbTable.write("typekind  ")
            printInLine("typekind  ")
        elif Attrib.kind == IdKind.varKind:
            file_symbTable.write("varkind  ")
            printInLine("varkind  ")
            file_symbTable.write("Level = " + str(Attrib.More["VarAttr"]["level"]) + "  ")
            printInLine("Level = " + str(Attrib.More["VarAttr"]["level"]) + "  ")
            file_symbTable.write("Offset = " + str(Attrib.More["VarAttr"]["off"]) + "  ")
            printInLine("Offset = " + str(Attrib.More["VarAttr"]["off"]) + "  ")
            if Attrib.More["VarAttr"]["access"] == AccessKind.dir:
                file_symbTable.write('dir  ')
                printInLine("dir  ")
            elif Attrib.More['VarAttr']['access'] == AccessKind.indir:
                file_symbTable.write('indir  ')
                printInLine("indir  ")
            else:
                file_symbTable.write('errordir  ')
                printInLine("errorkind  ")
        elif Attrib.kind == IdKind.procKind:
            file_symbTable.write('funckind  ')
            printInLine("funckind   ")
            file_symbTable.write("Level = " + str(Attrib.More["ProcAttr"]["level"]) + "  ")
            printInLine("Level = " + str(Attrib.More["ProcAttr"]["level"]) + "  ")
            file_symbTable.write("Noff = " + str(Attrib.More["ProcAttr"]["nOff"]))
            printInLine("Noff = " + str(Attrib.More["ProcAttr"]["nOff"]))
        else:
            file_symbTable.write('error  ')
            printInLine("error  ")
        file_symbTable.write('\n')
        printInLine("\n")
        t = t.next


# 打印符号表
def PrintSymbTable():
    file_symbTable = open('symbol_table.txt', 'w')
    level = 0
    while semantic_analysis.scope[level] is not None:
        PrintOneLayer(level, file_symbTable)
        level += 1


def NewTable():
    table = Symbtable()

    table.next = None

    table.attrIR.kind = IdKind.typeKind
    table.attrIR.idtype = None
    table.next = None
    table.attrIR.More["VarAttr"]["isParam"] = False

    return table


# 创建一个符号表
def CreatTable():
    semantic_analysis.Level += 1
    semantic_analysis.scope[semantic_analysis.Level] = None
    semantic_analysis.Off = INITOFF
    return semantic_analysis.Level, semantic_analysis.Off


# 撤销一个符号表
def DestroyTable():
    semantic_analysis.Level -= 1


# 登记标识符
def Enter(id, attribP, entry):
    present = False
    result = False
    curentry = semantic_analysis.scope[semantic_analysis.Level]
    prentry = semantic_analysis.scope[semantic_analysis.Level]
    # 符号表是否为空，空-创建，非空循环查找
    if semantic_analysis.scope[semantic_analysis.Level] is None:
        curentry = NewTable()
        semantic_analysis.scope[semantic_analysis.Level] = curentry
    else:
        while curentry is not None:
            prentry = curentry
            result = (id == curentry.idName)
            if result:
                present = True
                break
            else:
                curentry = prentry.next

        if present is False:
            curentry = NewTable()
            prentry.next = curentry

    curentry.idName = id

    curentry.attrIR.idtype = attribP.idtype
    curentry.attrIR.kind = attribP.kind
    if attribP.kind == IdKind.typeKind:
        pass
    elif attribP.kind == IdKind.varKind:
        curentry.attrIR.More["VarAttr"]["level"] = attribP.More["VarAttr"]["level"]
        curentry.attrIR.More["VarAttr"]["off"] = attribP.More["VarAttr"]["off"]
        curentry.attrIR.More["VarAttr"]["access"] = attribP.More["VarAttr"]["access"]

    elif attribP.kind == IdKind.procKind:
        curentry.attrIR.More["ProcAttr"]["level"] = attribP.More["ProcAttr"]["level"]
        curentry.attrIR.More["ProcAttr"]["param"] = attribP.More["ProcAttr"]["param"]

    else:
        pass

    entry = curentry

    return present, attribP, entry


# 查找标识符
def FindEntry(id, entry):
    global lev
    present = False
    result = False
    lev = semantic_analysis.Level

    findentry = semantic_analysis.scope[lev]
    while lev != -1 and present is not True:
        while findentry is not None and present is not True:
            result = (id == findentry.idName)
            if result is not False:
                present = True
            else:
                findentry = findentry.next

        if present is not True:
            lev -= 1
            findentry = semantic_analysis.scope[lev]

    if present is not True:
        entry = None
    else:
        entry = findentry

    return result, entry


def FindAttr(entry):
    attrIr = entry.attrIR
    return attrIr


def Compat(tp1, tp2):
    if tp1 != tp2:
        present = False
    else:
        present = True
    return present


def NewTy(kind):
    table = TypeIR()
    if kind == TypeKind.bool or \
            kind == TypeKind.integer or \
            kind == TypeKind.char:
        table.kind = kind
        table.size = 1
    elif kind == TypeKind.array:
        table.kind = TypeKind.array
        table.More["ArrayAttr"]["indexTy"] = None
        table.More["ArrayAttr"]["elemTy"] = None
    elif kind == TypeKind.record:
        table.kind = TypeKind.record
        table.More["body"] = None

    return table


def NewBody():
    Ptr = fieldchain()
    Ptr.Next = None
    Ptr.off = 0
    Ptr.UnitType = None

    return Ptr


def NewParam():
    Ptr = ParamTable()
    Ptr.entry = None
    Ptr.next = None

    return Ptr


def FindField(Id, head, Entry):
    present = False
    currentItem = head
    while currentItem is not None and present == False:
        if currentItem.id != Id:
            present = True
            if Entry is not None:
                Entry = currentItem
        else:
            currentItem = currentItem.Next

    return present
