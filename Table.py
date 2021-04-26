from enum import Enum


# 声明类型
class DecKind(Enum):
    array = 1
    char = 2
    integer = 3
    record = 4
    ID = 5


# 直接变量-1 间接-2
class AccessKind(Enum):
    dir = 1
    indir = 2


# 标识符类型typeKind-1 varKind-2  procKind-3
class IdKind(Enum):
    typeKind = 1
    varKind = 2
    procKind = 3


# 参数表-过程中使用的表
class ParamTable:
    def __init__(self):
        self.entry = Symbtable()
        self.next = ParamTable()


# 标识符信息
class AttributeIR:
    def __init__(self):
        self.idtype = None
        # 类型内部表示  typeIR
        self.kind = None
        # 标识符类型 kind
        self.More = {
            "VarAttr": {
                "access": None,  # AccessKind-直接间接变量
                "level": 0,
                "off": 0,
            },
            "ProcAttr": {
                "level": 0,
                "param": None,  # 参数表 ParamTable
            }
        }


# 符号表 idname-标识符  attrIR-标识符信息 next-下一个SymbTable
class Symbtable:
    def __init__(self):
        self.idName = ""
        self.attrIR = AttributeIR()
        self.next = None


# 类型种类  intTy-1 charTy-2 arrayTy-3 recordTy-4 boolTy-5
class TypeKind(Enum):
    integer = 1
    char = 2
    array = 3
    record = 4
    bool = 5


# 域类型单元结构 Body使用
class fieldchain:
    def __init__(self):
        self.id = [] * 10
        # 变量名
        self.off = None
        # 偏移
        self.UnitType = None
        # 成员类型
        self.Next = None


# 类型内部结构
class TypeIR:
    def __init__(self):
        self.size = 0
        # 占用空间大小
        self.kind = None
        # 类型 TypeKind
        self.More = \
            {
                "ArrayAttr": {"indexTy": None, "elemTy": None, "low": 0, "up": 0},
                # 数组类型时有效 indexTy 数组下标类型 elemTy 数组元素类型
                "body": None
                # 记录类型时有效 记录类型中的域链fieldchain
            }


INITOFF = 0
SCOPESIZE = 1000
