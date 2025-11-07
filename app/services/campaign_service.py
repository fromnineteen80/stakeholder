"""
Campaign Service - HP 10-Step Framework Business Logic
"""
from app.models.campaign import Campaign
from app.models.stakeholder import Stakeholder
from app.models.task import Task
from app import db

class CampaignService:
    """
    Business logic for campaign management
    Implements HP 10-step stakeholder engagement framework
    """
    
    # HP 10-Step Framework template
    FRAMEWORK_STEPS = {
        'purpose': [
            {'step': 1, 'name': 'Set Goals', 'description': 'Define how stakeholder relations will support organizational goals'},
            {'step': 2, 'name': 'Issue Identification', 'description': 'Assess current status and identify key issues'},
            {'step': 3, 'name': 'Stakeholder Identification', 'description': 'Identify those with influence over business'},
            {'step': 4, 'name': 'Stakeholder Prioritization', 'description': 'Prioritize by opportunity or risk'}
        ],
        'plan': [
            {'step': 5, 'name': 'Landscape Analysis', 'description': 'Map complete stakeholder landscape'},
            {'step': 6, 'name': 'Team Alignment', 'description': 'Align internal teams and establish governance'},
            {'step': 7, 'name': 'Research & Listening', 'description': 'Conduct research and listening sessions'},
            {'step': 8, 'name': 'Stakeholder Analysis', 'description': 'Analyze data and create predictive models'}
        ],
        'execute': [
            {'step': 9, 'name': 'Launch Campaign', 'description': 'Launch purposeful communication'},
            {'step': 10, 'name': 'Ongoing Analysis', 'description': 'Continuously analyze stakeholder sentiment'},
            {'step': 11, 'name': 'Collaborate', 'description': 'Engage directly with stakeholders'},
            {'step': 12, 'name': 'Realize Value', 'description': 'Create and measure shared value outcomes'}
        ]
    }
    
    @staticmethod
    def create_campaign_with_framework(name, owner_id, description=None):
        """
        Create new campaign with HP 10-step framework tasks
        Auto-generates tasks for each framework step
        """
        campaign = Campaign(
            name=name,
            owner_id=owner_id,
            description=description
        )
        
        db.session.add(campaign)
        db.session.flush()
        
        # Create tasks for each framework step
        for phase, steps in CampaignService.FRAMEWORK_STEPS.items():
            for step_info in steps:
                task = Task(
                    title=f"Step {step_info['step']}: {step_info['name']}",
                    description=step_info['description'],
                    created_by=owner_id,
                    campaign_id=campaign.id,
                    priority='high' if step_info['step'] <= 4 else 'medium'
                )
                task.add_tag(phase)
                task.add_tag('framework')
                db.session.add(task)
        
        db.session.commit()
        
        return campaign
    
    @staticmethod
    def advance_campaign_phase(campaign_id):
        """
        Move campaign to next phase and update relevant tasks
        """
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return None
        
        campaign.advance_phase()
        
        # Update task priorities for current phase
        current_phase_tasks = Task.query.filter(
            Task.campaign_id == campaign_id,
            Task.tags.contains([campaign.phase])
        ).all()
        
        for task in current_phase_tasks:
            if task.status == 'open':
                task.priority = 'urgent'
        
        db.session.commit()
        
        return campaign
    
    @staticmethod
    def get_campaign_progress(campaign_id):
        """
        Calculate campaign progress based on completed tasks
        """
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return None
        
        total_tasks = Task.query.filter_by(campaign_id=campaign_id).count()
        completed_tasks = Task.query.filter_by(
            campaign_id=campaign_id,
            status='completed'
        ).count()
        
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'campaign_id': campaign_id,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress_percentage': round(progress_percentage, 2),
            'current_phase': campaign.phase,
            'status': campaign.status
        }
    
    @staticmethod
    def recommend_stakeholders_for_campaign(campaign_id, min_influence=5.0, min_interest=0.0):
        """
        Recommend stakeholders for campaign based on influence and interest scores
        """
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return []
        
        # Get stakeholders not already in campaign
        current_stakeholder_ids = [s.id for s in campaign.stakeholders]
        
        recommended = Stakeholder.query.filter(
            Stakeholder.influence_score >= min_influence,
            Stakeholder.interest_score >= min_interest,
            ~Stakeholder.id.in_(current_stakeholder_ids) if current_stakeholder_ids else True
        ).order_by(
            Stakeholder.influence_score.desc(),
            Stakeholder.interest_score.desc()
        ).limit(20).all()
        
        return [s.to_dict() for s in recommended]
