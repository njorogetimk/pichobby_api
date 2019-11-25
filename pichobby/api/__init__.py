from flask import Blueprint

picapi = Blueprint('picapi', __name__)

from pichobby.api import views
