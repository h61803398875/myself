# -*- encoding:utf8 -*-

import json
import logging
import random
import struct
import time

import MySQLdb

import handle_names


class OrgMgmt(object):
    def __init__(self, kfuin, dept_info):

        self.logger = logging.getLogger("OrgMgmt")
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.kfuin = kfuin
        self.dept_info = dept_info

        self.logger.info("kfuin: {0}".format(self.kfuin))

    def parse_org_buf(self):
        # org tree table
        org_tree_table_name = "db_crm3_org.t_org_info"

        # employee list
        select_org_tree_sql = "select FOrgBuf from {0} where FCorpUin={1}".format(org_tree_table_name, self.kfuin)
        self.logger.info("get db_crm3_org.t_org_info buff")
        cursor.execute(select_org_tree_sql)
        org_buf = cursor.fetchall()[0][0]
        self.logger.info("decode db_crm3_org.t_org_info buff")
        org_str = org_buf.decode("hex")

        employees_list = []
        ind = 0
        self.logger.info("parse db_crm3_org.t_org_info buff")
        while ind < len(org_str):
            # Lid/Lpid/Ctype/Ltimestamp
            # public static $department = 1;
            # public static $leader = 11;
            # public static $employee = 10;

            id_, pid_, type_, timestamp_ = struct.unpack("=IIBI", org_str[ind:ind + 13])
            if (type_ == 10 or type_ == 11) and id_ not in employees_list:
                self.logger.debug("employee id:{0}".format(id_))
                employees_list.append(id_)

            ind = ind + 13

        return employees_list

    def org_2_db(self):
        kfuin_mod1000 = self.kfuin % 1000 / 100
        kfuin_mod100 = self.kfuin % 100

        # org name table
        org_name_table_name = "db_crm3_org_{0}.t_department_{1}".format(kfuin_mod1000, kfuin_mod100)

        # clear org name table
        # truncate_sql = "truncate {0}".format(org_name_table_name)
        # embress... replace with delete
        self.logger.info("delete dept infos in {0}, {1}".format(org_name_table_name, self.kfuin))
        delete_sql = "delete from {0} where FCorpUin={1}".format(org_name_table_name, self.kfuin)
        cursor.execute(delete_sql)

        # get employee list
        user_table_name = "qidian_user.t_user_basic_info_{0}".format(kfuin_mod100)
        self.logger.info("get employee in {0}, {1}".format(user_table_name, self.kfuin))
        select_sql = "select FUserUin from {0} where FCorpUin={1}".format(user_table_name, self.kfuin)
        cursor.execute(select_sql)
        employees_list = [employee[0] for employee in cursor.fetchall()]
        self.logger.info("employee list: {0}".format(", ".join([str(x) for x in employees_list])))

        employees_list_copy = employees_list[:]
        # gen org tree
        # (name, id, pid, is_dept, is_leader)
        self.logger.info("gen org tree info")
        _, org_list = self.gen_org_tree(0, 0, employees_list, self.dept_info, employees_list_copy)

        # left employee to root
        self.logger.info("add all not in org tree employee into first dept, num:{0}".format(len(employees_list)))
        while employees_list:
            user_id = employees_list.pop()
            org_list.append(("user_{0}".format(user_id), user_id, 1, False, False))

        # org tree table
        org_tree_table_name = "db_crm3_org.t_org_info"
        # pdb.set_trace()
        new_org_buf_str = ""
        for org_info in org_list:
            # dept
            if org_info[3]:
                # add dept info
                insert_dept_info_sql = "insert into {table_name} (FId,FPId,FCorpUin,FName,FLeader) values " \
                                       "({FId}, {FPId}, {FCorpUin},'{FName}',0)".format(table_name=org_name_table_name,
                                                                                        FId=org_info[1],
                                                                                        FPId=org_info[2],
                                                                                        FCorpUin=self.kfuin,
                                                                                        FName=org_info[0].encode(
                                                                                            "utf8"))

                self.logger.info("add dept info, name:{0}".format(org_info[0].encode("utf8")))
                cursor.execute(insert_dept_info_sql)

            # all
            if org_info[3]:
                org_type = 1
            else:
                if org_info[4]:
                    org_type = 11
                else:
                    org_type = 10

            # Lid/Lpid/Ctype/Ltimestamp
            # public static $department = 1;
            # public static $leader = 11;
            # public static $employee = 10;
            timestamp = int(time.time())
            new_org_buf_str = new_org_buf_str + struct.pack("=IIBI", org_info[1], org_info[2], org_type, timestamp)

        # update org info
        timestamp = int(time.time())
        update_org_info_sql = "update {table_name} set FOrgBuf='{FOrgBuf}', FUpdated=0 where  FCorpUin={FCorpUin}".format(
            table_name=org_tree_table_name,
            FOrgBuf=new_org_buf_str.encode("hex"), FCorpUin=kfuin)

        self.logger.info("update org buff")
        cursor.execute(update_org_info_sql)

        # update employee info
        email_len = 64
        phone_len = 11
        tel_len = 20
        external_position_len = 20

        employee_num = len(employees_list_copy)
        en_names = handle_names.gen_en_name(employee_num)
        ch_names = handle_names.gen_ch_name(employee_num)

        self.logger.info("update employee info")

        for account_id, real_name, account_name in zip(employees_list_copy, ch_names, en_names):
            email = "email{0}@t.com".format(handle_names.genRandomStr(email_len - 11, 2))
            phone = "176{0}".format(handle_names.genRandomStr(phone_len - 3, 0))
            tel = "0455-{0}".format(handle_names.genRandomStr(tel_len - 5, 0))
            gender = random.choice([1, 2])
            external_name = "w/" + real_name
            external_email = "wmail{0}@t.com".format(handle_names.genRandomStr(email_len - 11, 2))
            external_phone = "177{0}".format(handle_names.genRandomStr(phone_len - 3, 0))
            external_tel = "0456-{0}".format(handle_names.genRandomStr(tel_len - 5, 0))
            external_position = random.choice(["测试工程师", "项目经理", "开发工程师", "产品经理"])

            update_employee_sql = "update {table_name} set " \
                                  "FUserStrID='{FUserStrID}', FUserName='{FUserName}', FEmail='{FEmail}', FMobile='{FMobile}', FTEL='{FTEL}'," \
                                  "FExternalName='{FExternalName}', FExternalEmail='{FExternalEmail}', FExternalMobile='{FExternalMobile}', " \
                                  "FExternalTEL='{FExternalTEL}', FExternalPosition='{FExternalPosition}', FGender={FGender}" \
                                  " where FUserUin={FUserUin}".format(table_name=user_table_name,
                                                                      FUserStrID=account_name,
                                                                      FUserName=real_name,
                                                                      FEmail=email, FMobile=phone, FTEL=tel,
                                                                      FExternalName=external_name,
                                                                      FExternalEmail=external_email,
                                                                      FExternalMobile=external_phone,
                                                                      FExternalTEL=external_tel,
                                                                      FExternalPosition=external_position,
                                                                      FGender=gender,
                                                                      FUserUin=account_id)

            self.logger.debug("update employee name:{0}, id:{1}".format(real_name, account_id))

            cursor.execute(update_employee_sql)

    def gen_org_tree(self, pid, last_id, user_list, org_infos, user_list_copy):
        # (name, id, pid, is_dept, is_leader)
        ret_org_infos = []
        for org_info in org_infos:
            if org_info == u"人数":
                curr_dept_users = []
                leader = True
                self.logger.debug("dept employee num:{0}".format(org_infos[org_info]))

                for _ in xrange(org_infos[org_info]):
                    # 10% chance, employee also in other dept
                    if random.randrange(0, 10) == 0:

                        user_id = random.choice(user_list_copy)
                        if user_id not in curr_dept_users:
                            ret_org_infos.append(["user_{0}".format(user_id), user_id, pid, False, leader])
                            leader = False
                            continue

                    # 90% only in curr dept, or random already in curr dept
                    if user_list:
                        user_id = user_list.pop()
                        curr_dept_users.append(user_id)
                        ret_org_infos.append(["user_{0}".format(user_id), user_id, pid, False, leader])
                        leader = False

                self.logger.debug("dept employee:{0}".format(", ".join([str(x) for x in curr_dept_users])))


            else:
                dept_id = last_id + 1
                ret_org_infos.append([org_info, dept_id, pid, True, False])

                self.logger.debug("gen next dept, dept_id:{0}".format(dept_id))
                last_id, sub_org_infos = self.gen_org_tree(dept_id, dept_id, user_list, org_infos[org_info],
                                                           user_list_copy)
                ret_org_infos.extend(sub_org_infos)

        return last_id, ret_org_infos


if __name__ == "__main__":
    # db connect
    mysql_host = "10.189.30.34"
    mysql_port = 3492
    mysql_user = "uds_root"
    mysql_pwd = "uds_root@123"

    db = MySQLdb.connect(mysql_host, mysql_user, mysql_pwd, port=mysql_port)
    cursor = db.cursor()

    # org to db
    kfuin = 2852199895
    # depts = {u"IEG互动娱乐事业群": {u"人数": 1, u"经营管理委员会": {u"人数": 5}}}
    # dept data
    dept_filename = "dept.json"
    with open(dept_filename) as f:
        depts = json.load(f)

    org_mgmt = OrgMgmt(kfuin, depts)

    # org_mgmt.org_2_db()
    # cursor.execute("commit")

    with open("hello.txt2.data", "w") as f:
        f.writelines(org_mgmt.parse_org_buf())

    db.close()
