# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.document import DocumentHelper
from server.util import require_auth

document_fields = {
    'id': fields.Integer,
    'type': fields.Integer,
    'description': fields.String,
    'content': fields.String,
    'course_id': fields.String,
    'coursename': fields.String
}


class Document(Resource):
    @require_auth([3])
    @marshal_with(document_fields)
    def get(self, document_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', required=False)
        args = parser.parse_args()

        result = None
        if document_id is not None:
            result = DocumentHelper.get_by_id(document_id)
        else:
            result = DocumentHelper.get_all()
            if args['course_id'] is not None:
                result = DocumentHelper.filter_by_course(result, args['course_id'])
        if result is None:
            abort(404)
        return result

    @require_auth([3])
    @marshal_with(document_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        args = parser.parse_args()

        result = DocumentHelper.create_document(args['name'])
        if result:
            return DocumentHelper.get_by_id(result)
        else:
            abort(400)

    @require_auth([3])
    @marshal_with(document_fields)
    def put(self, document_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False, help='name is required')
        args = parser.parse_args()

        print args
        success = True
        if args['name'] is not None:
            if not DocumentHelper.modify_name(document_id, args['name']):
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

    def options(self, manager_id=None):
        return ''

