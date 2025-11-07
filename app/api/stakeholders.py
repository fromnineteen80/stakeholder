"""
Stakeholders API Endpoints
CRUD operations for stakeholder management
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import stakeholders_bp
from app.models.stakeholder import Stakeholder
from app.models.user import User
from app import db

@stakeholders_bp.route('', methods=['GET'])
@jwt_required()
def list_stakeholders():
    """
    List all stakeholders with optional filtering
    
    Query parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 50)
        - search: Search by name or organization
        - tag: Filter by tag
        - sentiment: Filter by relationship sentiment
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    search = request.args.get('search')
    tag = request.args.get('tag')
    sentiment = request.args.get('sentiment')
    
    query = Stakeholder.query
    
    if search:
        query = query.filter(
            db.or_(
                Stakeholder.name.ilike(f'%{search}%'),
                Stakeholder.organization.ilike(f'%{search}%')
            )
        )
    
    if sentiment:
        query = query.filter_by(sentiment=sentiment)
    
    if tag:
        query = query.filter(Stakeholder.tags.contains([tag]))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'stakeholders': [s.to_dict() for s in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@stakeholders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_stakeholder(id):
    """Get stakeholder by ID with full details"""
    stakeholder = Stakeholder.query.get_or_404(id)
    return jsonify({'stakeholder': stakeholder.to_dict(include_interactions=True)}), 200

@stakeholders_bp.route('', methods=['POST'])
@jwt_required()
def create_stakeholder():
    """
    Create new stakeholder
    
    Request body:
        {
            "name": "John Doe",
            "title": "CEO",
            "organization": "Acme Corp",
            "email": "john@acme.com",
            "phone": "555-1234",
            "influence_score": 7.5,
            "interest_score": 5.0,
            "tags": ["government", "supporter"]
        }
    """
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    stakeholder = Stakeholder(
        name=data['name'],
        email=data.get('email'),
        organization=data.get('organization')
    )
    
    # Set optional fields
    for field in ['title', 'phone', 'linkedin_url', 'twitter_handle', 
                  'influence_score', 'interest_score', 'stakeholder_type', 
                  'priority', 'notes', 'address']:
        if field in data:
            setattr(stakeholder, field, data[field])
    
    # Set tags
    if 'tags' in data:
        stakeholder.tags = data['tags']
    
    # Calculate sentiment based on scores
    stakeholder.sentiment = stakeholder.calculate_relationship_status()
    
    db.session.add(stakeholder)
    db.session.commit()
    
    return jsonify({
        'message': 'Stakeholder created successfully',
        'stakeholder': stakeholder.to_dict()
    }), 201

@stakeholders_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_stakeholder(id):
    """Update stakeholder"""
    stakeholder = Stakeholder.query.get_or_404(id)
    data = request.get_json()
    
    # Update fields
    for field in ['name', 'title', 'organization', 'email', 'phone', 
                  'linkedin_url', 'twitter_handle', 'influence_score', 
                  'interest_score', 'stakeholder_type', 'priority', 
                  'notes', 'address', 'tags']:
        if field in data:
            setattr(stakeholder, field, data[field])
    
    # Recalculate sentiment if scores changed
    if 'influence_score' in data or 'interest_score' in data:
        stakeholder.sentiment = stakeholder.calculate_relationship_status()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Stakeholder updated successfully',
        'stakeholder': stakeholder.to_dict()
    }), 200

@stakeholders_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_stakeholder(id):
    """Delete stakeholder"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.has_permission('delete'):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    stakeholder = Stakeholder.query.get_or_404(id)
    db.session.delete(stakeholder)
    db.session.commit()
    
    return jsonify({'message': 'Stakeholder deleted successfully'}), 200

@stakeholders_bp.route('/map', methods=['GET'])
@jwt_required()
def stakeholder_map():
    """
    Get stakeholder map data for visualization
    Returns all stakeholders with influence and interest scores
    """
    stakeholders = Stakeholder.query.all()
    
    map_data = {
        'stakeholders': [
            {
                'id': s.id,
                'name': s.name,
                'organization': s.organization,
                'influence_score': s.influence_score,
                'interest_score': s.interest_score,
                'sentiment': s.sentiment or s.calculate_relationship_status(),
                'tags': s.tags
            } for s in stakeholders
        ]
    }
    
    return jsonify(map_data), 200
