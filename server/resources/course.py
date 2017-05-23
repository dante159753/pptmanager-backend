# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.course import CourseHelper
from server.util import require_auth

course_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'doc_number': fields.Integer
}


class Course(Resource):
    @require_auth([1, 2, 3])
    @marshal_with(course_fields)
    def get(self, course_id=None):
        result = None
        if course_id is not None:
            result = CourseHelper.get_by_id(course_id)
        else:
            result = CourseHelper.get_all()
        if result is None:
            abort(404)
        return result

    @require_auth([3])
    @marshal_with(course_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        args = parser.parse_args()

        result = CourseHelper.create_course(args['name'])
        if result:
            return CourseHelper.get_by_id(result)
        else:
            abort(400)

    @require_auth([3])
    def delete(self, course_id):
        if CourseHelper.delete_by_id(course_id):
            return ''
        else:
            abort(400)

    def options(self, course_id=None):
        return ''
