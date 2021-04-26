import global_classes

# 关键字表
KEY_WORDS = ["program", "type", "integer", "char", "array", "of", "record", "end", "var", "procedure", "begin",
             "if", "then", "else", "fi", "while", "do", "endwh", "read", "write", "return"]

# 数字后允许出现的字符
SEPARATOR = [' ', '\t', '\r', '\n']
SYMBOL = [';', '.', ']', '+', '-', '*', '/', ')', '<', '>' ',']

# 标识符表
ID_TABLE = []

# 常量表
INIC_TABLE = []

# token序列
TOKEN = []
TOKEN_POINT = 0

# 输入程序文本
WORD = []
WORD_POINT = 0

# 错误提示
ERROR = []


def is_key_word(word):
    """
    判断字符串是否为关键字
    :param word: 待判断的字符串
    :return: 关键字对应下标，未找到为-1
    """
    global KEY_WORDS
    if word in KEY_WORDS:
        return KEY_WORDS.index(word)
    return -1


def add_word_table(table, words):
    """
    向表中添加元素
    :param table:加入的表
    :param words: 添加的元素
    :return:表中存在则返回原有下标，不存在则添加到队尾
    """
    if words in table:
        return table.index(words)
    table.append(words)
    return len(table) - 1


def error(rows, columns, message):
    global ERROR
    ERROR.append(global_classes.Error(rows, columns, message))


def DFA():
    global WORD, WORD_POINT
    global TOKEN, TOKEN_POINT
    global INIC_TABLE
    strin = ''
    start = WORD[WORD_POINT]

    ch = WORD[WORD_POINT].get_character()
    WORD_POINT += 1

    if ch != '\0':
        if ch.isalpha():
            # 不断地将后面的字符取出，直到取出完整的单词
            while True:
                if WORD_POINT == len(WORD) or not (WORD[WORD_POINT].get_character().isalpha() or
                                                   WORD[WORD_POINT].get_character().isdigit()):
                    strin += ch
                    break
                strin += ch
                ch = WORD[WORD_POINT].get_character()
                WORD_POINT += 1
            # 判断是关键字还是标识符
            position = is_key_word(strin)
            if position != -1:
                token = global_classes.Token(type=strin, position=-1, rows=start.get_rows(),
                                             columns=start.get_columns())
                return token
            else:
                # 加入标识符表
                position = add_word_table(ID_TABLE, strin)
                token = global_classes.Token(type='ID', position=position, rows=start.get_rows(),
                                             columns=start.get_columns())
                return token
        if ch.isdigit():
            # 不断地将后面的字符取出，直到取出完整的数字
            while True:
                if not (WORD[WORD_POINT].get_character().isdigit()):
                    strin += ch
                    break
                strin += ch
                ch = WORD[WORD_POINT].get_character()
                WORD_POINT += 1
            if WORD[WORD_POINT].get_character() not in SEPARATOR and WORD[WORD_POINT].get_character() not in SYMBOL:
                error(rows=start.get_rows(), columns=start.get_columns(), message='Illegal Identifier')
                # 将整个错误的单词取出
                while True:
                    if WORD_POINT == len(WORD) or WORD[WORD_POINT].get_character() in SEPARATOR \
                            or WORD[WORD_POINT].get_character() in SYMBOL:
                        break
                    strin += ch
                    WORD_POINT += 1
                return None
            position = add_word_table(INIC_TABLE, strin)
            token = global_classes.Token(type="INIC", position=position, rows=start.get_rows(),
                                         columns=start.get_columns())
            return token
        if ch == '+':
            return global_classes.Token(type='+', position=-1, rows=start.get_rows(), columns=start.get_rows())
        if ch == '-':
            return global_classes.Token(type='-', position=-1, rows=start.get_rows(), columns=start.get_rows())
        if ch == '*':
            return global_classes.Token(type='*', position=-1, rows=start.get_rows(), columns=start.get_rows())
        if ch == '/':
            return global_classes.Token(type='/', position=-1, rows=start.get_rows(), columns=start.get_rows())
        if ch == '<':
            return global_classes.Token(type='<', position=-1, rows=start.get_rows(), columns=start.get_rows())
        if ch == '>':
            return global_classes.Token(type='>', position=-1, rows=start.get_rows(), columns=start.get_rows())
        if ch == ';':
            return global_classes.Token(type=';', position=-1, rows=start.get_rows(), columns=start.get_rows())
        if ch == ':':
            if WORD[WORD_POINT].get_character() == '=':
                WORD_POINT += 1
                return global_classes.Token(type=':=', position=-1, rows=start.get_rows(), columns=start.get_rows())
            else:
                error(rows=start.get_rows(), columns=start.get_columns(), message='Much Character')
                return None
        if ch == ',':
            return global_classes.Token(type=',', position=-1, rows=start.get_rows(), columns=start.get_columns())
        if ch == '.':
            if WORD_POINT != len(WORD) and WORD[WORD_POINT].get_character() == '.':
                WORD_POINT += 1
                return global_classes.Token(type="..", position=-1, rows=start.get_rows(), columns=start.get_columns())
            else:
                return global_classes.Token(type='.', position=-1, rows=start.get_rows(), columns=start.get_columns())
        if ch == '=':
            return global_classes.Token(type='=', position=-1, rows=start.get_rows(), columns=start.get_columns())
        if ch == '[':
            return global_classes.Token(type='[', position=-1, rows=start.get_rows(), columns=start.get_columns())
        if ch == ']':
            return global_classes.Token(type=']', position=-1, rows=start.get_rows(), columns=start.get_columns())
        if ch == '(':
            return global_classes.Token(type='(', position=-1, rows=start.get_rows(), columns=start.get_columns())
        if ch == ')':
            return global_classes.Token(type=')', position=-1, rows=start.get_rows(), columns=start.get_columns())
        if ch == '{':
            while True:
                # 将注释完全掠过
                if WORD_POINT >= len(WORD):
                    error(rows=start.get_rows(), columns=start.get_columns(), message="a '{' is missing!")
                    return None
                if WORD[WORD_POINT].get_character() == '}':
                    break
                WORD_POINT += 1
            WORD_POINT += 1
            return None
        if ch == '}':
            error(rows=start.get_rows(), columns=start.get_columns(), message="a '}' is missing!")
        if ch == "'":
            strin = WORD[WORD_POINT].get_character()
            if WORD[WORD_POINT + 1].get_character() != "'":
                error(rows=start.get_rows(), columns=start.get_columns(), message="a '\'' is missing!")
                return None
            else:
                position = add_word_table(INIC_TABLE, strin)
                WORD_POINT += 2
                return global_classes.Token(type='INIC', position=position, rows=WORD[WORD_POINT-2].get_rows(),
                                            columns=WORD[WORD_POINT-2].get_columns())

        if ch in SEPARATOR:
            return None
        error(rows=start.get_rows(), columns=start.get_columns(), message='Illegal Character')
        return None
    else:
        return None


def lexical_analysis_run(filename):
    global TOKEN
    global WORD, WORD_POINT
    global ERROR
    print('Lexical Analysis start...')
    file_program = open(file=filename, mode='r', encoding='utf-8')
    text = file_program.read()
    # print(len(text))
    line, pos = 0, 0
    point = 0
    for i in range(0, len(text)):
        if i == 0:
            WORD.append(global_classes.Word(character=text[i], rows=1, columns=1))
            point = 0
        else:
            WORD.append(global_classes.Word(character=text[i], rows=1 + line, columns=1 + pos))
            point += 1
            pos += 1
        if text[i] == '\n':
            line += 1
            pos = 0
    point = 0
    while WORD_POINT != len(WORD):
        # if ERROR is not None:
        #     break
        temp = DFA()
        if temp is not None:
            TOKEN.append(temp)
    file_token = open('token.txt', 'w')
    if ERROR:
        for err in ERROR:
            strin = str(err.get_rows()) + '\t' + str(err.get_columns()) + '\t' + str(err.get_message())
            file_token.write(strin)
    else:
        for t in TOKEN:
            strin = str(str(t.get_type()) + '\t' + str(t.get_position()) + '\t' + str(t.get_rows()) + '\t' + str(
                t.get_columns()) + '\n')
            file_token.write(strin)
    file_token.close()

    # 写常量表
    file_constant_table = open('INIC_table.txt', 'w')
    if ERROR:
        for err in ERROR:
            strin = str(err.get_rows()) + '\t' + str(err.get_columns()) + '\t' + str(err.get_message())
            file_constant_table.write(strin)
    else:
        for t in INIC_TABLE:
            strin = str(t) + '\n'
            file_constant_table.write(strin)
    file_constant_table.close()

    # 写标识符表
    file_Identifier_table = open('ID_table.txt', 'w')
    if ERROR:
        for err in ERROR:
            strin = str(err.get_rows()) + '\t' + str(err.get_columns()) + '\t' + str(err.get_message())
            file_Identifier_table.write(strin)
    else:
        for t in ID_TABLE:
            strin = str(t) + '\n'
            file_Identifier_table.write(strin)
    file_Identifier_table.close()


def show_TOKEN():
    global TOKEN
    print('------TOKEN------')
    for t in TOKEN:
        print(str(str(t.get_type()) + '\t' + str(t.get_position()) + '\t' + str(t.get_rows()) + '\t' + str(
            t.get_columns())))


def get_ERROR():
    global ERROR
    return ERROR


def get_TOKEN():
    global TOKEN
    return TOKEN


def get_ID_TABLE():
    global ID_TABLE
    return ID_TABLE


def get_INIC_TABLE():
    global INIC_TABLE
    return INIC_TABLE


def get_KEY_WORDS():
    global KEY_WORDS
    return KEY_WORDS


if __name__ == "__main__":
    lexical_analysis_run('test/program.txt')
    show_TOKEN()
    print('Lexical Analysis over!')
