# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.school import SchoolHelper
from server.util import require_auth
import json

visible_doc_fields = {
    'node_id': fields.Integer,
    'label': fields.String
}

visible_course_fields = {
    'node_id': fields.Integer,
    'label': fields.String,
    'children': fields.List(fields.Nested(visible_doc_fields))
}

school_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'visible_doc_tree': fields.List(fields.Nested(visible_course_fields)),
    'checked_nodes': fields.List(fields.Integer),
    'modify_doc_tree': fields.List(fields.Nested(visible_course_fields)),
    'max_doc_id': fields.Integer  # 因为选中的树节点的编号包含course的节点编号，为了过滤这些，小于等于这个值的一定是doc编号
}


class School(Resource):
    @require_auth([1, 2, 3])
    @marshal_with(school_fields)
    def get(self, school_id=None):
        result = None
        if school_id is not None:
            result = SchoolHelper.get_by_id(school_id)
            if result:
                result['visible_doc_tree'], result['checked_nodes'] = SchoolHelper.get_visible_tree(school_id)
                result['modify_doc_tree'], result['max_doc_id'] = SchoolHelper.get_modify_tree(school_id)
        else:
            result = SchoolHelper.get_all()
        if result is None:
            abort(404)
        return result

    @require_auth([3])
    @marshal_with(school_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        args = parser.parse_args()

        result = SchoolHelper.create_school(args['name'])
        if result:
            return SchoolHelper.get_by_id(result)
        else:
            abort(400)

    @require_auth([3])
    @marshal_with(school_fields)
    def put(self, school_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)
        parser.add_argument('checked_nodes', required=False)
        args = parser.parse_args()

        print args
        success = True
        if args['name'] is not None:
            if not SchoolHelper.modify_name(school_id, args['name']):
                success = False
        if args['checked_nodes'] is not None:
            if not SchoolHelper.modify_visible_docs(school_id, json.loads(args['checked_nodes'])):
                success = False

        if not success:
            abort(400)

        return SchoolHelper.get_by_id(school_id)

    @require_auth([3])
    def delete(self, school_id):
        if SchoolHelper.delete_by_id(school_id):
            return ''
        else:
            abort(400)

    def options(self, school_id=None):
        return ''

