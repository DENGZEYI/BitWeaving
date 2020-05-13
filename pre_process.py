import copy
import time


class IpAddrConverter(object):

    def __init__(self, ip_addr):
        self.ip_addr = ip_addr

    @staticmethod
    def _get_bin(target):
        if not target.isdigit():
            raise Exception('bad ip address')
        target = int(target)
        assert target < 256, 'bad ip address'
        res = ''
        temp = target
        for t in range(8):
            a, b = divmod(temp, 2)
            temp = a
            res += str(b)
            if temp == 0:
                res += '0' * (7 - t)
                break
        return res[::-1]

    def to_32_bin(self):
        temp_list = self.ip_addr.split('.')
        assert len(temp_list) == 4, 'bad ip address'
        return ''.join(list(map(self._get_bin, temp_list)))


def get_diff_index(str1, str2):
    diff = []
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            diff.append(i)
        continue
    return diff


def if_mergable(port_list):
    for i in range(len(port_list) - 1):
        dif_index = get_diff_index(port_list[i], port_list[i + 1])
        if len(dif_index) == 1:
            return True
    return False


def replace_char(string, char, position):
    string = list(string)
    string[position] = char
    return ''.join(string)


def merge(port_list):
    new_port_list = []
    i = 0
    while i < len(port_list):
        if i < len(port_list) - 1:
            dif_index = get_diff_index(port_list[i], port_list[i + 1])
            if len(dif_index) == 1:
                ternary_format = replace_char(port_list[i], '*', dif_index[0])
                new_port_list.append(ternary_format)
                i += 2
            else:
                new_port_list.append(port_list[i])
                i += 1
        else:
            new_port_list.append(port_list[len(port_list) - 1])
            break
    return new_port_list


def get_ternary_format(port_list):
    while if_mergable(port_list):
        port_list = merge(port_list)
    return port_list


def get_port_ternary_form(start_port, end_port):
    if start_port == end_port:
        return [bin(start_port)[2:].rjust(16, '0')]
    else:
        port_list = []
        for i in range(start_port, end_port + 1):
            port_list.append(bin(i)[2:].rjust(16, '0'))
        return get_ternary_format(port_list)


def pre_process(rule_list_file):
    start_time = time.time()
    rule_list = []
    rule_index = 1
    with open(rule_list_file, mode='r') as f:
        for line in f:
            line_start_time = time.time()
            context = line.split('\t')
            # get src_addr
            src_addr = context[0][1:].split('/')[0]
            src_mask = int(context[0][1:].split('/')[1])
            src_addr = IpAddrConverter(src_addr).to_32_bin()[0:src_mask].ljust(32, '*')
            # get dst_addr
            dst_addr = context[1].split('/')[0]
            dst_mask = int(context[1].split('/')[1])
            dst_addr = IpAddrConverter(dst_addr).to_32_bin()[0:dst_mask].ljust(32, '*')
            # src_port_ternary_list
            src_port = context[2]
            src_port_start = int(src_port.split(' : ')[0])
            src_port_end = int(src_port.split(' : ')[1])
            src_port_ternary_list = get_port_ternary_form(src_port_start, src_port_end)
            # dst_port_ternary_list
            dst_port = context[3]
            dst_port_start = int(dst_port.split(' : ')[0])
            dst_port_end = int(dst_port.split(' : ')[1])
            dst_port_ternary_list = get_port_ternary_form(dst_port_start, dst_port_end)
            # get protocol
            # 协议这部分先就没有掩码吧
            protocol = context[4].split('/')[0]
            protocol = bin(int(protocol, 16))[2:].rjust(8, '0')
            # get flag 去掉结尾的换行符
            flag = 'accept'
            # flag = context[5].split('/')[0]
            # flag = bin(int(flag, 16))[2:].rjust(16, '0')

            src_length = len(src_port_ternary_list)
            dst_length = len(dst_port_ternary_list)

            for i in range(src_length):
                for j in range(dst_length):
                    rule = {'0': src_addr, '1': dst_addr, '2': src_port_ternary_list[i],
                            '3': dst_port_ternary_list[j], '4': protocol, 'action': flag}
                    rule_list.append(rule)
            rule_index += 1
            print('line:', rule_index, time.time()-line_start_time)
    end_time = time.time()
    print("total time: ", start_time - end_time)
    return rule_list
