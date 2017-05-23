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

        max_doc_id = 0
        tree = []
        visible_list = []
        for course in CourseHelper.get_all():
            docs = DocumentHelper.filter_by_course(DocumentHelper.get_by_school(school_id), course['id'])
            tree.append({
                'label': "{}({}/{})".format(course['name'], len(docs), course['doc_number']),
                'children': [{'node_id': doc['id'], 'label': doc['description']} for doc in docs]
            })
            for doc in docs:
                visible_list.append(doc['id'])
                max_doc_id = int(doc['id']) if max_doc_id < int(doc['id']) else max_doc_id
        # add doc that belongs to no course
        no_course_total = len(DocumentHelper.filter_by_course(DocumentHelper.get_all(), None))
        no_course_docs = DocumentHelper.filter_by_course(DocumentHelper.get_by_school(school_id), None)
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
    def get_modify_tree(school_id):
        from .course import CourseHelper
        from .document import DocumentHelper

        # 文档节点的node_id即为文档的id，课程节点的node_id为比最大的文档id更大的其他数字
        max_doc_id = 0
        result = []
        for course in CourseHelper.get_all():
            docs = DocumentHelper.filter_by_course(DocumentHelper.get_all(), course['id'])
            result.append({
                'label': "{}".format(course['name']),
                'children': [{'node_id': doc['id'], 'label': doc['description']} for doc in docs]
            })
            # get max doc id
            for doc in docs:
                max_doc_id = int(doc['id']) if max_doc_id < int(doc['id']) else max_doc_id

        # add doc that belongs to no course
        no_course_docs = DocumentHelper.filter_by_course(DocumentHelper.get_all(), None)
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
    def modify_visible_docs(school_id, doclist):
        from .document import DocumentHelper
        origin_visible_set = set(map(lambda doc: str(doc['id']), DocumentHelper.get_by_school(school_id)))
        dest_visible_set = set(map(lambda doc: str(doc), doclist))
        removed_set = origin_visible_set - set(dest_visible_set)
        print removed_set, school_id, doclist
        for doc_id in removed_set:
            DocumentHelper.remove_visible_from_schooluser(school_id, doc_id)

        DocumentHelper.remove_visible_from_school(school_id)
        result = True
        for doc_id in doclist:
            if not DocumentHelper.is_visible_to_school(school_id, doc_id):
                result = DocumentHelper.add_visible_school(school_id, doc_id)

        return result

    @staticmethod
    def create_school(name):

        cursor = execute_modify(
            "insert into school (name) "
            "values (?)",
            (name,)
        )
        # row count为1表示插入成功
        print cursor.rowcount
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
            (school_id,),
            True
        )
        return cursor.rowcount == 1

