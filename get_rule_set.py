import os

number = 1000
i_range = []
j_range = []
k_range = []
for i in range(4, 60, 4):
    i_range.append(i)
for j in range(5):
    j_range.append(-1 + j * 0.4)
    k_range.append(-1 + j * 0.4)
file_name_list = []
for i in i_range:
    for j in j_range:
        for k in k_range:
            name = './rule_set/acl1_seed_{myi}_{myj}_{myk}.rule'.format(myi=i, myj=j, myk=k)
            os.system('./db_generator/db_generator -bc ./parameter_files/acl1_seed \
                {mynumber} {myi} {myj} {myk} {myname}'.format(mynumber=number, myi=i, myj=j, myk=k, myname=name))
