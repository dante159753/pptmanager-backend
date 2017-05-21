# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater


def backmanager_formatter(backmanager_tuple):
    return {
        'id': backmanager_tuple[0],
        'name': backmanager_tuple[1],
        'is_super': True if backmanager_tuple[2] == 1 else False
    }


class BackendHelper:
    @staticmethod
    @format_by_formater(backmanager_formatter)
    def get_by_id(manager_id):
        cursor = execute_query('select id, username, is_super from backend_manager where id=?', [manager_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(backmanager_formatter)
    def get_by_name(manager_name):
        cursor = execute_query('select id, username, is_super from backend_manager where username=?', (manager_name,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(backmanager_formatter, True)
    def get_all():
        cursor = execute_query('select id, username, is_super from backend_manager')
        return cursor.fetchall()

    @staticmethod
    def create_manager(username, password):

        cursor = execute_modify(
            "insert into backend_manager (username, password) "
            "values (?, ?)",
            (username, password)
        )
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def modify_username(manager_id, manager_name):
        if BackendHelper.get_by_id(manager_id) is None:
            return False

        cursor = execute_modify(
            "update backend_manager set username=? where id=?",
            (manager_name, manager_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def modify_password(manager_id, password):
        cursor = execute_modify(
            "update backend_manager set password=? where id=?",
            (password, manager_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def check_password(manager_name, password):
        cursor = execute_query(
            'select count(*) from backend_manager where username=? and password=?',
            (manager_name, password)
        )
        return cursor.fetchone()[0] == 1

    @staticmethod
    def delete_by_id(manager_id):
        cursor = execute_modify(
            "delete from backend_manager where id=?",
            (manager_id,)
        )
        return cursor.rowcount == 1

