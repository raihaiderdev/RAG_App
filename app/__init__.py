from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Register pgvector type with SQLAlchemy BEFORE db.init_app
    # This ensures the Vector column type is known when models are mapped
    from pgvector.sqlalchemy import Vector  # noqa

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.ingest import ingest_bp
    from app.routes.query import query_bp

    app.register_blueprint(ingest_bp)
    app.register_blueprint(query_bp)

    # Root route — serves the UI
    @app.route("/")
    def index():
        return render_template("index.html")

    return app
