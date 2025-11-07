"""
Business Logic Services for Stakeholder Engagement Platform
"""
from app.services.stakeholder_service import StakeholderService
from app.services.campaign_service import CampaignService
from app.services.analytics_service import AnalyticsService
from app.services.task_service import TaskService
from app.services.collaboration_service import CollaborationService

__all__ = [
    'StakeholderService',
    'CampaignService',
    'AnalyticsService',
    'TaskService',
    'CollaborationService'
]
