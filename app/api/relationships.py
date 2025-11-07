"""
Relationships API Endpoints
Stakeholder connections and network mapping
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.api import relationships_bp
from app.models.relationship import Relationship
from app import db

@relationships_bp.route('', methods=['GET'])
@jwt_required()
def list_relationships():
    """List relationships"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    stakeholder_id = request.args.get('stakeholder_id', type=int)
    relationship_type = request.args.get('type')
    
    query = Relationship.query
    
    if stakeholder_id:
        query = query.filter(
            db.or_(
                Relationship.stakeholder_id == stakeholder_id,
                Relationship.related_stakeholder_id == stakeholder_id
            )
        )
    if relationship_type:
        query = query.filter_by(relationship_type=relationship_type)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'relationships': [r.to_dict(include_stakeholders=True) for r in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages
    }), 200

@relationships_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_relationship(id):
    """Get relationship by ID"""
    relationship = Relationship.query.get_or_404(id)
    return jsonify({'relationship': relationship.to_dict(include_stakeholders=True)}), 200

@relationships_bp.route('', methods=['POST'])
@jwt_required()
def create_relationship():
    """Create new relationship"""
    data = request.get_json()
    
    required = ['stakeholder_id', 'related_stakeholder_id', 'relationship_type']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    relationship = Relationship(
        stakeholder_id=data['stakeholder_id'],
        related_stakeholder_id=data['related_stakeholder_id'],
        relationship_type=data['relationship_type']
    )
    
    for field in ['strength', 'notes', 'tags', 'is_active']:
        if field in data:
            setattr(relationship, field, data[field])
    
    db.session.add(relationship)
    db.session.commit()
    
    return jsonify({
        'message': 'Relationship created successfully',
        'relationship': relationship.to_dict()
    }), 201

@relationships_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_relationship(id):
    """Update relationship"""
    relationship = Relationship.query.get_or_404(id)
    data = request.get_json()
    
    for field in ['relationship_type', 'strength', 'notes', 'tags', 'is_active']:
        if field in data:
            setattr(relationship, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Relationship updated successfully',
        'relationship': relationship.to_dict()
    }), 200

@relationships_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_relationship(id):
    """Delete relationship"""
    relationship = Relationship.query.get_or_404(id)
    db.session.delete(relationship)
    db.session.commit()
    
    return jsonify({'message': 'Relationship deleted successfully'}), 200

@relationships_bp.route('/network/<int:stakeholder_id>', methods=['GET'])
@jwt_required()
def get_stakeholder_network(stakeholder_id):
    """Get complete network for a stakeholder"""
    relationships = Relationship.query.filter(
        db.or_(
            Relationship.stakeholder_id == stakeholder_id,
            Relationship.related_stakeholder_id == stakeholder_id
        )
    ).all()
    
    return jsonify({
        'stakeholder_id': stakeholder_id,
        'relationships': [r.to_dict(include_stakeholders=True) for r in relationships],
        'count': len(relationships)
    }), 200
