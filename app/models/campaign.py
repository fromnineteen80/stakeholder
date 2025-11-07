"""
Campaign Model - Stakeholder Engagement Campaigns
"""
from datetime import datetime
from app import db

# Association table for many-to-many relationship between campaigns and stakeholders
campaign_stakeholders = db.Table('campaign_stakeholders',
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id'), primary_key=True),
    db.Column('stakeholder_id', db.Integer, db.ForeignKey('stakeholders.id'), primary_key=True),
    db.Column('added_at', db.DateTime, default=datetime.utcnow)
)

class Campaign(db.Model):
    """
    Campaign model for managing stakeholder engagement initiatives
    
    Based on HP 10-step engagement framework:
    - Purpose: Set goals, identify issues, identify stakeholders, prioritize
    - Plan: Landscape analysis, team alignment, research, stakeholder modeling
    - Execute: Launch campaign, ongoing analysis, collaborate, realize value
    
    Attributes:
        id: Primary key
        name: Campaign name
        description: Campaign objectives and details
        phase: Current phase (purpose, plan, execute)
        status: Campaign status (planning, active, paused, completed)
        owner_id: Foreign key to User (campaign owner)
        start_date: Campaign start date
        end_date: Campaign end date
        goals: JSON array of campaign goals
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Campaign phase and status
    phase = db.Column(db.String(50), default='purpose', nullable=False)
    status = db.Column(db.String(20), default='planning', nullable=False, index=True)
    
    # Ownership
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Timeline
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    
    # Campaign details
    goals = db.Column(db.JSON, default=list)
    target_audience = db.Column(db.Text)
    key_messages = db.Column(db.JSON, default=list)
    
    # Metrics and tracking
    engagement_score = db.Column(db.Float, default=0.0)
    shared_value_realized = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    stakeholders = db.relationship('Stakeholder', 
                                  secondary=campaign_stakeholders,
                                  backref=db.backref('campaigns', lazy='dynamic'))
    tasks = db.relationship('Task', backref='campaign', lazy='dynamic')
    
    # Valid phases (HP 10-step framework)
    PHASES = ['purpose', 'plan', 'execute']
    
    # Valid statuses
    STATUSES = ['planning', 'active', 'paused', 'completed', 'cancelled']
    
    def __init__(self, name, owner_id, description=None):
        self.name = name
        self.owner_id = owner_id
        self.description = description
    
    def add_stakeholder(self, stakeholder):
        """Add stakeholder to campaign"""
        if stakeholder not in self.stakeholders:
            self.stakeholders.append(stakeholder)
    
    def remove_stakeholder(self, stakeholder):
        """Remove stakeholder from campaign"""
        if stakeholder in self.stakeholders:
            self.stakeholders.remove(stakeholder)
    
    def add_goal(self, goal):
        """Add a goal to campaign"""
        if not self.goals:
            self.goals = []
        self.goals.append({
            'text': goal,
            'added_at': datetime.utcnow().isoformat()
        })
    
    def add_message(self, message):
        """Add a key message to campaign"""
        if not self.key_messages:
            self.key_messages = []
        self.key_messages.append(message)
    
    def advance_phase(self):
        """Move campaign to next phase"""
        phase_order = ['purpose', 'plan', 'execute']
        current_index = phase_order.index(self.phase)
        if current_index < len(phase_order) - 1:
            self.phase = phase_order[current_index + 1]
    
    def activate(self):
        """Set campaign status to active"""
        self.status = 'active'
        if not self.start_date:
            self.start_date = datetime.utcnow()
    
    def complete(self):
        """Mark campaign as completed"""
        self.status = 'completed'
        if not self.end_date:
            self.end_date = datetime.utcnow()
    
    def pause(self):
        """Pause campaign"""
        self.status = 'paused'
    
    def to_dict(self, include_stakeholders=False):
        """Serialize campaign to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'phase': self.phase,
            'status': self.status,
            'owner_id': self.owner_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'goals': self.goals or [],
            'target_audience': self.target_audience,
            'key_messages': self.key_messages or [],
            'engagement_score': self.engagement_score,
            'shared_value_realized': self.shared_value_realized,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_stakeholders:
            data['stakeholders'] = [
                {
                    'id': s.id,
                    'name': s.name,
                    'organization': s.organization
                } for s in self.stakeholders
            ]
            data['stakeholder_count'] = len(self.stakeholders)
        
        return data
    
    def __repr__(self):
        return f'<Campaign {self.name} ({self.status})>'
