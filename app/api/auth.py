"""
Authentication API Endpoints
User registration, login, token management
"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.api import auth_bp
from app.models.user import User
from app import db

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
        {
            "email": "user@example.com",
            "password": "securepassword",
            "first_name": "John",
            "last_name": "Doe",
            "role": "member"
        }
    
    Returns:
        201: User created successfully
        400: Invalid input or user already exists
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User with this email already exists'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        role=data.get('role', 'member')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT tokens
    
    Request body:
        {
            "email": "user@example.com",
            "password": "securepassword"
        }
    
    Returns:
        200: Login successful with access and refresh tokens
        401: Invalid credentials
    """
    data = request.get_json()
    
    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    # Find user
    user = User.query.filter_by(email=data['email']).first()
    
    # Verify credentials
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Check if user is active
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 401
    
    # Create tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    
    Returns:
        200: New access token
    """
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user
    
    Returns:
        200: Current user details
        404: User not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """
    Update current authenticated user
    
    Request body:
        {
            "first_name": "John",
            "last_name": "Doe"
        }
    
    Returns:
        200: User updated successfully
        404: User not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    
    Request body:
        {
            "current_password": "oldpassword",
            "new_password": "newpassword"
        }
    
    Returns:
        200: Password changed successfully
        400: Invalid current password
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current and new passwords required'}), 400
    
    # Verify current password
    if not user.check_password(data['current_password']):
        return jsonify({'error': 'Invalid current password'}), 400
    
    # Update password
    user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200
