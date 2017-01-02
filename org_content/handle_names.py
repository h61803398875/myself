# -*- encoding: utf8 -*-

import random


def handle_en_name_from_origin():
    with open("ch-name.origin.txt") as f:
        lines = f.readlines()

    with open("ch-name.txt", "w") as f:
        new_lines = []
        for line in lines:
            new_lines.append(line.split(" ")[0] + "\n")
        # delete last \n
        new_lines[-1] = new_lines[-1][:-1]

        f.writelines(new_lines)


def handle_ch_name_from_origin():
    with open("ch-name.origin.txt") as f:
        lines = f.readlines()

    with open("ch-name.txt", "w") as f:
        new_lines = []
        for line in lines:
            # filter empty line
            if line:
                names = line.split(",")
                # filter empty
                names = [name.strip().replace("?", "") + "\n" for name in names if name.strip()]
                new_lines.extend(names)

        # delete last \n
        new_lines[-1] = new_lines[-1][:-1]

        f.writelines(new_lines)


def handle_ch_family_name_from_origin():
    with open("ch-family-name.origin.txt") as f:
        lines = f.readlines()

    with open("ch-family-name.txt", "w") as f:
        new_lines = []
        for line in lines:
            # filter empty line
            if line:
                names = line.split(",")
                # filter empty
                names = [name.strip().replace("?", "") + "\n" for name in names if name.strip()]
                new_lines.extend(names)

        # delete last \n
        new_lines[-1] = new_lines[-1][:-1]

        f.writelines(new_lines)


def genRandomStr(memberLen=5, memberType=1):
    """
    memberLen:字符串len
    memberType: 
        0- 数字
        1- 字母
        2- 字母数字
        3- 字母数字符号
    """
    if memberType < 0 or memberType > 3:
        memberType = 1
    if memberLen < 1:
        memberLen = 1

    import random
    import string

    memberTypeDict = {
        0: string.digits,
        1: string.letters,
        2: string.letters + string.digits,
        3: string.printable
    }

    return "".join([random.choice(memberTypeDict.get(memberType)) for _ in xrange(memberLen)])


def gen_en_name(names_num=5000, name_file="en-name.txt"):
    with open(name_file) as f:
        names = f.readlines()

    full_names = []

    while True:
        for name in names:
            full_name = name.strip() + genRandomStr(10 - len(name.strip()), 2).upper()

            if full_name not in full_names:
                full_names.append(full_name)

                if len(full_names) >= names_num:
                    return full_names


def gen_ch_name(names_num=5000, name_file="ch-name.txt", family_name_file="ch-family-name.txt"):
    with open(name_file) as f:
        names = f.readlines()

    with open(family_name_file) as f:
        family_names = f.readlines()

    full_names = []

    while True:
        for name in names:

            the_family_name = random.choice(family_names).strip()
            the_name = name.strip()

            full_name = the_family_name + the_name + genRandomStr(10 - len(the_name) - len(the_family_name), 2).upper()

            if full_name not in full_names:
                full_names.append(full_name)

                if len(full_names) >= names_num:
                    return full_names


if __name__ == "__main__":
    # handle_ch_family_name_from_origin()
    # handle_en_name_from_origin()
    # handle_ch_name_from_origin()
    # print gen_en_name(3)
    print gen_ch_name(3)
