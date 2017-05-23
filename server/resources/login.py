# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, abort
from server.util import generate_token
from server.models.backend_manager import BackendHelper
from server.models.school_manager import SchoolManagerHelper
from server.models.school_user import SchoolUserHelper


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        # 1: 学校用户，2: 学校管理员，3: 后台管理员
        parser.add_argument('logtype', help='logtype is required', default=1)
        args = parser.parse_args()

        print args

        helper = SchoolUserHelper

        if str(args['logtype']) == '2':
            helper = SchoolManagerHelper

        if str(args['logtype']) == '3':
            helper = BackendHelper

        if helper.check_password(args['username'], args['password']):
            print helper.get_by_name(args['username'])
            return {'code': 200, 'data': generate_token(helper.get_by_name(args['username']))}
        else:
            return {'msg': 'invalid username or password', 'code': 401}

    def options(self):
        return ''
