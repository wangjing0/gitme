import click
import json
import os
from typing import Optional

from .git_diff import GitDiffAnalyzer
from .llm_client import CommitMessageGenerator
from .config import Config


@click.command()
@click.option('--staged-only', '-s', is_flag=True, default=True, help='Analyze only staged changes (default: True)')
@click.option('--all', '-a', is_flag=True, help='Analyze all changes including unstaged')
@click.option('--json', '-j', is_flag=True, help='Output file changes as JSON')
@click.option('--api-key', '-k', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
@click.option('--model', '-m', default='claude-3-haiku-20240307', help='Claude model to use')
@click.option('--commit', '-c', is_flag=True, help='Create commit with generated message')
def main(staged_only: bool, all: bool, json: bool, api_key: Optional[str], model: str, commit: bool):
    """GitMe - AI-powered git commit message generator using Claude"""
    
    analyzer = GitDiffAnalyzer()
    
    if not analyzer.git_available:
        click.echo("Error: Git is not available or not in a git repository", err=True)
        return
    
    # Determine which changes to analyze
    use_staged = not all
    
    # Get file changes
    file_changes = analyzer.get_file_changes(staged_only=use_staged)
    
    if not file_changes:
        click.echo("No changes detected to analyze")
        return
    
    if json:
        # Output JSON format of changes
        click.echo(analyzer.format_changes_json(staged_only=use_staged))
    else:
        # Generate commit message
        try:
            generator = CommitMessageGenerator(api_key=api_key)
            if model != 'claude-3-haiku-20240307':
                generator.model = model
            
            commit_message = generator.generate_commit_message(file_changes)
            
            click.echo(f"\nGenerated commit message:")
            click.echo(f"  {commit_message}\n")
            
            if commit:
                # Ask for confirmation before committing
                if click.confirm("Do you want to create a commit with this message?"):
                    import subprocess
                    try:
                        subprocess.run(["git", "commit", "-m", commit_message], check=True)
                        click.echo("Commit created successfully!")
                    except subprocess.CalledProcessError as e:
                        click.echo(f"Failed to create commit: {e}", err=True)
        
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            click.echo("Please set ANTHROPIC_API_KEY environment variable or use --api-key option", err=True)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    main()