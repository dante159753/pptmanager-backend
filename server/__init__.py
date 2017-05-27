# -*- coding: utf-8 -*-
from flask import Flask, make_response
from flask_restful import Api
import json

app = Flask(__name__)
api = Api(app)


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend({
        "Access-Control-Allow-Origin": '*',
        "Access-Control-Allow-Headers": 'token, Content-Type, Accept',
        'Access-Control-Expose-Headers': 'token',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
        })
    return resp

# set jwt secret
app.config['JWT_SECRET'] = 'my_secret'
# set upload folder
app.config['UPLOAD_FOLDER'] = '/root/pptmanager/pptmanager-backend/data'
# set db path
app.config['SQLITE_DIR'] = '/root/pptmanager/pptmanager-backend/sqlite.db'


from resources.login import Login
api.add_resource(Login, '/login')

from resources.backend_manager import BackendManager
api.add_resource(BackendManager, '/backend_manager', '/backend_manager/<int:manager_id>')

from resources.school import School
api.add_resource(School, '/school', '/school/<int:school_id>')

from resources.document import Document
api.add_resource(Document, '/document', '/document/<int:document_id>')

from resources.docfile import DocumentFile
api.add_resource(DocumentFile, '/docfile', '/docfile/<int:document_id>')

from resources.course import Course
api.add_resource(Course, '/course', '/course/<int:course_id>')

from resources.school_manager import SchoolManager
api.add_resource(SchoolManager, '/school_manager', '/school_manager/<int:manager_id>')

from resources.school_user import SchoolUser
api.add_resource(SchoolUser, '/school_user', '/school_user/<int:user_id>')
