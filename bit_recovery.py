import copy


def sort_key(order, key):
    odered_string = ''
    for i in range(len(order)):
        odered_string += key[order[i]]
    return odered_string


def bit_recovery(order_partitions, input_partitions):
    recovery_order_partitions = []
    output_partitions = []
    for partition_id in range(len(order_partitions)):
        order = order_partitions[partition_id]
        recovery_order = list(range(len(order)))
        for i in range(len(order)):
            recovery_order[order[i]] = i
        recovery_order_partitions.append(copy.deepcopy(recovery_order))

        input_partition = input_partitions[partition_id]
        output_partition = []
        for rule_id in range(len(input_partition)):
            new_key = sort_key(recovery_order, input_partition[rule_id]['key'])
            output_rule = {'key': new_key, 'action': input_partition[rule_id]['action']}
            output_partition.append(output_rule)
        output_partitions.append(output_partition)
    return output_partitions


def one_d_to_5_d(recovery_list):
    """
    将bit recover后的一维规则集转换成五维规则集
    :param recovery_list:
    :return: ori_list
    """
    multi_d_list = []
    for partition_id in range(len(recovery_list)):
        for rule_id in range(len(recovery_list[partition_id])):
            action = recovery_list[partition_id][rule_id]['action']
            key = recovery_list[partition_id][rule_id]['key']
            src_ip = key[0:32]
            dst_ip = key[32:64]
            src_port = key[64:80]
            dst_port = key[80:96]
            protocol = key[96:104]
            rule = {'src_ip': src_ip, 'dst_ip': dst_ip, 'src_port': src_port, 'dst_port': dst_port,
                    'protocol': protocol, 'action': action}
            multi_d_list.append(rule)
    return multi_d_list
