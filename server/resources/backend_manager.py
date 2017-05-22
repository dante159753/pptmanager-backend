# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.backend_manager import BackendHelper
from server.util import require_auth

back_manager_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'is_super': fields.Boolean
}


class BackendManager(Resource):
    @require_auth([3])
    @marshal_with(back_manager_fields)
    def get(self, manager_id=None):
        result = None
        if manager_id is not None:
            result = BackendHelper.get_by_id(manager_id)
        else:
            result = BackendHelper.get_all()
        if result is None:
            abort(404)
        return result

    @require_auth([3])
    @marshal_with(back_manager_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        args = parser.parse_args()

        if BackendHelper.create_manager(args['username'], args['password']):
            return BackendHelper.get_by_name(args['username'])
        else:
            abort(400)

    @require_auth([3])
    @marshal_with(back_manager_fields)
    def put(self, manager_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help='username is required')
        parser.add_argument('password', required=False, help='password is required')
        args = parser.parse_args()

        print args
        success = True
        if args['username'] is not None:
            if not BackendHelper.modify_username(manager_id, args['username']):
                success = False
        if args['password'] is not None:
            if not BackendHelper.modify_password(manager_id, args['password']):
                success = False

        if not success:
            abort(400)

        return BackendHelper.get_by_id(manager_id)

    @require_auth([3])
    def delete(self, manager_id):
        if BackendHelper.delete_by_id(manager_id):
            return ''
        else:
            abort(400)

    def options(self, manager_id=None):
        return ''

