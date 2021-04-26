class Error:

    def __init__(self, rows=0, columns=0, message=''):
        self.__rows = rows
        self.__columns = columns
        self.__message = message
        print('>>>line', rows, 'columns', columns, ':\t', message)

    def get_rows(self):
        return self.__rows

    def get_columns(self):
        return self.__columns

    def get_message(self):
        return self.__message


class Token:
    def __init__(self, type='', position=0, rows=0, columns=0):
        self.__type = type
        self.__position = position
        self.__rows = rows
        self.__columns = columns

    def get_type(self):
        return self.__type

    def get_position(self):
        return self.__position

    def get_rows(self):
        return self.__rows

    def get_columns(self):
        return self.__columns


class Word:

    def __init__(self, character='', rows=0, columns=0):
        self.__character = character
        self.__rows = rows
        self.__columns = columns

    def get_character(self):
        return self.__character

    def get_rows(self):
        return self.__rows

    def get_columns(self):
        return self.__columns


class Node:

    def __init__(self, name=None, token=None, father=None):
        self.__son_Node = []
        self.__name = name
        self.__token = token
        self.__father = father

    def get_name(self):
        return self.__name

    def add_son(self, strin, father):
        self.__son_Node.append(Node(name=strin, father=father))

    def add_token_son(self, token, father):
        self.__son_Node.append(Node(token=token, father=father))

    def get_sons(self):
        return self.__son_Node

    def get_token(self):
        return self.__token

    def get_father(self):
        return self.__father

    def get_son(self, strin):
        tmp = None
        for son in self.__son_Node:
            if son.get_name() and son.get_name() == strin:
                tmp = son
        return tmp
