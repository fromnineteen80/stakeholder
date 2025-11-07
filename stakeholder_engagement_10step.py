"""
HP 10-STEP STAKEHOLDER ENGAGEMENT PROCESS
Based on HP's proven framework for successful stakeholder relations
"""

class StakeholderEngagementProcess:
    """
    The complete HP 10-step process for stakeholder engagement.
    Used in HP's successful tariff advocacy campaign and other initiatives.
    """
    
    def __init__(self):
        self.phases = {
            "PURPOSE": {
                "description": "Define why stakeholder relations matter",
                "steps": [1, 2],
                "color": "#3E605A"  # Deep teal
            },
            "PLAN": {
                "description": "Identify and prioritize stakeholders",
                "steps": [3, 4, 5, 6],
                "color": "#46796F"  # Mid teal
            },
            "EXECUTE": {
                "description": "Launch and manage engagement",
                "steps": [7, 8],
                "color": "#FFE07C"  # Mustard
            },
            "CREATE VALUE": {
                "description": "Measure and optimize outcomes",
                "steps": [9, 10],
                "color": "#B86F56"  # Burnt orange
            }
        }
        
        self.steps = {
            1: {
                "phase": "PURPOSE",
                "name": "Business Goals",
                "description": "How stakeholder relations will support the organization's goals and objectives",
                "responsible": "ELT, Business Unit, Country Team",
                "outputs": [
                    "Defined business objectives",
                    "Stakeholder impact assessment",
                    "Success criteria"
                ],
                "key_questions": [
                    "What are our business goals?",
                    "How do stakeholders impact these goals?",
                    "What does success look like?"
                ]
            },
            2: {
                "phase": "PURPOSE",
                "name": "Issue Identification",
                "description": "Status of the relationship with stakeholders",
                "responsible": "ELT, CLT, Business Unit, Analyst Team, Stakeholder Relationship Managers",
                "outputs": [
                    "Current relationship status",
                    "Identified issues and opportunities",
                    "Risk assessment"
                ],
                "key_questions": [
                    "What is the current state of our relationships?",
                    "What issues need addressing?",
                    "What risks do we face?"
                ]
            },
            3: {
                "phase": "PLAN",
                "name": "Stakeholder Identification",
                "description": "Those with influence over business, message, credibility, and visibility",
                "responsible": "Business Unit, Country Team, CLT, Stakeholder Team",
                "outputs": [
                    "Complete stakeholder list",
                    "Influence mapping",
                    "Key decision-makers identified"
                ],
                "key_questions": [
                    "Who can influence our outcomes?",
                    "Who controls the message?",
                    "Who has credibility and visibility?"
                ]
            },
            4: {
                "phase": "PLAN",
                "name": "Stakeholder Prioritization",
                "description": "Those who pose greatest opportunity to impact the business or greatest risk to do harm",
                "responsible": "Business Unit, Country Team, CLT, Stakeholder Team",
                "outputs": [
                    "Prioritized stakeholder matrix (Influence x Interest)",
                    "High-value relationship list",
                    "Risk/opportunity classification"
                ],
                "key_questions": [
                    "Who has the most influence?",
                    "Who poses the greatest risk?",
                    "Who offers the greatest opportunity?"
                ]
            },
            5: {
                "phase": "PLAN",
                "name": "Landscape Analysis & Resource Identification",
                "description": "Mapping those prioritized stakeholders along with resources necessary to target and influence",
                "responsible": "CLT, Analyst Team, Stakeholder Team",
                "outputs": [
                    "Stakeholder landscape map",
                    "Resource requirements",
                    "Influence strategy per stakeholder"
                ],
                "key_questions": [
                    "What is the complete landscape?",
                    "What resources do we need?",
                    "How do we influence each stakeholder?"
                ]
            },
            6: {
                "phase": "PLAN",
                "name": "Internal Alignment & Governance",
                "description": "Relationship management and oversight for engagement to align strategy and outreach",
                "responsible": "Business Unit, Country Team, CLT, Stakeholder Team",
                "outputs": [
                    "Governance structure",
                    "Aligned internal strategy",
                    "Clear roles and responsibilities",
                    "Communication protocols"
                ],
                "key_questions": [
                    "How do we coordinate internally?",
                    "Who is responsible for what?",
                    "How do we maintain alignment?"
                ]
            },
            7: {
                "phase": "EXECUTE",
                "name": "Launch Campaign",
                "description": "Purposeful communication where stakeholders can consume and provide feedback",
                "responsible": "CLT, Stakeholder Team",
                "sub_activities": [
                    {
                        "activity": "Sustainable investment impacting targeted stakeholders",
                        "responsible": "CLT, Sustainability, Stakeholder Team"
                    },
                    {
                        "activity": "Refine campaign as needed",
                        "responsible": "CLT, Stakeholder Team → ELT, Business Unit, Country Team"
                    }
                ],
                "outputs": [
                    "Campaign launch plan",
                    "Communication materials",
                    "Feedback mechanisms",
                    "Refinement process"
                ],
                "key_questions": [
                    "How do we communicate our message?",
                    "How do stakeholders provide feedback?",
                    "How do we adapt based on feedback?"
                ]
            },
            8: {
                "phase": "EXECUTE",
                "name": "Targeted Engagement",
                "description": "Direct engagement with prioritized stakeholders",
                "responsible": "CLT, Executive Communications, Social Media Task Force, Stakeholder Team",
                "sub_activities": [
                    {
                        "activity": "Thought leadership from executives",
                        "responsible": "CLT, Executive Communications, Social Media Task Force, Stakeholder Team"
                    },
                    {
                        "activity": "Collaborate on business, message, or sustainable impact",
                        "responsible": "CLT, Stakeholder Team, Business Unit, Targeted Stakeholders"
                    },
                    {
                        "activity": "Resolve any identified issues",
                        "responsible": "CLT, Stakeholder Team, Targeted Stakeholders"
                    },
                    {
                        "activity": "Refine engagement as needed",
                        "responsible": "CLT, Stakeholder Team → ELT, Business Unit, Country Team"
                    }
                ],
                "outputs": [
                    "Executive engagement plan",
                    "Collaboration framework",
                    "Issue resolution process",
                    "Continuous improvement loop"
                ],
                "key_questions": [
                    "How do executives engage directly?",
                    "How do we collaborate on shared goals?",
                    "How do we resolve issues quickly?"
                ]
            },
            9: {
                "phase": "CREATE VALUE",
                "name": "For Organization Only",
                "description": "Measure outcomes: value creation, why only us, how could stakeholders earn or discover value in the future",
                "responsible": "ELT, Business Unit, Country Team, CLT, Stakeholder Team",
                "outputs": [
                    "Value measurement framework",
                    "Unique value proposition validation",
                    "Future value opportunities",
                    "ROI analysis"
                ],
                "key_questions": [
                    "What value did we create?",
                    "Why are we uniquely positioned?",
                    "What future value exists?"
                ]
            },
            10: {
                "phase": "CREATE VALUE",
                "name": "Shared Value for Organization & Target Stakeholder(s)",
                "description": "Collaborate on next steps together",
                "responsible": "ELT, Business Unit, Country Team, CLT, Stakeholder Team, Targeted Stakeholders",
                "outputs": [
                    "Shared value framework",
                    "Joint success metrics",
                    "Future collaboration roadmap",
                    "Long-term partnership strategy"
                ],
                "key_questions": [
                    "What value did stakeholders gain?",
                    "How do we both benefit?",
                    "What's next for our partnership?"
                ]
            }
        }
        
    def get_step(self, step_number):
        """Get details for a specific step"""
        return self.steps.get(step_number, None)
    
    def get_phase_steps(self, phase_name):
        """Get all steps for a specific phase"""
        phase = self.phases.get(phase_name.upper())
        if not phase:
            return None
        return [self.steps[num] for num in phase["steps"]]
    
    def print_process(self):
        """Print the complete 10-step process"""
        print("=" * 80)
        print("HP 10-STEP STAKEHOLDER ENGAGEMENT PROCESS")
        print("=" * 80)
        
        for phase_name, phase_data in self.phases.items():
            print(f"\n{'='*80}")
            print(f"{phase_name}: {phase_data['description']}")
            print(f"{'='*80}")
            
            for step_num in phase_data["steps"]:
                step = self.steps[step_num]
                print(f"\nSTEP {step_num}: {step['name']}")
                print(f"Description: {step['description']}")
                print(f"Responsible: {step['responsible']}")
                
                if 'sub_activities' in step:
                    print("Sub-activities:")
                    for activity in step['sub_activities']:
                        print(f"  • {activity['activity']}")
                        print(f"    Responsible: {activity['responsible']}")
                
                print(f"Key Questions:")
                for q in step['key_questions']:
                    print(f"  • {q}")
        
        print("\n" + "=" * 80)
    
    def get_step_checklist(self, step_number):
        """Get a checklist for implementing a specific step"""
        step = self.steps.get(step_number)
        if not step:
            return None
        
        checklist = {
            "step": step_number,
            "name": step["name"],
            "phase": step["phase"],
            "tasks": []
        }
        
        # Generate checklist items based on step
        if step_number == 1:
            checklist["tasks"] = [
                "Define business objectives",
                "Identify how stakeholders impact goals",
                "Establish success criteria",
                "Get ELT alignment"
            ]
        elif step_number == 2:
            checklist["tasks"] = [
                "Assess current stakeholder relationships",
                "Identify key issues",
                "Conduct risk assessment",
                "Document relationship status"
            ]
        elif step_number == 3:
            checklist["tasks"] = [
                "Create comprehensive stakeholder list",
                "Map influence and decision-making power",
                "Identify key decision-makers",
                "Document credibility and visibility"
            ]
        elif step_number == 4:
            checklist["tasks"] = [
                "Create Influence x Interest matrix",
                "Classify stakeholders by risk/opportunity",
                "Prioritize high-value relationships",
                "Define engagement strategy per tier"
            ]
        elif step_number == 5:
            checklist["tasks"] = [
                "Map complete stakeholder landscape",
                "Identify required resources (budget, time, people)",
                "Define influence strategy per stakeholder",
                "Create resource allocation plan"
            ]
        elif step_number == 6:
            checklist["tasks"] = [
                "Establish governance structure",
                "Align internal strategy across teams",
                "Define roles and responsibilities",
                "Create communication protocols"
            ]
        elif step_number == 7:
            checklist["tasks"] = [
                "Develop campaign messaging",
                "Create communication materials",
                "Establish feedback mechanisms",
                "Launch campaign",
                "Monitor and refine"
            ]
        elif step_number == 8:
            checklist["tasks"] = [
                "Schedule executive engagements",
                "Collaborate on shared goals",
                "Resolve identified issues",
                "Document interactions",
                "Refine approach continuously"
            ]
        elif step_number == 9:
            checklist["tasks"] = [
                "Measure value creation",
                "Validate unique value proposition",
                "Identify future value opportunities",
                "Calculate ROI"
            ]
        elif step_number == 10:
            checklist["tasks"] = [
                "Define shared value metrics",
                "Document stakeholder benefits",
                "Create future collaboration roadmap",
                "Build long-term partnership strategy"
            ]
        
        return checklist

# Example usage
if __name__ == "__main__":
    process = StakeholderEngagementProcess()
    process.print_process()
    
    print("\n\n" + "=" * 80)
    print("EXAMPLE: Step 4 Checklist")
    print("=" * 80)
    checklist = process.get_step_checklist(4)
    print(f"\nSTEP {checklist['step']}: {checklist['name']} ({checklist['phase']})")
    print("\nTasks:")
    for i, task in enumerate(checklist['tasks'], 1):
        print(f"{i}. {task}")
