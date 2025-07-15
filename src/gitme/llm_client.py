import os
import json
from typing import Dict, Optional
from anthropic import Anthropic


class CommitMessageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass it as parameter.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"  # Using Haiku for cost efficiency
    
    def generate_commit_message(self, file_changes: Dict[str, str]) -> str:
        if not file_changes:
            return "No changes to commit"
        
        prompt = self._create_prompt(file_changes)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
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
        for filename, diff in file_changes.items():
            changes_summary.append(f"File: {filename}\nChanges:\n{diff[:1000]}...")  # Truncate long diffs
        
        prompt = f"""Analyze the following git diff and generate a concise, informative commit message.
The commit message should:
1. Start with a verb in present tense (e.g., Add, Update, Fix, Remove)
2. Be under 72 characters
3. Clearly describe what changed and why (if apparent)
4. Follow conventional commit format if applicable

Git diff:
{chr(10).join(changes_summary)}

Generate only the commit message, nothing else:"""
        
        return prompt