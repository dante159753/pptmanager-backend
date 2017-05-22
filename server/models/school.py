# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater


def school_formatter(school_tuple):
    return {
        'id': school_tuple[0],
        'name': school_tuple[1]
    }


class SchoolHelper:
    @staticmethod
    @format_by_formater(school_formatter)
    def get_by_id(school_id):
        cursor = execute_query('select id, name from school where id=?', [school_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(school_formatter)
    def get_by_name(school_name):
        cursor = execute_query('select id, name from school where name=?', (school_name,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(school_formatter, True)
    def get_all():
        cursor = execute_query('select id, name from school')
        return cursor.fetchall()

    @staticmethod
    def get_visible_tree(school_id):
        from .course import CourseHelper
        from .document import DocumentHelper

        result = []
        for course in CourseHelper.get_all():
            print DocumentHelper.get_by_school(school_id)
            docs = DocumentHelper.filter_by_course(DocumentHelper.get_by_school(school_id), course['id'])
            result.append({
                'label': "{}({}/{})".format(course['name'], len(docs), course['doc_number']),
                'children': [{'label': doc['description']} for doc in docs]
            })

        return result

    @staticmethod
    def create_school(name):

        cursor = execute_modify(
            "insert into school (name) "
            "values (?)",
            (name,)
        )
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def modify_name(school_id, school_name):
        if SchoolHelper.get_by_id(school_id) is None:
            return False

        cursor = execute_modify(
            "update school set name=? where id=?",
            (school_name, school_id)
        )
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_id(school_id):
        cursor = execute_modify(
            "delete from school where id=?",
            (school_id,)
        )
        return cursor.rowcount == 1

