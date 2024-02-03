from flask import Flask

from config import Config
from app.extensions import mysql, mail

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Extentions
    mysql.init_app(app)
    mail.init_app(app)

    # Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="/")

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.recipe import bp as recipe_bp
    app.register_blueprint(recipe_bp, url_prefix="/recipe")


    @app.route('/r')
    def test_page():
        return ['%s' % rule for rule in app.url_map.iter_rules()]

    return app
