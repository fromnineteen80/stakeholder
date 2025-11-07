"""
Task Service - Todoist-style Task Management Business Logic
"""
from app.models.task import Task
from app.models.user import User
from app import db
from datetime import datetime, timedelta

class TaskService:
    """
    Business logic for task management
    Todoist-inspired simple and effective task tracking
    """
    
    @staticmethod
    def get_user_task_dashboard(user_id):
        """
        Get comprehensive task dashboard for user
        Includes overdue, today, upcoming, and completed tasks
        """
        now = datetime.utcnow()
        today_end = now.replace(hour=23, minute=59, second=59)
        week_end = now + timedelta(days=7)
        
        # Overdue tasks
        overdue = Task.query.filter(
            Task.assigned_to == user_id,
            Task.status.in_(['open', 'in_progress']),
            Task.due_date < now
        ).order_by(Task.due_date.asc()).all()
        
        # Today's tasks
        today = Task.query.filter(
            Task.assigned_to == user_id,
            Task.status.in_(['open', 'in_progress']),
            Task.due_date >= now,
            Task.due_date <= today_end
        ).order_by(Task.priority.desc()).all()
        
        # This week's tasks
        this_week = Task.query.filter(
            Task.assigned_to == user_id,
            Task.status.in_(['open', 'in_progress']),
            Task.due_date > today_end,
            Task.due_date <= week_end
        ).order_by(Task.due_date.asc()).all()
        
        # Recently completed
        completed = Task.query.filter(
            Task.assigned_to == user_id,
            Task.status == 'completed'
        ).order_by(Task.completed_at.desc()).limit(10).all()
        
        return {
            'overdue': [t.to_dict() for t in overdue],
            'today': [t.to_dict() for t in today],
            'this_week': [t.to_dict() for t in this_week],
            'recently_completed': [t.to_dict() for t in completed],
            'counts': {
                'overdue': len(overdue),
                'today': len(today),
                'this_week': len(this_week)
            }
        }
    
    @staticmethod
    def bulk_assign_tasks(task_ids, user_id):
        """Bulk assign tasks to user"""
        tasks = Task.query.filter(Task.id.in_(task_ids)).all()
        
        for task in tasks:
            task.assign(user_id)
        
        db.session.commit()
        
        return len(tasks)
    
    @staticmethod
    def bulk_complete_tasks(task_ids):
        """Bulk complete tasks"""
        tasks = Task.query.filter(Task.id.in_(task_ids)).all()
        
        for task in tasks:
            task.complete()
        
        db.session.commit()
        
        return len(tasks)
    
    @staticmethod
    def get_team_workload_distribution():
        """
        Get workload distribution across team members
        """
        users = User.query.filter_by(is_active=True).all()
        
        distribution = []
        for user in users:
            open_tasks = Task.query.filter(
                Task.assigned_to == user.id,
                Task.status.in_(['open', 'in_progress'])
            ).count()
            
            overdue_tasks = Task.query.filter(
                Task.assigned_to == user.id,
                Task.status.in_(['open', 'in_progress']),
                Task.due_date < datetime.utcnow()
            ).count()
            
            distribution.append({
                'user': user.to_dict(),
                'open_tasks': open_tasks,
                'overdue_tasks': overdue_tasks
            })
        
        return distribution
