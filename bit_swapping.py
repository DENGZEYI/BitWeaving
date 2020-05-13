import itertools

# # ori_rule_list:[{'0':'',1:'','action':''}]
# 论文中测试用例
# number_of_keys = 2
# key0_length = 2
# key1_length = 6
# key_length = key0_length + key1_length


number_of_keys = 5
key0_length = 32
key1_length = 32
key2_length = 16
key3_length = 16
key4_length = 8
key_length = key0_length + key1_length + key2_length + key3_length + key4_length


def bit_swapping(ori_rule_list):
    """
    :param ori_rule_list
    :return 一维前缀化的partitions
    """

    """
    如果list2包含list1，返回1，否则返回0
    输入：list列表，列表中每一项是一个rule字典
    """

    def if_contain(list1, list2):
        if len(list1) > len(list2):
            return False
        for i in range(0, len(list1)):
            for j in range(0, len(list2)):
                if list1[i] == list2[j]:
                    if i == len(list1) - 1:
                        return True
                    else:
                        break
                else:
                    if j == len(list2) - 1:
                        return False
                    continue

    '''
    一维化
    input:rule,dict
    output:rule_one_dimension,dict
    '''

    def to_one_dimension(rule):
        key = ''
        for i in range(number_of_keys):
            key += rule[str(i)]
        action = rule['action']
        rule_one_dimension = {'key': key, 'action': action}
        return rule_one_dimension

    '''
    # 将三态的规则转换成bit类型的规则
    # 输入：rule，一维化后的字典{'key':'','action':''}，有*的ternary形式
    # 输出：rule_result，列表
    '''

    def ternary2bit(rule):

        def find_all_asterisk(data, s):
            r_list = []
            for r in range(len(data)):
                if data[r] == s:
                    r_list.append(r)
            return r_list

        '''
        替换字符串中多个指定位置为指定字符
        p:位置列表，c:对应替换的字符列表
        '''

        def multi_sub(string, p, c):
            new = []
            for s in string:
                new.append(s)
            for index, point in enumerate(p):
                new[point] = c[index]
            return ''.join(new)

        asterisk_location = find_all_asterisk(rule['key'], '*')
        number_of_asterisk = len(asterisk_location)
        rule_result = []
        for item in itertools.product(['0', '1'], repeat=number_of_asterisk):
            key = multi_sub(rule['key'], asterisk_location, list(item))
            action = rule['action']
            rule_result.append({'key': key, 'action': action})
        return rule_result

    '''
    输入：rule1，rule2，字典，rule一维化后的字典，{'key': ,'action':}
    输出：如果是'我的包含'的话，返回1，否则返回0
    '''

    def if_my_contain(rule1, rule2):

        def find_all_asterisk(data, s):
            r_list = []
            for r in range(len(data)):
                if data[r] == s:
                    r_list.append(r)
            return r_list

        return if_contain(find_all_asterisk(rule1['key'], '*'), find_all_asterisk(rule2['key'], '*'))

    '''
    判断两条规则是否cross
    输入：rule1，rule2，字典，rule一维化后的字典，{'key': ,'action':}
    输出：返回1，crosspattern;否则返回0
    '''

    def if_cross(rule1, rule2):
        # 首先将规则一维化
        rule1 = to_one_dimension(rule1)
        rule2 = to_one_dimension(rule2)
        if not if_my_contain(rule1, rule2) and not if_my_contain(rule2, rule1):
            return 1
        else:
            return 0

    '''
    论文中algorithm 1
    将原始的规则集分割为cross_free的partition
    '''

    def find_minimal_partition_algorithm(rule_list):
        l_list = []
        p_list = []
        number_of_rule_list = len(rule_list)
        for i in reversed(range(number_of_rule_list)):
            flag = 0
            if not p_list:
                p_list.append(rule_list[i])
                continue
            for k in range(len(p_list)):
                if if_cross(rule_list[i], p_list[k]):
                    l_list.append(p_list)
                    p_list = [rule_list[i]]
                    flag = 1
                    break
            if flag != 1:
                p_list.append(rule_list[i])
            if i == 0:
                l_list.append(p_list)
        return l_list

    '''
    将分割后的数据集转换为前缀式
    输入：rule_list_partitions，分割后的数据集，[[{},{}],[{},{}]]
    输出：转换后的一维的prefix数据集
    '''

    def to_prefix(rule_list_partitions):
        def rule_list_to_one_dimension(input_rule_list):
            rule_list_one_dimension = []
            for i in range(len(input_rule_list)):
                prefix_rule_partition_one_dimension = []
                for j in range(len(input_rule_list[i])):
                    prefix_rule_partition_one_dimension.append(to_one_dimension(input_rule_list[i][j]))
                rule_list_one_dimension.append(prefix_rule_partition_one_dimension)
            return rule_list_one_dimension

        '''
        输出:每个partition中每位bit对应所拥有的*的个数,[[],[],[]]
        '''

        def asterisk_each_column(input_rule_list):
            # key_length = key0_length + key1_length
            output = []
            for partition_id in range(len(input_rule_list)):
                number_of_asterisk_list = []
                for i in range(key_length):
                    number_of_asterisk = 0
                    for rule_id in range(len(input_rule_list[partition_id])):
                        if input_rule_list[partition_id][rule_id]['key'][i] == '*':
                            number_of_asterisk += 1
                    number_of_asterisk_list.append(number_of_asterisk)
                output.append(number_of_asterisk_list)
            return output

        def swapping_order(input_rule_list):
            order = []
            for i in range(len(input_rule_list)):
                sorted_input = sorted(enumerate(input_rule_list[i]), key=lambda x: x[1])
                order.append([i[0] for i in sorted_input])
            return order

        def swapping_1d_rule_list_partitions(input_rule_list):
            def sort_key(order, key):
                odered_string = ''
                for i in range(len(order)):
                    odered_string += key[order[i]]
                return odered_string

            swapped_partitions = []
            for partition_id in range(len(input_rule_list)):
                swapped_list = []
                for rule_id in range(len(input_rule_list[partition_id])):
                    new_key = sort_key(order_list_result[partition_id], input_rule_list[partition_id][rule_id]['key'])
                    new_rule = {'key': new_key, 'action': input_rule_list[partition_id][rule_id]['action']}
                    swapped_list.append(new_rule)
                swapped_partitions.append(swapped_list)
            return swapped_partitions

        rule_list_1d = rule_list_to_one_dimension(rule_list_partitions)
        asterisk_each_column_list = asterisk_each_column(rule_list_1d)
        order_list_result = swapping_order(asterisk_each_column_list)
        swapped_prefix_partitions_1d = swapping_1d_rule_list_partitions(rule_list_1d)
        return swapped_prefix_partitions_1d, order_list_result

    partitions = find_minimal_partition_algorithm(ori_rule_list)
    prefix_1d_partitions, order_list = to_prefix(partitions)
    # 将顺序调换回来
    prefix_1d_partitions.reverse()
    for i in range(len(prefix_1d_partitions)):
        prefix_1d_partitions[i].reverse()
    order_list.reverse()
    return prefix_1d_partitions, order_list
