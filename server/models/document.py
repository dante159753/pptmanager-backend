# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater


def document_formatter(document_tuple):
    return {
        'id': document_tuple[0],
        'type': document_tuple[1],
        'description': document_tuple[2],
        'content': document_tuple[3],
        'course_id': document_tuple[4],
        'coursename': document_tuple[5] if document_tuple[5] else u'无所属课程'
    }


class DocumentHelper:
    @staticmethod
    @format_by_formater(document_formatter)
    def get_by_id(document_id):
        cursor = execute_query(
            'select document.id, type, description, content, course_id, course.name'
            ' from document left join course on document.course_id=course.id where document.id=? '
            , [document_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(document_formatter, True)
    def get_all():
        cursor = execute_query(
            'select document.id, type, description, content, course_id, course.name'
            ' from document left join course on document.course_id=course.id')
        return cursor.fetchall()

    @staticmethod
    @format_by_formater(document_formatter, True)
    def get_by_school(school_id):
        cursor = execute_query(
            'select document.id, type, description, content, course_id, course.name '
            'from document left join course on document.course_id=course.id where document.id in (select doc_id from '
            'school_doc where school_id=?)',
                               [school_id])
        return cursor.fetchall()

    @staticmethod
    @format_by_formater(document_formatter, True)
    def get_by_user(user_id):
        cursor = execute_query(
            'select document.id, type, description, content, course_id, course.name '
            'from document left join course on document.course_id=course.id where document.id in (select doc_id from '
            'user_doc where user_id=?)',
            [user_id])
        return cursor.fetchall()

    @staticmethod
    def filter_by_course(doc_list, course_id):
        return filter(
            lambda doc: (str(doc['course_id']) == str(course_id)),
            doc_list)

    @staticmethod
    def is_visible_to_school(school_id, doc_id):
        cursor = execute_query('select count(1) from school_doc where school_id=? and doc_id=?', [school_id, doc_id])
        return cursor.fetchone()[0] == 1

    @staticmethod
    def add_visible_school(school_id, doc_id):
        cursor = execute_modify('insert into school_doc(school_id, doc_id) values(?, ?)', [school_id, doc_id])
        return cursor.rowcount == 1

    @staticmethod
    def add_visible_user(user_id, doc_id):
        cursor = execute_modify('insert into user_doc(user_id, doc_id) values(?, ?)', [user_id, doc_id], True)
        return cursor.rowcount == 1

    @staticmethod
    def remove_visible_from_school(school_id):
        cursor = execute_modify('delete from school_doc where school_id=?', [school_id])
        return True

    @staticmethod
    def remove_visible_from_schooluser(school_id, doc_id):
        cursor = execute_modify('delete from user_doc where doc_id=? ' 
                                'and user_id in (select id from school_user where school_id=?)',
                                [doc_id, school_id, ])
        return True

    @staticmethod
    def remove_visible_from_user(user_id):
        cursor = execute_modify('delete from user_doc where user_id=?', [user_id])
        return True

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
    def modify_name(docid, name):
        cursor = execute_modify(
            "update document set description=? where id=?",
            (name, docid,)
        )
        # row count为1表示插入成功
        return True

    @staticmethod
    def modify_course(docid, course_id):
        cursor = execute_modify(
            "update document set course_id=? where id=?",
            (course_id, docid,)
        )
        # row count为1表示插入成功
        return True

    @staticmethod
    def delete_by_id(document_id):
        cursor = execute_modify(
            "delete from document where id=?",
            (document_id,),
            True
        )
        return cursor.rowcount == 1

