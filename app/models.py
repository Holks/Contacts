from time import time
from flask import current_app, url_for
import jwt
from app import db, login
from hashlib import md5

import json

import base64
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.baseModel import Base

TOKEN_EXPIRATION_TIME = 20000

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(Base, PaginatedAPIMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    _default_fields = [
        'username',
        'created',
        'id'
    ]

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=TOKEN_EXPIRATION_TIME):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    def get_token(self, expires_in=TOKEN_EXPIRATION_TIME):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def add_user(self, user):
        self.username = user['username']
        self.set_password(user['password'])
        db.session.add(self)
        db.session.commit()
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Contact(Base, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    actual_name = db.Column(db.String(200), index=True)
    code_name = db.Column(db.String(200), index=True, unique=True)
    phone_no = db.Column(db.String(200), index=True)

    _default_fields = [
        'id',
        'actual_name',
        'code_name',
        'phone_no'        
    ]

    def add_contact(self, user):
        self.actual_name = user['actual_name']
        self.code_name = user['code_name']
        self.phone_no = user['phone_no']
        db.session.add(self)
        db.session.commit()
    
    def delete_contact(self):
        db.session.delete(self)
        db.session.commit()

