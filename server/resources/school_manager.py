# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.school_manager import SchoolManagerHelper
from server.resources.school import school_fields
from server.util import require_auth

school_manager_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'school': fields.Nested(school_fields)
}


class SchoolManager(Resource):
    @require_auth([2, 3])
    @marshal_with(school_manager_fields)
    def get(self, manager_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('school_id', required=False)
        parser.add_argument('username', required=False)
        args = parser.parse_args()

        result = None
        if manager_id is not None:
            result = SchoolManagerHelper.get_by_id(manager_id)
        elif args['username'] is not None:
            result = SchoolManagerHelper.get_by_name(args['username'])
        else:
            result = SchoolManagerHelper.get_all()
            if args['school_id'] is not None:
                result = SchoolManagerHelper.filter_by_school(result, args['school_id'])
        if result is None:
            abort(404)
        return result

    @require_auth([3])
    @marshal_with(school_manager_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        parser.add_argument('school_id', required=True, help='school_id is required')
        args = parser.parse_args()

        if SchoolManagerHelper.create_manager(args['username'], args['password'], args['school_id']):
            return SchoolManagerHelper.get_by_name(args['username'])
        else:
            abort(400)

    @require_auth([2, 3])
    @marshal_with(school_manager_fields)
    def put(self, manager_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help='username is required')
        parser.add_argument('password', required=False, help='password is required')
        parser.add_argument('school_id', required=False, help='school_id is required')
        args = parser.parse_args()

        print args
        success = True
        if args['username'] is not None:
            if not SchoolManagerHelper.modify_username(manager_id, args['username']):
                success = False
        if args['password'] is not None:
            if not SchoolManagerHelper.modify_password(manager_id, args['password']):
                success = False
        if args['school_id'] is not None:
            if not SchoolManagerHelper.modify_school(manager_id, args['school_id']):
                success = False

        if not success:
            abort(400)

        return SchoolManagerHelper.get_by_id(manager_id)

    @require_auth([3])
    def delete(self, manager_id):
        if SchoolManagerHelper.delete_by_id(manager_id):
            return ''
        else:
            abort(400)

    def options(self, manager_id=None):
        return ''

