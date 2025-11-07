"""
API Blueprints for Stakeholder Engagement Platform
RESTful API endpoints for frontend consumption
"""
from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__)
stakeholders_bp = Blueprint('stakeholders', __name__)
interactions_bp = Blueprint('interactions', __name__)
tasks_bp = Blueprint('tasks', __name__)
campaigns_bp = Blueprint('campaigns', __name__)
relationships_bp = Blueprint('relationships', __name__)

# Import routes after blueprint creation to avoid circular imports
from app.api import auth, stakeholders, interactions, tasks, campaigns, relationships

__all__ = [
    'auth_bp',
    'stakeholders_bp',
    'interactions_bp',
    'tasks_bp',
    'campaigns_bp',
    'relationships_bp'
]
