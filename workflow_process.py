"""
10-STEP WORKFLOW PROCESS FOR STATELESS CLAUDE CODING
This file can be executed to verify the workflow at any time
"""

class WorkflowProcess:
    """
    Core workflow for maintaining project continuity across Claude sessions.
    Each step MUST be followed to ensure stateless coding works properly.
    """
    
    def __init__(self):
        self.steps = {
            1: {
                "name": "START SESSION",
                "action": "Read project_status.py",
                "command": "python project_status.py",
                "output": "Current state, completed tasks, pending tasks",
                "critical": True,
                "notes": "NEVER skip this. Execute to understand context."
            },
            2: {
                "name": "UNDERSTAND CONTEXT", 
                "action": "Read file_tree.md if it exists",
                "command": "cat file_tree.md",
                "output": "Complete file structure understanding",
                "critical": True,
                "notes": "Know what exists before making changes"
            },
            3: {
                "name": "WORK ON TASK",
                "action": "Complete the next pending task from project_status.py",
                "command": "# varies by task",
                "output": "New/modified files in repo",
                "critical": True,
                "notes": "Focus on ONE task at a time"
            },
            4: {
                "name": "UPDATE PROJECT STATUS",
                "action": "Move task from pending to completed in project_status.py",
                "command": "# edit project_status.py",
                "output": "Updated project_status.py",
                "critical": True,
                "notes": "Document what was done and commit SHA"
            },
            5: {
                "name": "CALCULATE TOKENS",
                "action": "Count tokens used this session",
                "command": "# Token counter in Claude UI",
                "output": "Token count update in project_status.py",
                "critical": True,
                "notes": "Update tokens_remaining field"
            },
            6: {
                "name": "UPDATE FILE TREE",
                "action": "Update file_tree.md with new/changed files",
                "command": "# edit file_tree.md",
                "output": "Current file structure documented",
                "critical": True,
                "notes": "Keep this in sync with repo"
            },
            7: {
                "name": "COMMIT WORK FILES",
                "action": "Commit task deliverables via GitHub API",
                "command": "# PUT to GitHub API",
                "output": "Commit SHA",
                "critical": True,
                "notes": "Commit actual work first"
            },
            8: {
                "name": "COMMIT STATUS FILES",
                "action": "Commit project_status.py and file_tree.md",
                "command": "# PUT to GitHub API",
                "output": "Commit SHA",
                "critical": True,
                "notes": "Always commit these together"
            },
            9: {
                "name": "CHECK TOKEN LIMIT",
                "action": "If tokens < 50,000, continue. Else, version and archive.",
                "command": "# if tokens_remaining < 50000: finalize()",
                "output": "Continue or archive decision",
                "critical": True,
                "notes": "Archive prevents status file bloat"
            },
            10: {
                "name": "REPORT STATUS",
                "action": "Tell user: task completed, tokens remaining, next step",
                "command": "print(f'✅ {task} | {tokens} tokens left | Next: {next_task}')",
                "output": "User confirmation message",
                "critical": True,
                "notes": "Always end with clear status report"
            }
        }
        
        self.archiving_process = {
            "trigger": "tokens_remaining < 50,000",
            "steps": [
                "Finalize current project_status.py (mark as complete session)",
                "Rename to project_status_v[N].py where N = next version number",
                "Move to management/ directory",
                "Add to .gitignore (keep repo lightweight)",
                "Create NEW project_status.py starting at v[N+1]",
                "Copy essential context (tech_stack, core decisions) to new version",
                "Reset tokens_remaining to session_start_tokens",
                "Commit both old (archived) and new (active) status files"
            ]
        }
        
    def verify_workflow(self):
        """Run this to verify the workflow is being followed"""
        print("=" * 80)
        print("10-STEP WORKFLOW PROCESS VERIFICATION")
        print("=" * 80)
        
        for step_num, step_data in self.steps.items():
            critical_marker = "🔴 CRITICAL" if step_data["critical"] else "⚪ Optional"
            print(f"\nSTEP {step_num}: {step_data['name']} {critical_marker}")
            print(f"   Action: {step_data['action']}")
            print(f"   Command: {step_data['command']}")
            print(f"   Output: {step_data['output']}")
            print(f"   Notes: {step_data['notes']}")
        
        print("\n" + "=" * 80)
        print("ARCHIVING PROCESS (When tokens < 50k)")
        print("=" * 80)
        print(f"Trigger: {self.archiving_process['trigger']}")
        for i, step in enumerate(self.archiving_process['steps'], 1):
            print(f"{i}. {step}")
        
        return True
    
    def get_step(self, step_number):
        """Get details for a specific step"""
        return self.steps.get(step_number, None)
    
    def check_critical_steps_complete(self, completed_steps):
        """Verify all critical steps were completed"""
        critical_steps = [num for num, data in self.steps.items() if data["critical"]]
        missing = [step for step in critical_steps if step not in completed_steps]
        
        if missing:
            print(f"⚠️  WARNING: Missing critical steps: {missing}")
            return False
        else:
            print("✅ All critical steps completed!")
            return True

class SessionHandoff:
    """
    Quick reference for starting a new Claude session
    """
    
    @staticmethod
    def start_new_session():
        """What to do when starting a new Claude session"""
        print("=" * 80)
        print("NEW SESSION START CHECKLIST")
        print("=" * 80)
        print("1. Read project_status.py immediately")
        print("2. Execute: python project_status.py")
        print("3. Read file_tree.md for structure context")
        print("4. Review pending_tasks list")
        print("5. Pick next task and begin work")
        print("=" * 80)
        
    @staticmethod
    def end_session():
        """What to do when ending a Claude session"""
        print("=" * 80)
        print("END SESSION CHECKLIST")
        print("=" * 80)
        print("✅ Updated project_status.py with completed tasks?")
        print("✅ Updated tokens_remaining count?")
        print("✅ Updated file_tree.md?")
        print("✅ Committed work files?")
        print("✅ Committed status files?")
        print("✅ Reported status to user?")
        print("=" * 80)

if __name__ == "__main__":
    # Verify the workflow
    workflow = WorkflowProcess()
    workflow.verify_workflow()
    
    print("\n\n")
    
    # Show session handoff instructions
    SessionHandoff.start_new_session()
