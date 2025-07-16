import os
import json
from typing import Dict, Optional
from anthropic import Anthropic


class CommitMessageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-7-sonnet-20250219"  # Using Sonnet 3.7 for best balance
    
    def generate_commit_message(self, file_changes: Dict[str, str]) -> str:
        if not file_changes:
            return "No changes to commit"
        
        prompt = self._create_prompt(file_changes)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text.strip()
        
        except Exception as e:
            print(f"Error generating commit message: {e}")
            return "Update files"
    
    def _create_prompt(self, file_changes: Dict[str, str]) -> str:
        changes_summary = []
        filenames = list(file_changes.keys())
        
        for filename, diff in file_changes.items():
            changes_summary.append(f"File: {filename}\nChanges:\n{diff[:1000]}...")  # Truncate long diffs
        
        prompt = f"""Analyze the following git diff and generate a concise, informative commit message.
The commit message should:
1. Have a summary line that starts with a verb in present tense (e.g., Add, Update, Fix, Remove)
2. The summary line should be under 50 characters
3. Include a blank line after the summary
4. List the changed files with bullet points
5. Keep the total message concise and informative

Example format:
Update user authentication logic

- Modified auth.py
- Updated config.json
- Fixed login.html

Git diff:
{chr(10).join(changes_summary)}

Generate only the commit message following the format above:"""
        
        return prompt