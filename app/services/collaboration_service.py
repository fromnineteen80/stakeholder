"""
Collaboration Service - Team Coordination Business Logic
"""
from app.models.user import User
from app.models.stakeholder import Stakeholder
from app.models.interaction import Interaction
from app.models.campaign import Campaign
from app import db
from datetime import datetime, timedelta

class CollaborationService:
    """
    Business logic for team collaboration
    Supports Slack-style real-time coordination and context sharing
    """
    
    @staticmethod
    def get_team_activity_feed(limit=50):
        """
        Get recent team activity across all entities
        Shows recent interactions, task completions, and campaign updates
        """
        # Recent interactions
        recent_interactions = Interaction.query.order_by(
            Interaction.created_at.desc()
        ).limit(limit).all()
        
        activity_feed = []
        
        for interaction in recent_interactions:
            activity_feed.append({
                'type': 'interaction',
                'timestamp': interaction.created_at.isoformat(),
                'user': interaction.user.full_name if interaction.user else 'Unknown',
                'stakeholder': interaction.stakeholder.name if interaction.stakeholder else 'Unknown',
                'action': f'{interaction.interaction_type} logged',
                'details': interaction.subject
            })
        
        # Sort by timestamp
        activity_feed.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return activity_feed[:limit]
    
    @staticmethod
    def get_stakeholder_engagement_history(stakeholder_id, days=90):
        """
        Get comprehensive engagement history for a stakeholder
        Shows all team member interactions and activity
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        interactions = Interaction.query.filter(
            Interaction.stakeholder_id == stakeholder_id,
            Interaction.date >= cutoff_date
        ).order_by(Interaction.date.desc()).all()
        
        history = []
        for interaction in interactions:
            history.append({
                'date': interaction.date.isoformat(),
                'type': interaction.interaction_type,
                'user': interaction.user.full_name if interaction.user else 'Unknown',
                'subject': interaction.subject,
                'sentiment': interaction.sentiment,
                'follow_up_required': interaction.follow_up_required
            })
        
        return {
            'stakeholder_id': stakeholder_id,
            'period_days': days,
            'interaction_count': len(history),
            'history': history
        }
    
    @staticmethod
    def get_shared_stakeholders(user_id1, user_id2):
        """
        Get stakeholders that two team members have both interacted with
        Useful for collaboration and knowledge sharing
        """
        user1_stakeholders = db.session.query(Interaction.stakeholder_id).filter(
            Interaction.user_id == user_id1
        ).distinct().subquery()
        
        user2_stakeholders = db.session.query(Interaction.stakeholder_id).filter(
            Interaction.user_id == user_id2
        ).distinct().subquery()
        
        shared_ids = db.session.query(user1_stakeholders.c.stakeholder_id).join(
            user2_stakeholders,
            user1_stakeholders.c.stakeholder_id == user2_stakeholders.c.stakeholder_id
        ).all()
        
        shared_stakeholder_ids = [id[0] for id in shared_ids]
        stakeholders = Stakeholder.query.filter(Stakeholder.id.in_(shared_stakeholder_ids)).all()
        
        return [s.to_dict() for s in stakeholders]
    
    @staticmethod
    def get_campaign_team_activity(campaign_id):
        """
        Get team activity specific to a campaign
        Shows all interactions with campaign stakeholders
        """
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return None
        
        stakeholder_ids = [s.id for s in campaign.stakeholders]
        
        if not stakeholder_ids:
            return {
                'campaign_id': campaign_id,
                'activity': []
            }
        
        interactions = Interaction.query.filter(
            Interaction.stakeholder_id.in_(stakeholder_ids)
        ).order_by(Interaction.date.desc()).limit(100).all()
        
        activity = []
        for interaction in interactions:
            activity.append({
                'date': interaction.date.isoformat(),
                'user': interaction.user.full_name if interaction.user else 'Unknown',
                'stakeholder': interaction.stakeholder.name if interaction.stakeholder else 'Unknown',
                'type': interaction.interaction_type,
                'subject': interaction.subject
            })
        
        return {
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'activity_count': len(activity),
            'activity': activity
        }
