from flask import jsonify, request, url_for
from app import db
from app.models import Contact
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, internal_server_error


@bp.route('/contacts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_contact(id):
    """
    Get single contact with <id>
    """
    return jsonify(Contact.query.get_or_404(id).to_dict())

@bp.route('/contacts', methods=['GET'])
@token_auth.login_required
def get_contacts():
    """
    Get all contacts added to the database who have acces to DB
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Contact.to_collection_dict(Contact.query, page, per_page, 
        'api.get_contacts')
    return jsonify(data)

@bp.route('/contacts', methods=['POST'])
@token_auth.login_required
def create_contact():
    """ 
    Add new contact to db
    """
    data = request.get_json() or {}
    # some data checks
    if 'code_name' not in data or 'phone_no' not in data or 'actual_name' not in data:
        return bad_request('must include code_name, actual_name and phone_no fields')
    if Contact.query.filter_by(code_name=data['code_name']).first():
        return bad_request('please use a different code_name')
    contact = Contact()
    # add Contact to database
    contact.add_contact(data)
    # check that the transaction was successful
    res = Contact.query.filter_by(code_name=data['code_name']).one_or_none()
    # return added contact as query response
    if res:
        response = jsonify(res.to_dict())
        response.status_code = 201
    # else return error
    else:
        response.status_code = 403
    response.headers['Location'] = url_for('api.create_contact', id=contact.id)
    return response

@bp.route('/contacts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json() or {}
    if 'code_name' in data and data['code_name'] != contact.code_name and \
            Contact.query.filter_by(code_name=data['code_name']).first():
        return bad_request('please use a different code_name')
    contact.from_dict(**data)
    db.session.commit()
    return jsonify(contact.to_dict())

@bp.route('/contacts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    contact.delete_contact()
    contact = Contact.query.get_or_404(id)
    if contact:
        internal_server_error('unknown internal server error - could not delete contact')
    else:
        response = {}
        response.headers['Location'] = url_for('api.delete_contact', id=id)
        response.status_code = 200
        return response