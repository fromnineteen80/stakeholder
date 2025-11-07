"""
Relationship Model - Stakeholder Connections and History
"""
from datetime import datetime
from app import db

class Relationship(db.Model):
    """
    Relationship model for tracking connections between stakeholders
    
    Maps stakeholder networks and influence patterns
    Supports relationship history and strength scoring
    
    Attributes:
        id: Primary key
        stakeholder_id: Foreign key to primary Stakeholder
        related_stakeholder_id: Foreign key to connected Stakeholder
        relationship_type: Type of connection (colleague, ally, competitor, etc.)
        strength: Relationship strength score (0-10)
        notes: Additional context about the relationship
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'relationships'
    
    id = db.Column(db.Integer, primary_key=True)
    stakeholder_id = db.Column(db.Integer, db.ForeignKey('stakeholders.id'), nullable=False, index=True)
    related_stakeholder_id = db.Column(db.Integer, db.ForeignKey('stakeholders.id'), nullable=False, index=True)
    
    # Relationship details
    relationship_type = db.Column(db.String(50), nullable=False)
    strength = db.Column(db.Float, default=5.0)
    
    # Context and notes
    notes = db.Column(db.Text)
    tags = db.Column(db.JSON, default=list)
    
    # Status tracking
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Valid relationship types
    RELATIONSHIP_TYPES = [
        'colleague',
        'supervisor',
        'subordinate',
        'ally',
        'competitor',
        'partner',
        'influencer',
        'advisor',
        'family',
        'friend',
        'neutral',
        'opponent',
        'other'
    ]
    
    def __init__(self, stakeholder_id, related_stakeholder_id, relationship_type):
        self.stakeholder_id = stakeholder_id
        self.related_stakeholder_id = related_stakeholder_id
        self.relationship_type = relationship_type
    
    def add_tag(self, tag):
        """Add a tag to relationship"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def to_dict(self, include_stakeholders=False):
        """Serialize relationship to dictionary"""
        data = {
            'id': self.id,
            'stakeholder_id': self.stakeholder_id,
            'related_stakeholder_id': self.related_stakeholder_id,
            'relationship_type': self.relationship_type,
            'strength': self.strength,
            'notes': self.notes,
            'tags': self.tags or [],
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_stakeholders:
            if self.stakeholder:
                data['stakeholder'] = {
                    'id': self.stakeholder.id,
                    'name': self.stakeholder.name
                }
            
            # Get related stakeholder using query
            from app.models.stakeholder import Stakeholder
            related = Stakeholder.query.get(self.related_stakeholder_id)
            if related:
                data['related_stakeholder'] = {
                    'id': related.id,
                    'name': related.name
                }
        
        return data
    
    def __repr__(self):
        return f'<Relationship {self.stakeholder_id} -> {self.related_stakeholder_id} ({self.relationship_type})>'
