"""
Interaction Model - Track all stakeholder engagements
"""
from datetime import datetime
from app import db

class Interaction(db.Model):
    """
    Interaction model for logging stakeholder engagements
    
    Tracks meetings, calls, emails, and other touchpoints
    Essential for relationship health scoring and history
    
    Attributes:
        id: Primary key
        stakeholder_id: Foreign key to Stakeholder
        user_id: Foreign key to User (who logged the interaction)
        interaction_type: Type (meeting, call, email, note, social_media)
        subject: Brief description or subject line
        description: Detailed notes about the interaction
        outcome: Result or next steps
        sentiment: Sentiment of interaction (positive, neutral, negative)
        date: When interaction occurred
        duration_minutes: Length of interaction
        follow_up_required: Whether follow-up is needed
        follow_up_date: When to follow up
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    stakeholder_id = db.Column(db.Integer, db.ForeignKey('stakeholders.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Interaction details
    interaction_type = db.Column(db.String(50), nullable=False, index=True)
    subject = db.Column(db.String(500))
    description = db.Column(db.Text)
    outcome = db.Column(db.Text)
    
    # Sentiment and scoring
    sentiment = db.Column(db.String(20), default='neutral')
    impact_on_relationship = db.Column(db.Float, default=0.0)
    
    # Timing
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    duration_minutes = db.Column(db.Integer)
    
    # Follow-up tracking
    follow_up_required = db.Column(db.Boolean, default=False)
    follow_up_date = db.Column(db.DateTime)
    follow_up_completed = db.Column(db.Boolean, default=False)
    
    # Metadata
    tags = db.Column(db.JSON, default=list)
    attachments = db.Column(db.JSON, default=list)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Valid interaction types
    INTERACTION_TYPES = [
        'meeting',
        'phone_call',
        'email',
        'video_call',
        'social_media',
        'note',
        'event',
        'other'
    ]
    
    # Valid sentiments
    SENTIMENTS = ['positive', 'neutral', 'negative']
    
    def __init__(self, stakeholder_id, user_id, interaction_type, subject=None):
        self.stakeholder_id = stakeholder_id
        self.user_id = user_id
        self.interaction_type = interaction_type
        self.subject = subject
    
    def add_tag(self, tag):
        """Add a tag to interaction"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def add_attachment(self, filename, url):
        """Add an attachment reference"""
        if not self.attachments:
            self.attachments = []
        self.attachments.append({
            'filename': filename,
            'url': url,
            'uploaded_at': datetime.utcnow().isoformat()
        })
    
    def to_dict(self, include_stakeholder=False, include_user=False):
        """Serialize interaction to dictionary"""
        data = {
            'id': self.id,
            'stakeholder_id': self.stakeholder_id,
            'user_id': self.user_id,
            'interaction_type': self.interaction_type,
            'subject': self.subject,
            'description': self.description,
            'outcome': self.outcome,
            'sentiment': self.sentiment,
            'impact_on_relationship': self.impact_on_relationship,
            'date': self.date.isoformat(),
            'duration_minutes': self.duration_minutes,
            'follow_up_required': self.follow_up_required,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'follow_up_completed': self.follow_up_completed,
            'tags': self.tags or [],
            'attachments': self.attachments or [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_stakeholder and self.stakeholder:
            data['stakeholder'] = {
                'id': self.stakeholder.id,
                'name': self.stakeholder.name,
                'organization': self.stakeholder.organization
            }
        
        if include_user and self.user:
            data['user'] = {
                'id': self.user.id,
                'full_name': self.user.full_name
            }
        
        return data
    
    def __repr__(self):
        return f'<Interaction {self.interaction_type} with {self.stakeholder_id}>'
