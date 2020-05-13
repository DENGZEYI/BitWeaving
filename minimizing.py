import copy
import operator
import math


def replace_char(string, char, position):
    string = list(string)
    string[position] = char
    return ''.join(string)


class Queue:
    def __init__(self):
        self.__list = list()

    def isEmpty(self):
        return self.__list == []

    def push(self, data):
        self.__list.append(data)

    def pop(self):
        if self.isEmpty():
            return False
        return self.__list.pop(0)


def breadth_traversal(tree):
    queue = Queue()
    queue.push(tree)
    result = []
    while not queue.isEmpty():
        node = queue.pop()
        result.append(node)
        right_child = node.getRightChild()
        left_child = node.getLeftChild()
        if left_child is not None:
            queue.push(left_child)
        if right_child is not None:
            queue.push(right_child)
    return result


# def show(root):
#     result = breadth_traversal(root)
#     for i in range(len(result)):
#         print(result[i].dict_list, file=f)
#         print(result[i].path, file=f)
#         # if result[i].parent is not None:
#         #     print("parent:")
#         #     print(result[i].parent.dict_list)
#         print("\n", file=f)
#

def inherited(node):
    if node.parent.dict_list[0]['action'] != '':
        return node.parent.dict_list
    else:
        return inherited(node.parent)


def find_index(input_list, element):
    for i in range(len(input_list)):
        if element == input_list[i]:
            return i


def find_index_list(str_input, char):
    char_index = []
    for i in range(len(str_input)):
        if char == str_input[i]:
            char_index.append(i)
    return char_index


def my_operation(list_left, list_right, list_parent):
    list_left_action = []
    list_right_action = []
    result = copy.deepcopy(list_left)

    for i in range(len(list_left)):
        list_left_action.append(list_left[i]['action'])
    for i in range(len(list_right)):
        list_right_action.append(list_right[i]['action'])

    for i in range(len(list_right_action)):
        if list_right_action[i] not in list_left_action:
            result.append(copy.deepcopy(list_right[i]))
        else:
            index = find_index(list_left_action, list_right_action[i])
            new_cost = list_left[index]['cost'] + list_right[i]['cost']
            result[index]['cost'] = copy.deepcopy(new_cost)
    # for i in range(len(result)):
    #     if list_parent[0]['action'] == result[i]['action']:
    #         temp = list_parent[0]['cost'] + result[i]['cost']
    #         result[i]['cost'] = temp

    return result


def contained_in(action, list2):
    list2_action = []
    action = [action]
    for i in range(len(list2)):
        list2_action.append(list2[i]['action'])
    result = set(action).issubset(set(list2_action))
    return result


def is_default_rule(input_rule):
    key = input_rule['key']
    for i in range(len(key)):
        if key[i] != '*':
            return False
    return True


class BinaryTree:
    def __init__(self, action, cost, parent):
        self.dict_list = [{'action': action, 'cost': cost}]
        self.path = []
        self.leftChild = None
        self.rightChild = None
        self.parent = parent

    def insertLeft(self, newNode, cost, parent):
        if self.leftChild is None:
            self.leftChild = BinaryTree(newNode, cost, parent)
            path = copy.deepcopy(self.path)
            path.append('1')
            self.leftChild.path = path
        else:
            t = BinaryTree(newNode, cost, parent)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode, cost, parent):
        if self.rightChild is None:
            self.rightChild = BinaryTree(newNode, cost, parent)
            path = copy.deepcopy(self.path)
            path.append('0')
            self.rightChild.path = path
        else:
            t = BinaryTree(newNode, cost, parent)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setVal(self, obj, cost):
        self.dict_list = [{'action': obj, 'cost': cost}]

    def setDictList(self, new_list):
        self.dict_list = new_list

    def getVal(self):
        return self.dict_list

    def middle_digui(self, root):
        if root is None:
            return
        else:
            self.middle_digui(root.leftChild)
            print(root.dict_list)
            self.middle_digui(root.rightChild)


def algorithm_ORTC(input_rule_list, default_rule):
    """
    一维优化，参考论文constructing optimal ip routing tables
    :param default_rule:default rule
    :param input_rule_list:按照prefix长度递减的方式排列好的规则集列表，形式：[{'key',:'','action':''}]
    :return output:一维最小化后的列表
    """
    # 构造树，1向左，0向右
    t = BinaryTree(default_rule['action'], 1, None)
    root = t
    for rule_id in range(len(input_rule_list)):
        rule = input_rule_list[rule_id]
        t = root
        for index in range(len(rule['key'])):
            if index != len(rule['key']) - 1:
                if rule['key'][index] == '1':
                    if t.leftChild is None:
                        t.insertLeft('', 0, t)
                    t = t.getLeftChild()
                    continue
                if rule['key'][index] == '0':
                    if t.rightChild is None:
                        t.insertRight('', 0, t)
                    t = t.getRightChild()
                    continue
                if rule['key'][index] == '*':
                    break
            else:
                if rule['key'][index] == '*':
                    break
                if rule['key'][index] == '1':
                    t.insertLeft(rule['action'], 0, t)
                    break
                if rule['key'][index] == '0':
                    t.insertRight(rule['action'], 0, t)
                    break

    # print("中序遍历构造好的树的结果：")
    # show(root)

    # pass1
    node_list = breadth_traversal(root)
    for i in range(len(node_list)):
        # # 根节点不补全子节点
        # if node_list[i].parent is None:
        #     continue
        if node_list[i].getLeftChild() is not None and node_list[i].getRightChild() is None:
            node_list[i].insertRight(node_list[i].getVal()[0]['action'], node_list[i].getVal()[0]['cost'], node_list[i])
            right_child = node_list[i].getRightChild()
            if right_child.dict_list[0]['action'] == '':
                right_child.setVal(inherited(right_child)[0]['action'], inherited(right_child)[0]['cost'])
        if node_list[i].getRightChild() is not None and node_list[i].getLeftChild() is None:
            node_list[i].insertLeft(node_list[i].getVal()[0]['action'], node_list[i].getVal()[0]['cost'], node_list[i])
            left_child = node_list[i].getLeftChild()
            if left_child.dict_list[0]['action'] == '':
                left_child.setVal(inherited(left_child)[0]['action'], inherited(left_child)[0]['cost'])
    # print("中序遍pass1中补全好的树的结果：")
    # show(root)

    # pass2
    node_list = breadth_traversal(root)
    node_list.reverse()
    for i in range(len(node_list)):
        if node_list[i].getLeftChild() is not None and node_list[i].getRightChild() is not None:
            left_child = node_list[i].getLeftChild()
            right_child = node_list[i].getRightChild()
            node_list[i].setDictList(
                my_operation(left_child.getVal(), right_child.getVal(),
                             node_list[i].getVal()))
    # print('pas2:', file=f)
    # show(root)

    # pass3
    # print(default_action)
    default_list = root.getVal()
    default_action = sorted(default_list, key=lambda x: x['cost'], reverse=True)[0]
    root.setDictList([default_action])
    node_list = breadth_traversal(root)
    for i in range(1, len(node_list)):
        # a = inherited(node_list[i])[0]['action']
        # b = node_list[i].dict_list
        # c = contained_in(a,b)
        if contained_in(inherited(node_list[i])[0]['action'], node_list[i].dict_list):
            node_list[i].setDictList([{'action': '', 'cost': 0}])
        else:
            a = sorted(node_list[i].getVal(), key=operator.itemgetter('cost'), reverse=True)
            node_list[i].setDictList([a[0]])
    # print('pass3:', file=f)
    # show(root)

    # 从二叉树中选出结果
    output = []
    node_list = breadth_traversal(root)
    length = len(default_rule['key'])
    for i in range(len(node_list)):
        if node_list[i].dict_list[0]['action'] != '':
            output.append(
                {'key': (''.join(node_list[i].path)).ljust(length, '*'), 'action': node_list[i].dict_list[0]['action']})
    output.reverse()
    # print(output, file=f)
    return output


def ternary_2_prefix_format(extra_input_list):
    if len(extra_input_list) == 0:
        return []
    # 构造之前partition,需要注意的是extra_input_list中的规则并非前缀式，需要进行转换
    output = []
    key_length = len(extra_input_list[0]['key'])
    for rule_id in range(len(extra_input_list)):
        # print(extra_input_list[rule_id], '/', len(extra_input_list))
        char_list = []
        rule = extra_input_list[rule_id]
        index_list = find_index_list(rule['key'], '*')
        # 如果没有*
        if len(index_list) == 0:
            output.append(rule)
            continue
        # 处理连串*在结尾的情况,将连串的在结尾处的*去除掉，剩下在字符串中间的*,不考虑全是*
        last = key_length - 1
        number = 0
        for i in reversed(range(len(index_list))):
            if index_list[i] == last:
                number += 1
                last -= 1
        for i in range(number):
            index_list.pop()

        # 不处理中间是*的情况
        if len(index_list) != 0:
            continue
        else:
            output.append(extra_input_list[rule_id])
            continue

        # # 将中间的*替换为1或0
        # number = pow(2, len(index_list))
        # # print("* length:", len(index_list))
        # for i in range(number):
        #     char_list.append(((str(bin(i)))[2:]).rjust(len(index_list), '0'))
        # for i in range(len(char_list)):
        #     key = rule['key']
        #     for j in range(len(index_list)):
        #         key = replace_char(key, char_list[i][j], index_list[j])
        #         output.append({'key': key, 'action': 'extra'})

    return output


def algorithm_ORTC_prefix_shadowing(input_rule_list, extra_input_list, default_rule):
    """
    一维优化，参考论文constructing optimal ip routing tables
    :param extra_input_list: prefix_shadowing
    :param default_rule:default rule
    :param input_rule_list:按照prefix长度递减的方式排列好的规则集列表，形式：[{'key',:'','action':''}]
    :return output:一维最小化后的列表
    """
    # 构造树，1向左，0向右，先构建当前partition
    t = BinaryTree(default_rule['action'], 1, None)
    root = t
    for rule_id in range(len(input_rule_list)):
        rule = input_rule_list[rule_id]
        p = root
        for index in range(len(rule['key'])):
            if rule['key'][index] == '1':
                if p.leftChild is None:
                    p.insertLeft('', 0, p)
                p = p.getLeftChild()
            if rule['key'][index] == '0':
                if p.rightChild is None:
                    p.insertRight('', 0, p)
                p = p.getRightChild()
            if rule['key'][index] == '*':
                p.setVal(rule['action'], 1)
            if index == len(rule['key']) - 1:
                p.setVal(rule['action'], 1)
    # print("中序遍历添加了当前partition的树的结果：", file=f)
    # show(root)

    shadowing_p = ternary_2_prefix_format(extra_input_list)
    for rule_id in range(len(shadowing_p)):
        rule = shadowing_p[rule_id]
        p = root
        for index in range(len(rule['key'])):
            if index != len(rule['key']) - 1:
                if rule['key'][index] == '1':
                    if p.leftChild is None:
                        p.insertLeft('', 0, p)
                    p = p.getLeftChild()
                    continue
                if rule['key'][index] == '0':
                    if p.rightChild is None:
                        p.insertRight('', 0, p)
                    p = p.getRightChild()
                    continue
                if rule['key'][index] == '*':
                    break
            else:
                if rule['key'][index] == '*':
                    break
                if rule['key'][index] == '1':
                    p.insertLeft(rule['action'], 0, p)
                    break
                if rule['key'][index] == '0':
                    p.insertRight(rule['action'], 0, p)
                    break

    # print("中序遍历添加了以前partition的树的结果：", file=f)
    # show(root)

    # pass1
    node_list = breadth_traversal(root)
    for i in range(len(node_list)):
        # # 根节点不补全子节点
        # if node_list[i].parent is None:
        #     continue
        if node_list[i].getLeftChild() is not None and node_list[i].getRightChild() is None:
            node_list[i].insertRight(node_list[i].getVal()[0]['action'], node_list[i].getVal()[0]['cost'], node_list[i])
            right_child = node_list[i].getRightChild()
            if right_child.dict_list[0]['action'] == '':
                right_child.setVal(inherited(right_child)[0]['action'], inherited(right_child)[0]['cost'])
        if node_list[i].getRightChild() is not None and node_list[i].getLeftChild() is None:
            node_list[i].insertLeft(node_list[i].getVal()[0]['action'], node_list[i].getVal()[0]['cost'], node_list[i])
            left_child = node_list[i].getLeftChild()
            if left_child.dict_list[0]['action'] == '':
                left_child.setVal(inherited(left_child)[0]['action'], inherited(left_child)[0]['cost'])
    # print("中序遍pass1中补全好的树的结果：", file=f)
    # show(root)

    # pass2
    node_list = breadth_traversal(root)
    node_list.reverse()
    for i in range(len(node_list)):
        if node_list[i].getLeftChild() is not None and node_list[i].getRightChild() is not None:
            left_child = node_list[i].getLeftChild()
            right_child = node_list[i].getRightChild()
            node_list[i].setDictList(
                my_operation(left_child.getVal(), right_child.getVal(),
                             node_list[i].getVal()))
    # print('pas2:', file=f)
    # show(root)

    # pass3
    default_list = root.getVal()
    default_index = 0
    for i in range(len(default_list)):
        if default_list[i]['action'] == 'default':
            default_index = i
            break
    root.setDictList([default_list[default_index]])
    # print(default_action)
    node_list = breadth_traversal(root)
    for i in range(1, len(node_list)):
        # a = inherited(node_list[i])[0]['action']
        # b = node_list[i].dict_list
        # c = contained_in(a,b)
        if contained_in(inherited(node_list[i])[0]['action'], node_list[i].dict_list):
            node_list[i].setDictList([{'action': '', 'cost': 0}])
        else:
            a = sorted(node_list[i].getVal(), key=operator.itemgetter('cost'), reverse=True)
            node_list[i].setDictList([a[0]])
    # print('pass3:', file=f)
    # show(root)

    # 从二叉树中选出结果
    output = []
    node_list = breadth_traversal(root)
    length = len(default_rule['key'])
    for i in range(len(node_list)):
        if node_list[i].dict_list[0]['action'] != '' and node_list[i].dict_list[0]['action'] != 'extra' \
                and node_list[i].dict_list[0]['action'] != 'default':
            output.append(
                {'key': (''.join(node_list[i].path)).ljust(length, '*'), 'action': node_list[i].dict_list[0]['action']})
    output.reverse()
    # print("result:", file=f)
    # print(output, file=f)
    return output


def get_recover_order(order):
    recovery_order = list(range(len(order)))
    for i in range(len(order)):
        recovery_order[order[i]] = i
    return recovery_order


def change_order(rule_set, order):
    output = []
    for i in range(len(rule_set)):
        new_key = ''
        for j in range(len(order)):
            new_key += rule_set[i]['key'][order[j]]
        new_action = rule_set[i]['action']
        output.append({'key': new_key, 'action': new_action})
    return output


def minimizing(partitions, order_list):
    for i in range(1, len(partitions)):
        print("partition: ", i)
        previous_rule_set = []
        for j in range(len(partitions)):
            if j >= i:
                break
            else:
                a = change_order(partitions[j], get_recover_order(order_list[j]))
                b = change_order(a, order_list[i])
                for m in range(len(b)):
                    previous_rule_set.append({'key': b[m]['key'], 'action': 'extra'})
        default_key = '*' * len(partitions[0][0]['key'])
        default = {'key': default_key, 'action': 'default'}
        temp = algorithm_ORTC_prefix_shadowing(partitions[i], previous_rule_set, default)
        print(len(partitions[i])/len(temp))
        partitions.insert(i+1, temp)
        partitions.pop(i)
    return partitions


def minimizing_no_prefix_shadowing(partitions, order_list):
    for i in range(len(partitions)):
        default_key = '*' * len(partitions[0][0]['key'])
        default = {'key': default_key, 'action': 'default'}
        # 有问题
        temp = algorithm_ORTC_prefix_shadowing(partitions[i], [], default)
        partitions.insert(i+1, temp)
        partitions.pop(i)
    return partitions
# f = open('./intermediate_data/minimizing_log.txt', 'w')
# input_rule_list1 = [{'key': '00*', 'action': '2'}, {'key': '10*', 'action': '2'}, {'key': '11*', 'action': '3'}]
# default_rule1 = {'key': '***', 'action': '1'}
# input_rule_list2 = [{'key': '01', 'action': '2'}, {'key': '1*', 'action': '2'}]
# default_rule2 = {'key': '**', 'action': '0'}
# input_rule_list3 = [{'key': '1111100110011110011000010111000001111111001011010110010111010000000110101000010100000110'
#                             '****************', 'action': '1'}, {
#                         'key': '1111100110011110011000010111000001111111001011010110010111010000000110101000010100000'
#                                '111****************',
#                         'action': '3'}]
# default_rule3 = {'key': '*' * 104, 'action': '2'}
# # algorithm_ORTC(input_rule_list3, default_rule3)
# input_rule_list4 = [{'key': '010*', 'action': 'a'}, {'key': '0110', 'action': 'a'}, {'key': '00**', 'action': 'a'}]
# input_rule_list_shadowing = [{'key': '*000', 'action': 'extra'}, {'key': '0111', 'action': 'extra'}]
# default_rule4 = {'key': '****', 'action': 'default'}
# # algorithm_ORTC_prefix_shadowing(input_rule_list4, input_rule_list_shadowing, default_rule4)
# input_list = [[{'key': '00*0', 'action': 'd'}, {'key': '1101', 'action': 'd'}],
#               [{'key': '010*', 'action': 'a'}, {'key': '0110', 'action': 'a'}, {'key': '00**', 'action': 'a'}]]
#
# input_order = [[2, 3, 0, 1], [0, 1, 2, 3]]
# print(minimizing(input_list, input_order))
# f.close()
