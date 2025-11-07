"""
User Model - Authentication and Authorization
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """
    User model for platform authentication and team collaboration
    
    Attributes:
        id: Primary key
        email: Unique email address for login
        password_hash: Hashed password (bcrypt)
        first_name: User's first name
        last_name: User's last name
        role: User role (admin, manager, member, viewer)
        is_active: Account status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='member')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    interactions = db.relationship('Interaction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='assigned_user', lazy='dynamic', foreign_keys='Task.assigned_to')
    created_tasks = db.relationship('Task', backref='creator', lazy='dynamic', foreign_keys='Task.created_by')
    campaigns = db.relationship('Campaign', backref='owner', lazy='dynamic')
    
    def __init__(self, email, password, first_name, last_name, role='member'):
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, permission):
        """
        Check if user has specific permission based on role
        
        Permissions hierarchy:
        - admin: Full access (create, read, update, delete all)
        - manager: Create, read, update stakeholders and campaigns
        - member: Read, create interactions and tasks
        - viewer: Read-only access
        """
        role_permissions = {
            'admin': ['create', 'read', 'update', 'delete', 'manage_users'],
            'manager': ['create', 'read', 'update', 'manage_campaigns'],
            'member': ['read', 'create_interaction', 'create_task'],
            'viewer': ['read']
        }
        return permission in role_permissions.get(self.role, [])
    
    def to_dict(self):
        """Serialize user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
