"""
Stakeholder Service - Profile Management Business Logic
"""
from app.models.stakeholder import Stakeholder
from app.models.interaction import Interaction
from app import db
from datetime import datetime, timedelta

class StakeholderService:
    """
    Business logic for stakeholder management
    Handles profile updates, sentiment tracking, and relationship health
    """
    
    @staticmethod
    def calculate_engagement_score(stakeholder_id):
        """
        Calculate stakeholder engagement score based on interactions
        
        Factors:
        - Interaction frequency (30-day window)
        - Interaction sentiment
        - Interaction variety
        - Follow-up completion rate
        
        Returns:
            Float score between 0-10
        """
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        interactions = Interaction.query.filter(
            Interaction.stakeholder_id == stakeholder_id,
            Interaction.date >= cutoff_date
        ).all()
        
        if not interactions:
            return 0.0
        
        # Base score from frequency (0-4 points)
        frequency_score = min(len(interactions) * 0.5, 4.0)
        
        # Sentiment score (0-3 points)
        positive_count = sum(1 for i in interactions if i.sentiment == 'positive')
        sentiment_score = (positive_count / len(interactions)) * 3.0
        
        # Variety score (0-2 points)
        interaction_types = set(i.interaction_type for i in interactions)
        variety_score = min(len(interaction_types) * 0.5, 2.0)
        
        # Follow-up score (0-1 point)
        follow_ups = [i for i in interactions if i.follow_up_required]
        follow_up_score = 0.0
        if follow_ups:
            completed = sum(1 for i in follow_ups if i.follow_up_completed)
            follow_up_score = (completed / len(follow_ups)) * 1.0
        
        total_score = frequency_score + sentiment_score + variety_score + follow_up_score
        return round(total_score, 2)
    
    @staticmethod
    def update_relationship_health(stakeholder_id):
        """
        Update stakeholder relationship health based on recent interactions
        Updates influence and interest scores
        """
        stakeholder = Stakeholder.query.get(stakeholder_id)
        if not stakeholder:
            return None
        
        # Get recent interactions (90 days)
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        interactions = Interaction.query.filter(
            Interaction.stakeholder_id == stakeholder_id,
            Interaction.date >= cutoff_date
        ).all()
        
        if interactions:
            # Calculate average impact
            avg_impact = sum(i.impact_on_relationship or 0.0 for i in interactions) / len(interactions)
            
            # Adjust interest score based on interaction sentiment and impact
            positive_ratio = sum(1 for i in interactions if i.sentiment == 'positive') / len(interactions)
            interest_adjustment = (positive_ratio - 0.5) * 2.0 + avg_impact
            
            # Update interest score (bounded between -10 and 10)
            new_interest = stakeholder.interest_score + interest_adjustment
            stakeholder.interest_score = max(-10.0, min(10.0, new_interest))
            
            # Recalculate relationship status
            stakeholder.sentiment = stakeholder.calculate_relationship_status()
            
            db.session.commit()
        
        return stakeholder
    
    @staticmethod
    def get_priority_stakeholders(limit=10):
        """
        Get high-priority stakeholders that need attention
        Based on influence score, recent interaction frequency, and overdue follow-ups
        """
        # High influence stakeholders with no recent interactions
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        high_influence = Stakeholder.query.filter(
            Stakeholder.influence_score >= 7.0
        ).all()
        
        priority_stakeholders = []
        for stakeholder in high_influence:
            recent_interactions = Interaction.query.filter(
                Interaction.stakeholder_id == stakeholder.id,
                Interaction.date >= cutoff_date
            ).count()
            
            if recent_interactions == 0:
                priority_stakeholders.append({
                    'stakeholder': stakeholder.to_dict(),
                    'reason': 'High influence, no recent interaction',
                    'priority_score': stakeholder.influence_score
                })
        
        # Sort by priority score
        priority_stakeholders.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return priority_stakeholders[:limit]
    
    @staticmethod
    def bulk_update_tags(stakeholder_ids, tags_to_add=None, tags_to_remove=None):
        """Bulk update tags for multiple stakeholders"""
        stakeholders = Stakeholder.query.filter(Stakeholder.id.in_(stakeholder_ids)).all()
        
        for stakeholder in stakeholders:
            if tags_to_add:
                for tag in tags_to_add:
                    stakeholder.add_tag(tag)
            
            if tags_to_remove:
                for tag in tags_to_remove:
                    stakeholder.remove_tag(tag)
        
        db.session.commit()
        
        return len(stakeholders)
