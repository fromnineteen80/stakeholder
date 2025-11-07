"""
Campaigns API Endpoints
HP 10-step stakeholder engagement framework
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import campaigns_bp
from app.models.campaign import Campaign
from app.models.stakeholder import Stakeholder
from app import db

@campaigns_bp.route('', methods=['GET'])
@jwt_required()
def list_campaigns():
    """List campaigns"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status = request.args.get('status')
    phase = request.args.get('phase')
    
    query = Campaign.query
    
    if status:
        query = query.filter_by(status=status)
    if phase:
        query = query.filter_by(phase=phase)
    
    query = query.order_by(Campaign.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'campaigns': [c.to_dict(include_stakeholders=True) for c in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages
    }), 200

@campaigns_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_campaign(id):
    """Get campaign by ID"""
    campaign = Campaign.query.get_or_404(id)
    return jsonify({'campaign': campaign.to_dict(include_stakeholders=True)}), 200

@campaigns_bp.route('', methods=['POST'])
@jwt_required()
def create_campaign():
    """Create new campaign"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    campaign = Campaign(
        name=data['name'],
        owner_id=current_user_id,
        description=data.get('description')
    )
    
    for field in ['phase', 'status', 'start_date', 'end_date', 'goals', 
                  'target_audience', 'key_messages']:
        if field in data:
            setattr(campaign, field, data[field])
    
    db.session.add(campaign)
    db.session.commit()
    
    return jsonify({
        'message': 'Campaign created successfully',
        'campaign': campaign.to_dict()
    }), 201

@campaigns_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_campaign(id):
    """Update campaign"""
    campaign = Campaign.query.get_or_404(id)
    data = request.get_json()
    
    for field in ['name', 'description', 'phase', 'status', 'start_date', 
                  'end_date', 'goals', 'target_audience', 'key_messages', 
                  'engagement_score', 'shared_value_realized']:
        if field in data:
            setattr(campaign, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Campaign updated successfully',
        'campaign': campaign.to_dict()
    }), 200

@campaigns_bp.route('/<int:id>/stakeholders', methods=['POST'])
@jwt_required()
def add_stakeholder_to_campaign(id):
    """Add stakeholder to campaign"""
    campaign = Campaign.query.get_or_404(id)
    data = request.get_json()
    
    if not data.get('stakeholder_id'):
        return jsonify({'error': 'stakeholder_id is required'}), 400
    
    stakeholder = Stakeholder.query.get_or_404(data['stakeholder_id'])
    campaign.add_stakeholder(stakeholder)
    db.session.commit()
    
    return jsonify({'message': 'Stakeholder added to campaign successfully'}), 200

@campaigns_bp.route('/<int:id>/stakeholders/<int:stakeholder_id>', methods=['DELETE'])
@jwt_required()
def remove_stakeholder_from_campaign(id, stakeholder_id):
    """Remove stakeholder from campaign"""
    campaign = Campaign.query.get_or_404(id)
    stakeholder = Stakeholder.query.get_or_404(stakeholder_id)
    
    campaign.remove_stakeholder(stakeholder)
    db.session.commit()
    
    return jsonify({'message': 'Stakeholder removed from campaign successfully'}), 200

@campaigns_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(id):
    """Delete campaign"""
    campaign = Campaign.query.get_or_404(id)
    db.session.delete(campaign)
    db.session.commit()
    
    return jsonify({'message': 'Campaign deleted successfully'}), 200
