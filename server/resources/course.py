# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from server.models.course import CourseHelper
from server.util import check_token

course_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


class Course(Resource):
    @marshal_with(course_fields)
    @check_token
    def get(self, course_id=None):
        result = None
        if course_id is not None:
            result = CourseHelper.get_by_id(course_id)
        else:
            result = CourseHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(course_fields)
    @check_token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        args = parser.parse_args()

        result = CourseHelper.create_course(args['name'])
        if result:
            return CourseHelper.get_by_id(result)
        else:
            abort(400)

    @check_token
    def delete(self, course_id):
        if CourseHelper.delete_by_id(course_id):
            return ''
        else:
            abort(400)

