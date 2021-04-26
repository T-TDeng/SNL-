# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from treelib import Node, Tree
import global_classes


class a:
    def __init__(self):
        self.int = 0



tree = Tree()
point = Node()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    node = global_classes.Node()
    print(len(node.get_sons()))
    tree.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
