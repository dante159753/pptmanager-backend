# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater
from .school import SchoolHelper


def schooluser_formatter(schooluser_tuple):
    return {
        'id': schooluser_tuple[0],
        'username': schooluser_tuple[1],
        'school_id': SchoolHelper.get_by_id(schooluser_tuple[2]),
        'logtype': 1
    }


class SchoolUserHelper:
    @staticmethod
    @format_by_formater(schooluser_formatter)
    def get_by_id(user_id):
        cursor = execute_query('select id, username, school_id from school_user where id=?', [user_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(schooluser_formatter)
    def get_by_name(username):
        cursor = execute_query('select id, username, school_id from school_user where username=?', (username,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(schooluser_formatter, True)
    def get_all():
        cursor = execute_query('select id, username, school_id from school_user')
        return cursor.fetchall()

    @staticmethod
    def create_user(username, password, school_id):

        cursor = execute_modify(
            "insert into school_user (username, password, school_id) "
            "values (?, ?, ?)",
            (username, password, school_id)
        )
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def modify_username(user_id, user_name):
        if SchoolUserHelper.get_by_id(user_id) is None:
            return False

        cursor = execute_modify(
            "update school_user set username=? where id=?",
            (user_name, user_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def modify_password(user_id, password):
        cursor = execute_modify(
            "update school_user set password=? where id=?",
            (password, user_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def modify_school(user_id, school_id):
        cursor = execute_modify(
            "update school_user set school_id=? where id=?",
            (school_id, user_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def check_password(user_name, password):
        cursor = execute_query(
            'select count(*) from school_user where username=? and password=?',
            (user_name, password)
        )
        return cursor.fetchone()[0] == 1

    @staticmethod
    def delete_by_id(user_id):
        cursor = execute_modify(
            "delete from school_user where id=?",
            (user_id,)
        )
        return cursor.rowcount == 1

