# -*- coding: utf-8 -*-

from server.util import execute_query, execute_modify, format_by_formater
from .school import SchoolHelper


def schooluser_formatter(schooluser_tuple):
    return {
        'id': schooluser_tuple[0],
        'username': schooluser_tuple[1],
        'school': SchoolHelper.get_by_id(schooluser_tuple[2]),
        'logtype': 1,
        'doc_number': schooluser_tuple[3],
    }


class SchoolUserHelper:
    @staticmethod
    @format_by_formater(schooluser_formatter)
    def get_by_id(user_id):
        cursor = execute_query(
            'select id, username, school_id, (select count(1) from user_doc where user_id=school_user.id) as doc_number'
            ' from school_user where id=?', [user_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(schooluser_formatter)
    def get_by_name(username):
        cursor = execute_query(
            'select id, username, school_id, (select count(1) from user_doc where user_id=school_user.id) as doc_number' 
            ' from school_user where username=?', (username,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(schooluser_formatter, True)
    def get_all():
        cursor = execute_query(
            'select id, username, school_id, (select count(1) from user_doc where user_id=school_user.id) as doc_number'
            ' from school_user')
        return cursor.fetchall()

    @staticmethod
    def filter_by_school(users, school_id):
        return filter(lambda user: (str(user['school']['id']) == str(school_id)), users)

    @staticmethod
    def get_visible_tree(user):
        from .course import CourseHelper
        from .document import DocumentHelper

        max_doc_id = 0
        tree = []
        visible_list = []
        for course in CourseHelper.get_all():
            docs = DocumentHelper.filter_by_course(DocumentHelper.get_by_user(user['id']), course['id'])
            # 总可见文档数是用户所属学校的总可见文档数
            total_visible = len(DocumentHelper.filter_by_course(
                DocumentHelper.get_by_school(user['school']['id']),
                course['id']
            ))
            tree.append({
                'label': "{}({}/{})".format(course['name'], len(docs), total_visible),
                'children': [{'node_id': doc['id'], 'label': doc['description']} for doc in docs]
            })
            for doc in docs:
                visible_list.append(doc['id'])
                max_doc_id = int(doc['id']) if max_doc_id < int(doc['id']) else max_doc_id
        # add doc that belongs to no course
        no_course_total = len(DocumentHelper.filter_by_course(DocumentHelper.get_by_school(user['school']['id']), None))
        no_course_docs = DocumentHelper.filter_by_course(DocumentHelper.get_by_user(user['id']), None)
        tree.insert(0, {
            'label': u"无所属课程({}/{})".format(len(no_course_docs), no_course_total),
            'children': [{'node_id': doc['id'], 'label': doc['description']} for doc in no_course_docs]
        })
        for doc in no_course_docs:
            visible_list.append(doc['id'])
            max_doc_id = int(doc['id']) if max_doc_id < int(doc['id']) else max_doc_id
        # add node_id to courses
        node_id = max_doc_id + 1
        for course in tree:
            course['node_id'] = node_id
            node_id += 1

        return tree, visible_list

    @staticmethod
    def get_modify_tree(user):
        from .course import CourseHelper
        from .document import DocumentHelper

        # 文档节点的node_id即为文档的id，课程节点的node_id为比最大的文档id更大的其他数字
        max_doc_id = 0
        result = []
        for course in CourseHelper.get_all():
            docs = DocumentHelper.filter_by_course(DocumentHelper.get_by_school(user['school']['id']), course['id'])
            result.append({
                'label': "{}".format(course['name']),
                'children': [{'node_id': doc['id'], 'label': doc['description']} for doc in docs]
            })
            # get max doc id
            for doc in docs:
                max_doc_id = int(doc['id']) if max_doc_id < int(doc['id']) else max_doc_id

        # add doc that belongs to no course
        no_course_docs = DocumentHelper.filter_by_course(DocumentHelper.get_by_school(user['school']['id']), None)
        result.insert(0, {
            'label': u"无所属课程".format(len(no_course_docs)),
            'children': [{'node_id': doc['id'], 'label': doc['description']} for doc in no_course_docs]
        })
        for doc in no_course_docs:
            max_doc_id = int(doc['id']) if max_doc_id < int(doc['id']) else max_doc_id
        # add node id to courses
        node_id = max_doc_id + 1
        for course in result:
            course['node_id'] = node_id
            node_id += 1

        return result, max_doc_id

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
    def modify_visible_docs(user_id, doclist):
        from .document import DocumentHelper
        DocumentHelper.remove_visible_from_user(user_id)

        result = True
        print doclist
        for doc_id in doclist:
            result = DocumentHelper.add_visible_user(user_id, doc_id)

        return result

    @staticmethod
    def delete_by_id(user_id):
        cursor = execute_modify(
            "delete from school_user where id=?",
            (user_id,),
            True
        )
        return cursor.rowcount == 1

