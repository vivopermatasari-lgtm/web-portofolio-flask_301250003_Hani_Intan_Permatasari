from flask import Flask
from config import Config
from models import db
from datetime import datetime

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register blueprints
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    # Context processor for current year
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow}

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)