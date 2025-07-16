import click
import json
import os
from typing import Optional
from datetime import datetime

from .git_diff import GitDiffAnalyzer
from .llm_client import CommitMessageGenerator
from .config import Config
from .storage import MessageStorage


@click.group()
def cli():
    """GitMe - AI-powered git commit message generator using Claude"""
    pass


@cli.command()
@click.option('--staged-only', '-s', is_flag=True, default=True, help='Analyze only staged changes (default: True)')
@click.option('--all', '-a', is_flag=True, help='Analyze all changes including unstaged')
@click.option('--json', '-j', is_flag=True, help='Output file changes as JSON')
@click.option('--api-key', '-k', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
@click.option('--model', '-m', default='claude-3-7-sonnet-20250219', help='Claude model to use')
@click.option('--commit', '-c', is_flag=True, help='Create commit with generated message')
def generate(staged_only: bool, all: bool, json: bool, api_key: Optional[str], model: str, commit: bool):
    """Generate a commit message for current changes"""
    
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
            generator.model = model
            
            commit_message = generator.generate_commit_message(file_changes)
            
            # Save the generated message
            storage = MessageStorage()
            repo_path = os.getcwd()
            storage.save_message(commit_message, repo_path, file_changes)
            
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


@cli.command()
@click.option('--limit', '-n', default=10, help='Number of messages to show (default: 10)')
@click.option('--all-repos', '-r', is_flag=True, help='Show messages from all repositories')
@click.option('--clear', is_flag=True, help='Clear message history')
def show(limit: int, all_repos: bool, clear: bool):
    """Show previously generated commit messages"""
    storage = MessageStorage()
    repo_path = os.getcwd() if not all_repos else None
    
    if clear:
        if click.confirm(f"Are you sure you want to clear {'all' if all_repos else 'this repository'} message history?"):
            storage.clear_messages(repo_path)
            click.echo("Message history cleared.")
        return
    
    messages = storage.get_messages(repo_path, limit)
    
    if not messages:
        click.echo("No previously generated messages found.")
        return
    
    for i, entry in enumerate(reversed(messages), 1):
        timestamp = datetime.fromisoformat(entry['timestamp'])
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        click.echo(f"\n{click.style(f'[{i}]', fg='cyan')} {click.style(formatted_time, fg='green')}")
        if all_repos:
            click.echo(f"    Repository: {entry['repo_path']}")
        click.echo(f"    Message: {entry['message']}")
        
        # Show file changes summary
        file_changes = entry.get('file_changes', {})
        if file_changes:
            files_count = len(file_changes)
            click.echo(f"    Files changed: {files_count}")




def main():
    """Entry point that provides backward compatibility"""
    import sys
    
    # If no arguments or help flag, show the group help
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h']):
        cli()
    # If the first argument is a known subcommand, use the group
    elif len(sys.argv) > 1 and sys.argv[1] in ['generate', 'show']:
        cli()
    # Otherwise, assume it's the old-style command and prepend 'generate'
    else:
        sys.argv.insert(1, 'generate')
        cli()


if __name__ == "__main__":
    main()