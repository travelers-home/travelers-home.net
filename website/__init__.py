from flask import Flask, render_template_string, request
from flask_flatpages import FlatPages
from flask_flatpages.utils import pygmented_markdown
from flask.ext.images import Images

def jinja_renderer(text):
  prerendered_body = render_template_string(text)
  return pygmented_markdown(prerendered_body)

app = Flask(__name__)

# Default Values for config
app.config['SECTION_MAX_LINKS'] = 10
app.config['FLATPAGES_HTML_RENDERE'] = jinja_renderer
app.config.from_object('config')
flatpages = FlatPages(app)
images = Images(app)

from website.views import general
from website.views import pages

app.register_blueprint(general.mod)
app.register_blueprint(pages.mod)

@app.context_processor
def context_data():
  def is_active(endpoint=None, section=None, noclass=False):
    rtn = ""
    if noclass:
      rtn = 'active'
    else:
      rtn = 'class=active'
    if endpoint and section:
      if 'section' in request.view_args:
        if request.url_rule.endpoint == endpoint and request.view_args['section'] == section:
          return rtn
    elif endpoint:
      return rtn if request.url_rule.endpoint == endpoint else ''
    elif section:
      if 'section' in request.view_args:
        return rtn if request.view_args['section'] == section else ''
      elif 'path' in request.view_args:
        return rtn if request.view_args['path'].split('/')[0] == section else ''
    return ''
  return dict(is_active=is_active,
              debug=app.debug,
              sections=pages.get_sections(flatpages))

