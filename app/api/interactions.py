"""
Interactions API Endpoints
Log and retrieve stakeholder interactions
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import interactions_bp
from app.models.interaction import Interaction
from app import db

@interactions_bp.route('', methods=['GET'])
@jwt_required()
def list_interactions():
    """List interactions with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    stakeholder_id = request.args.get('stakeholder_id', type=int)
    interaction_type = request.args.get('type')
    
    query = Interaction.query
    
    if stakeholder_id:
        query = query.filter_by(stakeholder_id=stakeholder_id)
    if interaction_type:
        query = query.filter_by(interaction_type=interaction_type)
    
    query = query.order_by(Interaction.date.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'interactions': [i.to_dict(include_stakeholder=True, include_user=True) for i in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages
    }), 200

@interactions_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_interaction(id):
    """Get interaction by ID"""
    interaction = Interaction.query.get_or_404(id)
    return jsonify({'interaction': interaction.to_dict(include_stakeholder=True, include_user=True)}), 200

@interactions_bp.route('', methods=['POST'])
@jwt_required()
def create_interaction():
    """Create new interaction"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('stakeholder_id') or not data.get('interaction_type'):
        return jsonify({'error': 'stakeholder_id and interaction_type required'}), 400
    
    interaction = Interaction(
        stakeholder_id=data['stakeholder_id'],
        user_id=current_user_id,
        interaction_type=data['interaction_type'],
        subject=data.get('subject')
    )
    
    for field in ['description', 'outcome', 'sentiment', 'impact_on_relationship', 
                  'date', 'duration_minutes', 'follow_up_required', 'follow_up_date', 'tags']:
        if field in data:
            setattr(interaction, field, data[field])
    
    db.session.add(interaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Interaction logged successfully',
        'interaction': interaction.to_dict()
    }), 201

@interactions_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_interaction(id):
    """Update interaction"""
    interaction = Interaction.query.get_or_404(id)
    data = request.get_json()
    
    for field in ['subject', 'description', 'outcome', 'sentiment', 
                  'impact_on_relationship', 'date', 'duration_minutes', 
                  'follow_up_required', 'follow_up_date', 'follow_up_completed', 'tags']:
        if field in data:
            setattr(interaction, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Interaction updated successfully',
        'interaction': interaction.to_dict()
    }), 200

@interactions_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_interaction(id):
    """Delete interaction"""
    interaction = Interaction.query.get_or_404(id)
    db.session.delete(interaction)
    db.session.commit()
    
    return jsonify({'message': 'Interaction deleted successfully'}), 200
