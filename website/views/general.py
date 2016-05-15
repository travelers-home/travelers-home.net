from website import app
from flask import Blueprint, render_template, session, redirect, url_for, \
        request, abort

mod = Blueprint('general', __name__)

@mod.route('/contact')
def contact(name=None):
  return render_template('general/contact.html', name=name)
