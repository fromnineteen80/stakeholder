"""
Configuration Management for Stakeholder Engagement Platform
Environment-specific settings for development, production, and testing
"""
import os
from datetime import timedelta

class Config:
    """Base configuration with common settings"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/stakeholder_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Redis settings
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'
    
    # Pagination
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 100
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx'}

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with production values
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    
    # Use SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
