# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.document import DocumentHelper
from server.util import check_token

document_fields = {
    'id': fields.Integer,
    'type': fields.Integer,
    'description': fields.String,
    'content': fields.String,
    'course': fields.String
}


class Document(Resource):
    @marshal_with(document_fields)
    @check_token
    def get(self, document_id=None):
        result = None
        if document_id is not None:
            result = DocumentHelper.get_by_id(document_id)
        else:
            result = DocumentHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(document_fields)
    @check_token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        args = parser.parse_args()

        result = DocumentHelper.create_document(args['name'])
        if result:
            return DocumentHelper.get_by_id(result)
        else:
            abort(400)

    @marshal_with(document_fields)
    @check_token
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

    @check_token
    def delete(self, document_id):
        if DocumentHelper.delete_by_id(document_id):
            return ''
        else:
            abort(400)

