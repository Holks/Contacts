from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """
    Get single user with <id>
    """
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """
    Get all users added to the database who have acces to DB
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users', methods=['POST'])
@token_auth.login_required
def create_user():
    """ 
    Add new user to db
    """
    data = request.get_json() or {}
    print(data)
    # some data checks
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    user = User()
    # add user to database
    user.add_user(data)
    # check that the transaction was successful
    res = User.query.filter_by(username=data['username']).one_or_none()
    # return added user as query response
    if res:
        response = jsonify(res.to_dict())
        response.status_code = 201
    # else return error
    else:
        response.status_code = 403
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    user.from_dict(**data)
    db.session.commit()
    return jsonify(user.to_dict())
