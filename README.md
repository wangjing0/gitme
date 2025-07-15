# GitMe

AI-powered git commit message generator using Claude.

## Features

- Analyzes git diff to generate meaningful commit messages
- Uses Claude AI for intelligent summarization
- Supports both staged and all changes
- JSON output format for file changes
- Direct commit creation with generated messages
- Configurable model selection

## Installation

```bash
pip install gitme
```

Or install from source:

```bash
git clone https://github.com/yourusername/gitme.git
cd gitme
pip install -e .
```

## Setup

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

Generate commit message for staged changes:
```bash
gitme
```

Generate commit message for all changes:
```bash
gitme --all
```

Output changes as JSON:
```bash
gitme --json
```

Create commit directly:
```bash
gitme --commit
```

Use a different Claude model:
```bash
gitme --model claude-3-opus-20240229
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