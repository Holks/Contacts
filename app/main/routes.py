from datetime import datetime
from flask import render_template, redirect, url_for
from app import db
from app.main import bp
from flask_login import login_required

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('registry.get_contacts'))

