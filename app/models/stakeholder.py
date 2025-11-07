"""
Stakeholder Model - Profile Management and Relationship Mapping
"""
from datetime import datetime
from app import db

class Stakeholder(db.Model):
    """
    Stakeholder model for managing external relationships
    
    Tracks influence, interest, sentiment, and engagement history
    Core entity for the stakeholder engagement platform
    
    Attributes:
        id: Primary key
        name: Stakeholder full name
        title: Job title or role
        organization: Company or organization name
        email: Contact email
        phone: Contact phone
        influence_score: Influence level (-10 to 10)
        interest_score: Interest level (-10 to 10)
        sentiment: Current sentiment (Proactively Defend, Defend, Protect, etc.)
        tags: JSON array of categorization tags
        notes: Additional context and notes
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'stakeholders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    title = db.Column(db.String(255))
    organization = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), index=True)
    phone = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(500))
    twitter_handle = db.Column(db.String(100))
    
    # Stakeholder mapping scores
    influence_score = db.Column(db.Float, default=0.0, nullable=False)
    interest_score = db.Column(db.Float, default=0.0, nullable=False)
    
    # Relationship status based on HP 10-step framework
    sentiment = db.Column(db.String(50), default='Identify')
    
    # Categorization and context
    tags = db.Column(db.JSON, default=list)
    stakeholder_type = db.Column(db.String(100))
    priority = db.Column(db.String(20), default='Medium')
    
    # Additional information
    notes = db.Column(db.Text)
    address = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    interactions = db.relationship('Interaction', backref='stakeholder', lazy='dynamic', cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='stakeholder', lazy='dynamic')
    relationships = db.relationship('Relationship', 
                                   foreign_keys='Relationship.stakeholder_id',
                                   backref='stakeholder',
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    
    def __init__(self, name, email=None, organization=None):
        self.name = name
        self.email = email
        self.organization = organization
    
    def calculate_relationship_status(self):
        """
        Determine relationship status based on influence and interest scores
        
        Uses HP 10-step framework mapping:
        - High interest + High influence = Strategic Partnership
        - High interest + Low influence = Valuable Relationship
        - Low interest + High influence = Defend/Protect
        - Low interest + Low influence = Monitor
        """
        if self.interest_score >= 5 and self.influence_score >= 5:
            return 'Strategic Partner'
        elif self.interest_score >= 5 and self.influence_score >= 2:
            return 'High Value Relationship'
        elif self.interest_score >= 2 and self.influence_score >= 5:
            return 'Collaborate'
        elif self.interest_score >= 0 and self.influence_score >= 5:
            return 'Protect'
        elif self.interest_score <= -5 and self.influence_score >= 5:
            return 'Proactively Defend'
        elif self.interest_score <= -2 and self.influence_score >= 5:
            return 'Defend'
        elif self.interest_score >= 2:
            return 'Commit'
        elif self.interest_score >= 0:
            return 'Connect'
        else:
            return 'Monitor'
    
    def add_tag(self, tag):
        """Add a tag to stakeholder"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag):
        """Remove a tag from stakeholder"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def to_dict(self, include_interactions=False):
        """Serialize stakeholder to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'organization': self.organization,
            'email': self.email,
            'phone': self.phone,
            'linkedin_url': self.linkedin_url,
            'twitter_handle': self.twitter_handle,
            'influence_score': self.influence_score,
            'interest_score': self.interest_score,
            'sentiment': self.sentiment or self.calculate_relationship_status(),
            'tags': self.tags or [],
            'stakeholder_type': self.stakeholder_type,
            'priority': self.priority,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_interactions:
            data['interactions'] = [i.to_dict() for i in self.interactions.limit(10)]
            data['interaction_count'] = self.interactions.count()
        
        return data
    
    def __repr__(self):
        return f'<Stakeholder {self.name}>'
