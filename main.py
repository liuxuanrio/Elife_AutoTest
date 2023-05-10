import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
# This is a sample Python script.
from test.suite.ui_auto_test_suite import OpenFile, AutoFile


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    script_path = os.path.abspath(__file__)[:-8]
    case = OpenFile().testFileCase(script_path)
    for i in case:
        print(f"{script_path}/{i}")
        print(AutoFile().openFile(f"{script_path}/{i}"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
