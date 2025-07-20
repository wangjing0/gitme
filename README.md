# A git commit message generator.

```bash
git add . && git commit -am "ugh... what did I do? what do I even say here?"
```
# ↓
```bash
gitme -c              # Use Anthropic Claude (default)
gitme -p openai -c    # Use OpenAI as model provider
```

```bash
gitme show
```

![gitme-cli](https://github.com/wangjing0/gitme/raw/main/commits.png)

## Features

- Analyzes git diffs to generate contextually relevant commit messages
- **Multiple AI Providers**: Choose between Anthropic Claude or OpenAI GPT models
- Operates only on local git repositories, NO remote interaction
- Detects untracked files and prompts to add them
- Supports staged changes only or all modified files
- Saves message history for review
- Direct commit with confirmation
- Selectable model options for both providers
- Repository-specific message storage

## Installation

Install from PyPI:

```bash
pip install gitme-cli
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/wangjing0/gitme.git
```

Or develop locally:

```bash
git clone https://github.com/wangjing0/gitme.git
cd gitme
pip install -e .
```

## Setup

### AI Provider Setup

Choose one or both providers:

**For Anthropic Claude (default):**
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
```

**For OpenAI GPT:**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Optional dependencies:**
```bash
# For OpenAI support
pip install openai
```


**Note:** All `gitme` commands must be run from within a git repository directory. If you're not in a git repository, you'll see an error message prompting you to run `git init`.

### Basic Usage

```bash
# Generate message for staged changes (default - uses Anthropic Claude)
gitme

# Generate message for all changes
gitme -a

# Generate message and commit
gitme -c
```

### Provider Selection

```bash
# Use OpenAI instead of Anthropic (default)
gitme -p openai

# Use OpenAI with specific model
gitme -p openai -m gpt-4

# Use Anthropic with specific model
gitme -m claude-3-haiku-20240307

# Combine with other options
gitme -p openai -c  # Use OpenAI and commit
```

### Untracked Files Handling

When you run `gitme`, it will automatically detect any untracked files in your repository and prompt you to add them to the staging area:

```bash
📁 Untracked files found:
    new_feature.py
    test_file.js
 Do you want to add these untracked files to the staging area? [y/N]:
```

- Choose **y** to add all untracked files to staging and include them in the commit message generation
- Choose **n** to proceed without the untracked files (they won't be included in the analysis)

### Message History

```bash
# Show previous messages
gitme show

# Show last 5 messages
gitme show -n 5

# Show from all repositories
gitme show -r

# Clear history
gitme show --clear
```

## Options

### Generate Options

- `-s, --staged`: Analyze only staged changes
- `-a, --all`: Analyze all changes (staged and unstaged)
- `-p, --provider`: Choose AI provider (`anthropic` or `openai`, default: anthropic)
- `-m, --model`: Model to use (provider-specific)
- `-c, --commit`: Create commit with generated message (uses `git commit -a -m "auto-generated message"`)

### Show Options

- `-n, --limit`: Number of messages to show
- `-r, --all-repos`: Show messages from all repositories
- `--clear`: Clear message history

### Available Models

**Anthropic Claude:**
- `claude-3-7-sonnet-20250219` (default)
- `claude-3-haiku-20240307`
- `claude-3-sonnet-20240229`

**OpenAI GPT:**
- `gpt-4o-mini` (default when using OpenAI)
- `gpt-4o`
- `gpt-4`
- `gpt-3.5-turbo`

### Advanced Examples

```bash
# Compare providers for the same changes
gitme -p anthropic -m claude-3-haiku-20240307  # Fast, cost-effective
gitme -p openai -m gpt-4o-mini                 # Alternative fast option

# High-quality commit messages
gitme -p openai -m gpt-4o                      # Premium OpenAI model
gitme -p anthropic                             # Default Claude Sonnet

# Quick commit workflows
gitme -p openai -c                             # OpenAI + auto-commit
gitme -p anthropic -a -c                      # Claude + all changes + commit
```

## Privacy & Security Notice

⚠️ **Important**: When using `gitme` or `gitme generate`, your code changes will be sent to the selected AI provider (Anthropic Claude or OpenAI GPT) for processing. The tool does NOT send your entire codebase - only the diff contents of changed files.

**Please exercise caution when using this tool:**
- Avoid using it with repositories containing sensitive information, credentials, or proprietary code
- Review your changes before running the command to ensure no sensitive data is included
- Consider using `.gitignore` to exclude sensitive files from git tracking
- Be aware that different providers have different data handling policies
- Both Anthropic and OpenAI have their own privacy policies and data retention practices

## Requirements

- Python 3.8+
- Git
- At least one AI provider API key:
  - Anthropic API key for Claude models
  - OpenAI API key for GPT models
- Optional: `openai` Python package for OpenAI support

## Contributing

Contributions are welcome! Please feel free to submit a pull request. @wangjing0

## License

MIT