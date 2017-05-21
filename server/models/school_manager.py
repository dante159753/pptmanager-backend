# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater
from .school import SchoolHelper


def schoolmanager_formatter(schoolmanager_tuple):
    return {
        'id': schoolmanager_tuple[0],
        'username': schoolmanager_tuple[1],
        'school_id': SchoolHelper.get_by_id(schoolmanager_tuple[2])
    }


class SchoolManagerHelper:
    @staticmethod
    @format_by_formater(schoolmanager_formatter)
    def get_by_id(manager_id):
        cursor = execute_query('select id, username, school_id from school_manager where id=?', [manager_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(schoolmanager_formatter)
    def get_by_name(manager_name):
        cursor = execute_query('select id, username, school_id from school_manager where username=?', (manager_name,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(schoolmanager_formatter, True)
    def get_all():
        cursor = execute_query('select id, username, school_id from school_manager')
        return cursor.fetchall()

    @staticmethod
    def create_manager(username, password, school_id):

        cursor = execute_modify(
            "insert into school_manager (username, password, school_id) "
            "values (?, ?, ?)",
            (username, password, school_id)
        )
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def modify_username(manager_id, manager_name):
        if SchoolManagerHelper.get_by_id(manager_id) is None:
            return False

        cursor = execute_modify(
            "update school_manager set username=? where id=?",
            (manager_name, manager_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def modify_password(manager_id, password):
        cursor = execute_modify(
            "update school_manager set password=? where id=?",
            (password, manager_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def modify_school(manager_id, school_id):
        cursor = execute_modify(
            "update school_manager set school_id=? where id=?",
            (school_id, manager_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def check_password(manager_name, password):
        cursor = execute_query(
            'select count(*) from school_manager where username=? and password=?',
            (manager_name, password)
        )
        return cursor.fetchone()[0] == 1

    @staticmethod
    def delete_by_id(manager_id):
        cursor = execute_modify(
            "delete from school_manager where id=?",
            (manager_id,)
        )
        return cursor.rowcount == 1

