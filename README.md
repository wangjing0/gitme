# GitMe

AI-powered git commit message generator.

## Features

- AI-Powered Analysis: Leverages Claude AI to analyze git diffs and generate contextually relevant commit messages
- Flexible Change Selection: Support for staged changes only or all modified files
- Message History: Track and review previously generated commit messages with the `show` command
- Multiple Output Formats: Export changes as JSON for integration with other tools
- One-Click Commits: Generate and commit with a single command using the `--commit` flag
- Model Flexibility: Choose between different Claude models (Haiku, Sonnet, Opus) based on your needs
- Smart Storage: Automatically saves generated messages for future reference
- Repository-Aware: Maintains separate message histories for different git repositories

## Installation

```bash
pip install gitme
```

Or install from source:

```bash
git clone https://github.com/wangjing0/gitme.git
cd gitme
pip install -e .
```

## Setup

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

### Generate Commit Messages

Generate commit message for staged changes:
```bash
gitme
gitme generate  # explicit subcommand
```

Generate commit message for all changes:
```bash
gitme --all
gitme -a
```

Output changes as JSON:
```bash
gitme --json
gitme -j
```

Create commit directly:
```bash
gitme --commit
gitme -c
```

Use a different Claude model (default is `claude-3-7-sonnet-20250219`):
```bash
gitme --model claude-opus-4-20250514
gitme -m claude-3-haiku-20240307
```

### View Message History

Show previously generated commit messages:
```bash
gitme show
```

Show last 5 messages:
```bash
gitme show --limit 5
gitme show -n 5
```

Show messages from all repositories:
```bash
gitme show --all-repos
gitme show -r
```

Clear message history for current repository:
```bash
gitme show --clear
```

Clear all message history:
```bash
gitme show --clear --all-repos
```

## Options

- `-s, --staged-only`: Analyze only staged changes (default)
- `-a, --all`: Analyze all changes including unstaged
- `-j, --json`: Output file changes as JSON
- `-k, --api-key`: Anthropic API key
- `-m, --model`: Claude model to use
- `-c, --commit`: Create commit with generated message

## Requirements

- Python 3.8+
- Git
- Anthropic API key

## License

MIT