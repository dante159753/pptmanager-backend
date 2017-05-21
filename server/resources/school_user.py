# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.school_user import SchoolUserHelper
from server.resources.school import school_fields
from server.util import check_token

school_user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'school_id': fields.Nested(school_fields)
}


class SchoolUser(Resource):
    @marshal_with(school_user_fields)
    @check_token
    def get(self, user_id=None):
        result = None
        if user_id is not None:
            result = SchoolUserHelper.get_by_id(user_id)
        else:
            result = SchoolUserHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(school_user_fields)
    @check_token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        args = parser.parse_args()

        if SchoolUserHelper.create_user(args['username'], args['password']):
            return SchoolUserHelper.get_by_name(args['username'])
        else:
            abort(400)

    @marshal_with(school_user_fields)
    @check_token
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help='username is required')
        parser.add_argument('password', required=False, help='password is required')
        args = parser.parse_args()

        print args
        success = True
        if args['username'] is not None:
            if not SchoolUserHelper.modify_username(user_id, args['username']):
                success = False
        if args['password'] is not None:
            if not SchoolUserHelper.modify_password(user_id, args['password']):
                success = False

        if not success:
            abort(400)

        return SchoolUserHelper.get_by_id(user_id)

    @check_token
    def delete(self, user_id):
        if SchoolUserHelper.delete_by_id(user_id):
            return ''
        else:
            abort(400)

