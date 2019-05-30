from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.registry import bp
from app.models import Contact, User
import json
from flask_login import login_required

@bp.route('/contacts', methods=['GET'])
@login_required
def get_contacts():
    # Get all contacts sort by db id
    data = Contact.query.order_by(Contact.id).all()
    return render_template('list_view.html', title='', \
        data=data, header=Contact._default_fields)

@bp.route('/contact/<int:id>', methods=['GET'])
@login_required
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    return render_template('contact_view.html', contact=contact)

@bp.route('/contact/<int:id>', methods=['PUT','DELETE'])
@login_required
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'PUT':   
        print("put")     
        data = request.get_json() or {}
        if 'code_name' in data and data['code_name'] != contact.code_name and \
                Contact.query.filter_by(code_name=data['code_name']).first():
            flash('could not edit')
            return url_for('main.index')
        contact.from_dict(**data)
        db.session.commit()
        return url_for('main.index')

    if request.method == 'DELETE':
        print("delete")
        contact.delete_contact()
        return url_for('main.index')

@bp.route('/contact', methods=['POST'])
@login_required
def contact():
    # get json object
    data = request.get_json()
    if data:
        # serverside checks for data integrity
        if 'code_name' not in data or 'phone_no' not in data or 'actual_name' not in data:
            flash('must include code_name, actual_name and phone_no fields')
            return redirect(url_for('main.index'))

        if Contact.query.filter_by(code_name=data['code_name']).first():
            flash('please use a different code_name')
            return redirect(url_for('main.index'))

        contact = Contact()
        # add Contact to database
        contact.add_contact(data)
    # always return listview template
    return redirect(url_for('main.index'))

