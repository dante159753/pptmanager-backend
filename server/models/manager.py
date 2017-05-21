# -*- coding: utf-8 -*-

from server import db_conn
from server.util import format_by_formater

def backmanager_formatter(backmanager_tuple):
    return {
        'id': backmanager_tuple[0],
        'username': backmanager_tuple[1],
        'is_super': backmanager_tuple[2]
    }


class BackManagerHelper:
    @staticmethod
    @format_by_formater(backmanager_formatter)
    def get_by_id(manager_id):
        cursor = db_conn.get_db().cursor()
        cursor.execute('select id, username, is_super from backend_manager where id=%s', [manager_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(backmanager_formatter)
    def get_by_name(manager_name):
        cursor = db_conn.get_db().cursor()
        cursor.execute('select id, username from manager_account where username=%s', (manager_name,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(backmanager_formatter, True)
    def get_all():
        cursor = db_conn.get_db().cursor()
        cursor.execute('select id, username from manager_account')
        return cursor.fetchall()

    @staticmethod
    def create_manager(username, password, auth_list=None):
        if ManagerHelper.get_by_name(username) is not None:
            return False
            
        db = db_conn.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into manager_account (username, password) "
            "values (%s, %s)", 
            (username, password)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            if auth_list:
                # get created manager
                manager = ManagerHelper.get_by_name(username)
                # success, insert authorities
                is_success = True
                for auth_id in auth_list:
                    if AuthorityHelper.get_by_id(auth_id) is not None:
                        if not AuthorityHelper.add_authority(manager['manager_id'], auth_id):
                            is_success = False
                        else:
                            pass
                    else:
                        pass
    
                return is_success
            else:
                return True

    @staticmethod
    def modify_username(manager_id, manager_name):
        if ManagerHelper.get_by_id(manager_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update manager_account set username=%s where id=%s", 
            (manager_name, manager_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def modify_password(manager_id, password):
        if ManagerHelper.get_by_id(manager_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update manager_account set password=%s where id=%s", 
            (password, manager_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def check_password(manager_name, password):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select count(*) from manager_account where username=%s and password=%s', 
            (manager_name, password)
            )
        return cursor.fetchone()[0] == 1

    @staticmethod
    def delete_by_id(manager_id):
        if ManagerHelper.get_by_id(manager_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from manager_account where id=%s", 
            (manager_id,)
            )
        db.commit()
        return cursor.rowcount == 1

