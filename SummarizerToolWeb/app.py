from flask import Flask, session
from controllers import main_controller, history_controller
from markupsafe import escape
import os
from SummarizerToolWeb.db import db
import uuid
# from models import SummaryModel
from models.SummaryModel import Summary

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Tralalelo tralala vs Bombardilo krokodilo'

    
    @app.before_request
    def ensure_user_id():
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_controller.bp)
    app.register_blueprint(history_controller.bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

