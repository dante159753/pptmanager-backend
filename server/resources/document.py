# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.document import DocumentHelper
from server.util import require_auth
from server.models.school_manager import SchoolManagerHelper
from server.models.school_user import SchoolUserHelper
import werkzeug

document_fields = {
    'id': fields.Integer,
    'type': fields.Integer,
    'description': fields.String,
    'content': fields.String,
    'course_id': fields.String,
    'coursename': fields.String
}


class Document(Resource):
    @require_auth([1, 2, 3])
    @marshal_with(document_fields)
    def get(self, document_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', required=False)
        parser.add_argument('logtype', required=False)
        parser.add_argument('username', required=False)
        args = parser.parse_args()

        result = None
        if document_id is not None:
            result = DocumentHelper.get_by_id(document_id)
        else:
            result = DocumentHelper.get_all()
            if args['course_id'] is not None:
                result = DocumentHelper.filter_by_course(
                    result,
                    args['course_id'] if args['course_id'] != '0' else None
                )
            if args['logtype'] is not None and args['username'] is not None:
                if str(args['logtype']) == '2':  # school manager
                    print 'filter by school manager'
                    manager = SchoolManagerHelper.get_by_name(args['username'])
                    school_visible_set = map(lambda x: x['id'], DocumentHelper.get_by_school(manager['school']['id']))
                    result = filter(lambda x: x['id'] in school_visible_set, result)
                elif str(args['logtype']) == '3':  # backend manager
                    print 'filter by backend manager'
                    pass
                else:  # school user
                    print SchoolUserHelper.get_by_name(args['username'])
                    user_visible_set = map(
                        lambda x: x['id'],
                        DocumentHelper.get_by_user(
                            SchoolUserHelper.get_by_name(args['username'])['id']
                        )
                    )
                    result = filter(lambda x: x['id'] in user_visible_set, result)
        if result is None:
            abort(404)
        return result

    @require_auth([3])
    @marshal_with(document_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        result = DocumentHelper.create_document(args['file'])
        if result:
            return DocumentHelper.get_by_id(result)
        else:
            abort(400)

    @require_auth([3])
    @marshal_with(document_fields)
    def put(self, document_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)
        parser.add_argument('course_id', required=False)
        args = parser.parse_args()

        print args
        success = True
        if args['name'] is not None:
            if not DocumentHelper.modify_name(document_id, args['name']):
                success = False
        if args['course_id'] is not None:
            if not DocumentHelper.modify_course(document_id, args['course_id'] if args['course_id'] != '0' else None):
                success = False

        if not success:
            abort(400)

        return DocumentHelper.get_by_id(document_id)

    @require_auth([3])
    def delete(self, document_id):
        if DocumentHelper.delete_by_id(document_id):
            return ''
        else:
            abort(400)

    def options(self, document_id=None):
        return ''

