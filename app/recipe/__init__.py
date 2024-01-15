from flask import Blueprint

bp = Blueprint('recipe', __name__)

from app.recipe import routes