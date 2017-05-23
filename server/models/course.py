# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater
from .document import DocumentHelper


def course_formatter(course_tuple):
    return {
        'id': course_tuple[0],
        'name': course_tuple[1],
        'doc_number': len(DocumentHelper.filter_by_course(DocumentHelper.get_all(), course_tuple[0]))
    }


class CourseHelper:
    @staticmethod
    @format_by_formater(course_formatter)
    def get_by_id(course_id):
        cursor = execute_query('select id, name from course where id=?', [course_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(course_formatter, True)
    def get_all():
        cursor = execute_query('select id, name from course')
        return cursor.fetchall()

    @staticmethod
    def create_course(name):

        cursor = execute_modify(
            "insert into course (name) "
            "values (?)",
            (name,)
        )
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def delete_by_id(course_id):
        for doc in DocumentHelper.filter_by_course(DocumentHelper.get_all(), course_id):
            DocumentHelper.modify_course(doc['id'], None)
        cursor = execute_modify(
            "delete from course where id=?",
            (course_id,),
            True
        )
        return cursor.rowcount == 1

