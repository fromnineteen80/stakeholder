# File Tree - Stakeholder Engagement Platform

Last Updated: 2025-11-06
Status: Setup Phase Complete

```
stakeholder/
│
├── .gitignore                              # Git ignore patterns
│
├── project_status.py                       # ACTIVE project status tracker (v1)
├── workflow_process.py                     # 10-step workflow documentation (executable)
├── file_tree.md                            # THIS FILE - complete structure reference
│
├── management/                             # Archived status files (when tokens < 50k)
│   └── README.md                           # Management folder documentation
│
├── research_addendum_CRITICAL.md          # Soappboxx competitive analysis
├── stakeholder_engagement_research.md     # Market research and UX analysis  
└── stakeholder_project_findings.md        # HP tariff case study and platform design

```

## File Descriptions

### Project Management
- **project_status.py** - Executable Python file tracking completed/pending tasks, tech stack, and token usage
- **workflow_process.py** - Complete 10-step workflow process for stateless Claude sessions
- **file_tree.md** - This file; documents complete repository structure

### Research Documents
- **research_addendum_CRITICAL.md** - Soappboxx platform analysis, predictive modeling, design system
- **stakeholder_engagement_research.md** - Competitor analysis (12 platforms), UX best practices, architecture
- **stakeholder_project_findings.md** - HP tariff advocacy case study, HP 10-step process, MVP definition

### Configuration
- **.gitignore** - Excludes archived status files, Python cache, environment files

## Next Phase: Alpha File Structure (Step 3)

### Backend Structure (Planned)
```
app/
├── __init__.py                    # Flask app factory
├── models/                        # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py
│   ├── stakeholder.py
│   ├── interaction.py
│   ├── task.py
│   ├── campaign.py
│   └── relationship.py
├── api/                          # RESTful endpoints
│   ├── __init__.py
│   ├── stakeholders.py
│   ├── interactions.py
│   ├── tasks.py
│   ├── campaigns.py
│   └── relationships.py
└── services/                     # Business logic
    ├── __init__.py
    ├── stakeholder_service.py
    ├── campaign_service.py
    ├── analytics_service.py
    ├── task_service.py
    └── collaboration_service.py

config.py                         # Configuration management
requirements.txt                  # Python dependencies
```

### Frontend Structure (Planned)
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/              # Reusable components
│   │   ├── base/               # Buttons, inputs, etc.
│   │   ├── layout/             # Header, sidebar, etc.
│   │   ├── data/               # Tables, lists, charts
│   │   ├── stakeholder/        # Stakeholder-specific
│   │   ├── interaction/        # Interaction-specific
│   │   └── task/               # Task-specific
│   ├── pages/                  # Page components
│   │   ├── Dashboard.jsx
│   │   ├── StakeholderList.jsx
│   │   ├── StakeholderDetail.jsx
│   │   ├── CampaignManager.jsx
│   │   └── TaskList.jsx
│   ├── theme/                  # MD3 + Soappboxx colors
│   │   ├── colors.js
│   │   ├── typography.js
│   │   └── theme.js
│   ├── services/               # API client
│   │   └── api.js
│   ├── App.jsx
│   └── index.jsx
└── package.json
```

## Token Tracking

| Session | Start | Used | Remaining | Status |
|---------|-------|------|-----------|--------|
| v1      | 190000| 42105| 147895    | Active |

## Notes

- All archived status files moved to `management/` when tokens < 50k
- Status files are executable Python (no abbreviations, max 30k tokens)
- Every commit updates both project_status.py AND file_tree.md
- File tree updated whenever structure changes
