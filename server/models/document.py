# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater


def document_formatter(document_tuple):
    return {
        'id': document_tuple[0],
        'type': document_tuple[1],
        'description': document_tuple[2],
        'content': document_tuple[3],
        'course_id': document_tuple[4],
        'coursename': document_tuple[5] if document_tuple[5] else '无所属课程'
    }


class DocumentHelper:
    @staticmethod
    @format_by_formater(document_formatter)
    def get_by_id(document_id):
        cursor = execute_query(
            'select document.id, type, description, content, course_id, course_name'
            ' from document, course where id=? and document.course_id=course.id'
            , [document_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(document_formatter, True)
    def get_all():
        cursor = execute_query(
            'select document.id, type, description, content, course_id, course.name'
            ' from document, course where document.course_id=course.id')
        return cursor.fetchall()

    @staticmethod
    @format_by_formater(document_formatter, True)
    def get_by_school(school_id):
        cursor = execute_query(
            'select document.id, type, description, content, course_id, course.name '
            'from document, course where document.course_id=course.id and document.id in (select doc_id from '
            'school_doc where school_id=?)',
                               [school_id])
        return cursor.fetchall()

    @staticmethod
    def filter_by_course(doc_list, course_id):
        return filter(
            lambda doc: (doc['course_id'] is not None) and (int(doc['course_id']) == int(course_id)),
            doc_list)

    @staticmethod
    def create_document(name):

        cursor = execute_modify(
            "insert into document (name) "
            "values (?)",
            (name,)
        )
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def delete_by_id(document_id):
        cursor = execute_modify(
            "delete from document where id=?",
            (document_id,)
        )
        return cursor.rowcount == 1

