"""
Flask App Factory for Stakeholder Engagement Platform
Initializes Flask application with extensions and blueprints
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='development'):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration environment (development, production, testing)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.api import stakeholders_bp, interactions_bp, tasks_bp, campaigns_bp, relationships_bp, auth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(stakeholders_bp, url_prefix='/api/stakeholders')
    app.register_blueprint(interactions_bp, url_prefix='/api/interactions')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(campaigns_bp, url_prefix='/api/campaigns')
    app.register_blueprint(relationships_bp, url_prefix='/api/relationships')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'stakeholder-platform'}, 200
    
    return app
