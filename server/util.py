# -*- coding: utf-8 -*-
from flask import Blueprint, request, g, url_for
from flask_restful import abort, reqparse
from functools import wraps
import json
import jwt
from server import app


def generate_token(obj):
    return jwt.encode(obj, app.config['JWT_SECRET'], algorithm='HS256')


def require_auth(logtype_list, nowrap=False):
    def check_token(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('token', '')
            try:
                obj = jwt.decode(token, app.config['JWT_SECRET'], algorithm='HS256')
                print obj['logtype']
                if int(obj['logtype']) not in logtype_list:
                    return {'msg': 'no authority', 'code': 401}
            except jwt.InvalidTokenError:
                return {'msg': 'invalid token', 'code': 401}

            if nowrap:
                return f(*args, **kwargs)
            else:
                return {'code': 200, 'data': f(*args, **kwargs)}
        return decorated_function
    return check_token


def format_by_formater(formater, multi=False):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            try:
                if multi:
                    return map(lambda x: formater(x), result)
                else:
                    return formater(result)
            except TypeError:
                return None
        return decorated_function
    return real_decorator


def execute_query(sql, args=tuple()):
    # connect to mysql
    import sqlite3
    db_conn = sqlite3.connect(app.config['SQLITE_DIR'])

    cursor = db_conn.cursor()
    cursor.execute(sql, args)
    return cursor


def execute_modify(sql, args=tuple(), foreign=False):
    # connect to mysql
    import sqlite3
    db_conn = sqlite3.connect(app.config['SQLITE_DIR'])

    cursor = db_conn.cursor()
    if foreign:
        cursor.execute("PRAGMA foreign_keys = true;")
    cursor.execute(sql, args)
    db_conn.commit()
    return cursor
