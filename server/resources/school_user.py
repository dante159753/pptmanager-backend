# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.school_user import SchoolUserHelper
from server.resources.school import school_fields, visible_course_fields
from server.util import require_auth
import json

school_user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'doc_number': fields.Integer,
    'school': fields.Nested(school_fields),
    'visible_doc_tree': fields.List(fields.Nested(visible_course_fields)),
    'checked_nodes': fields.List(fields.Integer),
    'modify_doc_tree': fields.List(fields.Nested(visible_course_fields)),
    'max_doc_id': fields.Integer  # 因为选中的树节点的编号包含course的节点编号，为了过滤这些，小于等于这个值的一定是doc编号
}


class SchoolUser(Resource):
    @require_auth([1, 2, 3])
    @marshal_with(school_user_fields)
    def get(self, user_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('school_id', required=False)
        args = parser.parse_args()

        user = SchoolUserHelper.get_by_id(user_id)
        result = None
        if user is not None:
            result = SchoolUserHelper.get_by_id(user_id)
            if result:
                result['visible_doc_tree'], result['checked_nodes'] = SchoolUserHelper.get_visible_tree(user)
                result['modify_doc_tree'], result['max_doc_id'] = SchoolUserHelper.get_modify_tree(user)
        else:
            result = SchoolUserHelper.get_all()
            if args['school_id'] is not None:
                result = SchoolUserHelper.filter_by_school(result, args['school_id'])
        if result is None:
            abort(404)
        return result

    @require_auth([2, 3])
    @marshal_with(school_user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        parser.add_argument('school_id', required=True, help='school_id is required')
        args = parser.parse_args()

        if SchoolUserHelper.create_user(args['username'], args['password'], args['school_id']):
            return SchoolUserHelper.get_by_name(args['username'])
        else:
            abort(400)

    @require_auth([1, 2, 3])
    @marshal_with(school_user_fields)
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help='username is required')
        parser.add_argument('password', required=False, help='password is required')
        parser.add_argument('school_id', required=False, help='school_id is required')
        parser.add_argument('checked_nodes', required=False)
        args = parser.parse_args()

        print args
        success = True
        if args['username'] is not None:
            if not SchoolUserHelper.modify_username(user_id, args['username']):
                success = False
        if args['password'] is not None:
            if not SchoolUserHelper.modify_password(user_id, args['password']):
                success = False
        if args['school_id'] is not None:
            if not SchoolUserHelper.modify_school(user_id, args['school_id']):
                success = False
        if args['checked_nodes'] is not None:
            if not SchoolUserHelper.modify_visible_docs(user_id, json.loads(args['checked_nodes'])):
                success = False

        if not success:
            abort(400)

        return SchoolUserHelper.get_by_id(user_id)

    @require_auth([2, 3])
    def delete(self, user_id):
        if SchoolUserHelper.delete_by_id(user_id):
            return ''
        else:
            abort(400)

    def options(self, user_id=None):
        return ''

