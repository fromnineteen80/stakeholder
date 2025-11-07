"""
Analytics Service - Influence/Interest Calculations and Reporting
"""
from app.models.stakeholder import Stakeholder
from app.models.interaction import Interaction
from app.models.campaign import Campaign
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func

class AnalyticsService:
    """
    Business logic for analytics and reporting
    Provides insights on stakeholder engagement and relationship health
    """
    
    @staticmethod
    def generate_stakeholder_map_data():
        """
        Generate data for stakeholder influence/interest matrix visualization
        """
        stakeholders = Stakeholder.query.all()
        
        map_data = {
            'quadrants': {
                'strategic_partner': [],
                'high_value_relationship': [],
                'collaborate': [],
                'defend': [],
                'proactively_defend': [],
                'protect': [],
                'commit': [],
                'connect': [],
                'monitor': []
            },
            'all_stakeholders': []
        }
        
        for s in stakeholders:
            data_point = {
                'id': s.id,
                'name': s.name,
                'organization': s.organization,
                'influence': s.influence_score,
                'interest': s.interest_score,
                'sentiment': s.sentiment or s.calculate_relationship_status(),
                'tags': s.tags
            }
            
            map_data['all_stakeholders'].append(data_point)
            
            # Categorize into quadrants
            sentiment = s.sentiment or s.calculate_relationship_status()
            if sentiment in map_data['quadrants']:
                map_data['quadrants'][sentiment.lower().replace(' ', '_')].append(data_point)
        
        return map_data
    
    @staticmethod
    def get_engagement_trends(days=90):
        """
        Get engagement trends over specified period
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        interactions_by_type = db.session.query(
            Interaction.interaction_type,
            func.count(Interaction.id).label('count')
        ).filter(
            Interaction.date >= cutoff_date
        ).group_by(
            Interaction.interaction_type
        ).all()
        
        interactions_by_sentiment = db.session.query(
            Interaction.sentiment,
            func.count(Interaction.id).label('count')
        ).filter(
            Interaction.date >= cutoff_date
        ).group_by(
            Interaction.sentiment
        ).all()
        
        return {
            'period_days': days,
            'by_type': {t: c for t, c in interactions_by_type},
            'by_sentiment': {s: c for s, c in interactions_by_sentiment},
            'total_interactions': sum(c for _, c in interactions_by_type)
        }
    
    @staticmethod
    def get_relationship_health_summary():
        """
        Get overall relationship health metrics
        """
        total_stakeholders = Stakeholder.query.count()
        
        sentiment_distribution = db.session.query(
            Stakeholder.sentiment,
            func.count(Stakeholder.id).label('count')
        ).group_by(
            Stakeholder.sentiment
        ).all()
        
        avg_influence = db.session.query(
            func.avg(Stakeholder.influence_score)
        ).scalar() or 0.0
        
        avg_interest = db.session.query(
            func.avg(Stakeholder.interest_score)
        ).scalar() or 0.0
        
        high_priority_count = Stakeholder.query.filter(
            Stakeholder.influence_score >= 7.0,
            Stakeholder.interest_score >= 5.0
        ).count()
        
        return {
            'total_stakeholders': total_stakeholders,
            'sentiment_distribution': {s: c for s, c in sentiment_distribution},
            'average_influence': round(avg_influence, 2),
            'average_interest': round(avg_interest, 2),
            'high_priority_count': high_priority_count,
            'high_priority_percentage': round((high_priority_count / total_stakeholders * 100), 2) if total_stakeholders > 0 else 0
        }
    
    @staticmethod
    def get_campaign_performance_metrics():
        """
        Get performance metrics across all campaigns
        """
        active_campaigns = Campaign.query.filter_by(status='active').count()
        completed_campaigns = Campaign.query.filter_by(status='completed').count()
        
        campaigns_by_phase = db.session.query(
            Campaign.phase,
            func.count(Campaign.id).label('count')
        ).group_by(
            Campaign.phase
        ).all()
        
        return {
            'active_campaigns': active_campaigns,
            'completed_campaigns': completed_campaigns,
            'by_phase': {p: c for p, c in campaigns_by_phase}
        }
