# -*- coding: utf-8 -*-
from flask import Flask, make_response
from flask_restful import Api
import json

app = Flask(__name__)
api = Api(app)

# set jwt secret
app.config['JWT_SECRET'] = 'my_secret'
# set upload folder
app.config['UPLOAD_FOLDER'] = '/root/petclinic/pet_clinic_backend/data'


from resources.backend_manager import BackendManager
api.add_resource(BackendManager, '/backend_manager', '/backend_manager/<int:manager_id>')

from resources.school import School
api.add_resource(School, '/school', '/school/<int:school_id>')

from resources.document import Document
api.add_resource(Document, '/document', '/document/<int:document_id>')

from resources.course import Course
api.add_resource(Course, '/course', '/course/<int:course_id>')

from resources.school_manager import SchoolManager
api.add_resource(SchoolManager, '/school_manager', '/school_manager/<int:manager_id>')

from resources.school_user import SchoolUser
api.add_resource(SchoolUser, '/school_user', '/school_user/<int:user_id>')
