# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import flask, os
from server.models.document import DocumentHelper
from server.util import require_auth
from server import app


class DocumentFile(Resource):
    def get(self, document_id=None):
        doc = DocumentHelper.get_by_id(document_id)

        response = flask.make_response(open(os.path.join(app.config['UPLOAD_FOLDER'], doc['path']), 'rb').read())
        response.headers['content-type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = "inline; filename=" + doc['description']

        return response

    def options(self, document_id=None):
        return ''

