"""
Task Model - Todoist-style task management
"""
from datetime import datetime
from app import db

class Task(db.Model):
    """
    Task model for team task management and stakeholder follow-ups
    
    Inspired by Todoist for simple, effective task tracking
    Supports assignments, priorities, due dates, and completion tracking
    
    Attributes:
        id: Primary key
        title: Task title or description
        description: Detailed task notes
        status: Task status (open, in_progress, completed, cancelled)
        priority: Task priority (low, medium, high, urgent)
        assigned_to: Foreign key to User (assignee)
        created_by: Foreign key to User (creator)
        stakeholder_id: Optional foreign key to Stakeholder
        campaign_id: Optional foreign key to Campaign
        due_date: When task is due
        completed_at: When task was completed
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    
    # Status and priority
    status = db.Column(db.String(20), default='open', nullable=False, index=True)
    priority = db.Column(db.String(20), default='medium', nullable=False, index=True)
    
    # Assignments
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Relationships
    stakeholder_id = db.Column(db.Integer, db.ForeignKey('stakeholders.id'), index=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), index=True)
    
    # Timing
    due_date = db.Column(db.DateTime, index=True)
    completed_at = db.Column(db.DateTime)
    
    # Metadata
    tags = db.Column(db.JSON, default=list)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Valid statuses
    STATUSES = ['open', 'in_progress', 'completed', 'cancelled']
    
    # Valid priorities
    PRIORITIES = ['low', 'medium', 'high', 'urgent']
    
    def __init__(self, title, created_by, priority='medium'):
        self.title = title
        self.created_by = created_by
        self.priority = priority
    
    def complete(self):
        """Mark task as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
    
    def cancel(self):
        """Mark task as cancelled"""
        self.status = 'cancelled'
    
    def reopen(self):
        """Reopen a completed or cancelled task"""
        self.status = 'open'
        self.completed_at = None
    
    def assign(self, user_id):
        """Assign task to user"""
        self.assigned_to = user_id
    
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status not in ['completed', 'cancelled']:
            return datetime.utcnow() > self.due_date
        return False
    
    def add_tag(self, tag):
        """Add a tag to task"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def to_dict(self, include_relationships=False):
        """Serialize task to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'created_by': self.created_by,
            'stakeholder_id': self.stakeholder_id,
            'campaign_id': self.campaign_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_overdue': self.is_overdue(),
            'tags': self.tags or [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_relationships:
            if self.assigned_user:
                data['assignee'] = {
                    'id': self.assigned_user.id,
                    'full_name': self.assigned_user.full_name
                }
            
            if self.creator:
                data['creator'] = {
                    'id': self.creator.id,
                    'full_name': self.creator.full_name
                }
            
            if self.stakeholder:
                data['stakeholder'] = {
                    'id': self.stakeholder.id,
                    'name': self.stakeholder.name
                }
        
        return data
    
    def __repr__(self):
        return f'<Task {self.title} ({self.status})>'
