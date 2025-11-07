"""
Tasks API Endpoints
Todoist-style task management
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import tasks_bp
from app.models.task import Task
from app import db

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def list_tasks():
    """List tasks with filtering"""
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    assigned_to_me = request.args.get('assigned_to_me', type=bool)
    
    query = Task.query
    
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if assigned_to_me:
        query = query.filter_by(assigned_to=current_user_id)
    
    query = query.order_by(Task.due_date.asc().nullslast(), Task.priority.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'tasks': [t.to_dict(include_relationships=True) for t in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages
    }), 200

@tasks_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_task(id):
    """Get task by ID"""
    task = Task.query.get_or_404(id)
    return jsonify({'task': task.to_dict(include_relationships=True)}), 200

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """Create new task"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        created_by=current_user_id,
        priority=data.get('priority', 'medium')
    )
    
    for field in ['description', 'status', 'assigned_to', 'stakeholder_id', 
                  'campaign_id', 'due_date', 'tags']:
        if field in data:
            setattr(task, field, data[field])
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201

@tasks_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    """Update task"""
    task = Task.query.get_or_404(id)
    data = request.get_json()
    
    for field in ['title', 'description', 'status', 'priority', 'assigned_to', 
                  'stakeholder_id', 'campaign_id', 'due_date', 'tags']:
        if field in data:
            setattr(task, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    }), 200

@tasks_bp.route('/<int:id>/complete', methods=['POST'])
@jwt_required()
def complete_task(id):
    """Mark task as completed"""
    task = Task.query.get_or_404(id)
    task.complete()
    db.session.commit()
    
    return jsonify({
        'message': 'Task completed successfully',
        'task': task.to_dict()
    }), 200

@tasks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    """Delete task"""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}), 200
