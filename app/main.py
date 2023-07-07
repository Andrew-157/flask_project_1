from flask import Blueprint, render_template, redirect, url_for, request, flash

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    flash('test message', 'info')
    return render_template('main/index.html')
