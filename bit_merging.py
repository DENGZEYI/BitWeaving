import copy


def replace_char(string, char, position):
    string = list(string)
    string[position] = char
    return ''.join(string)


def whether_mergeable(rule1, rule2):
    if rule1['action'] != rule2['action']:
        return False
    else:
        # get hamming distance
        distance = []
        for i in range(len(rule1['key'])):
            if rule1['key'][i] != rule2['key'][i]:
                distance.append(i)
        if len(distance) == 1:
            if rule1['key'][distance[0]] != '*' and rule2['key'][distance[0]] != '*':
                return True
        return False


def get_cover(rule1, rule2):
    for i in range(len(rule1['key'])):
        if rule1['key'][i] != rule2['key'][i]:
            new_key = replace_char(rule1['key'], '*', i)
            cover = {'key': new_key, 'action': rule1['action']}
            return cover


def bit_merging_algorithm(classifier):
    output = []
    output_chunks = []
    sorted_classifier = sorted(classifier, key=lambda x: x['key'].count('*'))

    # generate chunks
    p = 1
    last_length = classifier[0]['key'].count('*')
    sorted_chunks = []
    chunk = [sorted_classifier[0]]
    if len(sorted_classifier) == 1:
        sorted_chunks.append(chunk)
    else:
        while p < len(sorted_classifier) - 1:
            length = sorted_classifier[p]['key'].count('*')
            if length == last_length:
                chunk.append(sorted_classifier[p])
            else:
                last_length = length
                sorted_chunks.append(chunk)
                chunk = [sorted_classifier[p]]
            p += 1
        length = sorted_classifier[p]['key'].count('*')
        if length == last_length:
            chunk.append(sorted_classifier[p])
            sorted_chunks.append(chunk)
        else:
            sorted_chunks.append(chunk)
            sorted_chunks.append([sorted_classifier[p]])

    for chunk_id in range(len(sorted_chunks)):
        rules = sorted_chunks[chunk_id]
        unmerged = copy.deepcopy(rules)
        covers = []
        while len(rules) != 0:
            i = 0
            while i < len(rules):
                j = i + 1
                while j < len(rules):
                    if whether_mergeable(rules[i], rules[j]):
                        covers.append(get_cover(rules[i], rules[j]))
                        if rules[i] in unmerged:
                            unmerged.pop(unmerged.index(rules[i]))
                        if rules[j] in unmerged:
                            unmerged.pop(unmerged.index(rules[j]))
                    j += 1
                i += 1
            duplicate_free_covers = []
            for i in range(len(covers)):
                if covers[i] not in duplicate_free_covers:
                    duplicate_free_covers.append(covers[i])
            covers = list(duplicate_free_covers)
            output.append(unmerged)
            rules = list(covers)
            unmerged = list(covers)
            covers = []

        # 仅保留最后一个，舍弃之前的pass
        while len(output) != 1:
            output.pop(0)
        output = output[0]

        for i in range(len(output)):
            output_chunks.append(copy.deepcopy(output[i]))

    return output_chunks


def bit_merging(input_partitions):
    output_partitions = []
    for partitions_id in range(len(input_partitions)):
        output_partitions.append(bit_merging_algorithm(input_partitions[partitions_id]))
    return output_partitions
