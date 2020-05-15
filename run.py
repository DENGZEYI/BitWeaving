import bit_swapping
import bit_merging
import bit_recovery
import minimizing
from savelist import savelist
import pre_process
import json
import os
import time


def show(input_partitions):
    partition_number = len(input_partitions)
    print("\nnumber of partitions : ", partition_number)
    for i in range(partition_number):
        print("partition ", i, " ", input_partitions[i])
        

def pre_run(rule_list_file_name_path):
    file_name = rule_list_file_name_path.split('/')[-1]
    rule_list = pre_process.pre_process(rule_list_file_name_path)

    # 处理数据并写入文件
    with open('./rule_set_processed/' + file_name, 'w') as f:
        f.write(json.dumps(rule_list))


def run(rule_list_file_name_path):
    # 读取数据
    file_name = rule_list_file_name_path.split('/')[-1]
    with open('./rule_set_processed/' + file_name, 'r') as f:
        rule_list = json.loads(f.read())
    ori_rule_list_length = len(rule_list)
    # bit swapping
    bit_swapping_result, order_list = bit_swapping.bit_swapping(rule_list)
    # with open('intermediate_data/bit_swapping_result.txt', "w", encoding="utf-8") as f:
    #     f.write(savelist.write(bit_swapping_result))
    # minimizing
    # minimizing_result = minimizing.minimizing(bit_swapping_result, order_list)
    # bit merging
    bit_merging_result = bit_merging.bit_merging(bit_swapping_result)
    # with open('intermediate_data/bit_merging_result.txt', "w", encoding="utf-8") as f:
    #     f.write(savelist.write(bit_merging_result))
    # bit recovery
    bit_recovery_result = bit_recovery.bit_recovery(order_list, bit_merging_result)
    # with open('intermediate_data/bit_recovery_result.txt', "w", encoding="utf-8") as f:
    #     f.write(savelist.write(bit_recovery_result))
    # 还原维度
    final_list = bit_recovery.one_d_to_5_d(bit_recovery_result)
    # with open('intermediate_data/final_result.txt', "w", encoding="utf-8") as f:
    #     f.write(savelist.write(final_list))

    rule_list_length = len(final_list)
    return rule_list_length, ori_rule_list_length, rule_list_length / ori_rule_list_length


def experiment():
    summary_rule_list_length = []
    summary_ori_rule_list_length = []
    summary_compressing_ratio = []
    summary = []
    file_name_list = os.listdir('./rule_set')
    for i in range(len(file_name_list)):
        print('rule_set', i, '/', len(file_name_list))
        file_name_path = './rule_set/' + file_name_list[i]
        pre_run(file_name_path)
        # a, b, c = run(file_name_path)
    #     with open('./result/summary_partition.txt', mode='a') as f:
    #         f.write("rule_list_number:" + str(a))
    #         f.write('\t')
    #         f.write("rule_list_number_ori" + str(b))
    #         f.write('\t')
    #         f.write(str(c))
    #         f.write('\n')
    #     summary_rule_list_length.append(a)
    #     summary_ori_rule_list_length.append(b)
    #     summary_compressing_ratio.append(c)
    #     print("processing: " + str(i) + "/" + str(len(file_name_list)))
    # summary.append(summary_rule_list_length)
    # summary.append(summary_ori_rule_list_length)
    # summary.append(summary_compressing_ratio)
    # with open('summary.txt') as file:
    #     file.write(json.dumps(summary))


def test():
    rule_list = [{'0': '**', '1': '100000', 'action': 'a'}, {'0': '**', '1': '100010', 'action': 'a'},
                 {'0': '**', '1': '100100', 'action': 'a'}, {'0': '**', '1': '100110', 'action': 'a'},
                 {'0': '**', '1': '101000', 'action': 'a'}, {'0': '**', '1': '110000', 'action': 'a'},
                 {'0': '**', '1': '111000', 'action': 'a'}, {'0': '01', '1': '******', 'action': 'd'},
                 {'0': '1*', '1': '******', 'action': 'd'}, {'0': '**', '1': '******', 'action': 's'}]
    bit_swapping_result, order_list = bit_swapping.bit_swapping(rule_list)
    print('bit_swapping_result:')
    show(bit_swapping_result)

    minimizing_result = minimizing.minimizing(bit_swapping_result, order_list)
    print('bit_swapping_result:')
    show(bit_swapping_result)

    bit_merging_result = bit_merging.bit_merging(minimizing_result)
    print('bit_merging_result:')
    show(bit_merging_result)

    bit_recovery_result = bit_recovery.bit_recovery(order_list, bit_merging_result)
    print('bit_recovery_result:')
    show(bit_recovery_result)


experiment()
