# A git commit message generator.

```bash
git add . && git commit -am "ugh... what did I do? what do I even say here?"
```
# ↓
```bash
gitme -c
```

```bash
gitme show
```

![gitme-cli](https://github.com/wangjing0/gitme/raw/main/commits.png)

## Features

- Analyzes git diffs to generate contextually relevant commit messages
- Operates only on local git repositories, NO remote interaction
- Detects untracked files and prompts to add them
- Supports staged changes only or all modified files
- Saves message history for review
- Direct commit with confirmation
- Selectable Claude model options
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

Set Anthropic API key if not already set in your environment:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```


**Note:** All `gitme` commands must be run from within a git repository directory. If you're not in a git repository, you'll see an error message prompting you to run `git init`.

### Basic Usage

```bash
# Generate message for staged changes (default)
# Will prompt to add any untracked files found
gitme

# Generate message for all changes
gitme -a

# Generate message and commit
gitme -c

# Use different model
gitme -m claude-3-haiku-20240307 -c
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
- `-m, --model`: Claude model to use
- `-c, --commit`: Create commit with generated message (uses `git commit -a -m "auto-generated message"`)

### Show Options

- `-n, --limit`: Number of messages to show
- `-r, --all-repos`: Show messages from all repositories
- `--clear`: Clear message history

## Privacy & Security Notice

⚠️ **Important**: When using `gitme` or `gitme generate`, the changes will be sent to Anthropic's Claude for processing. The tool does NOT send your entire codebase - only the diff contents of changed files.

**Please exercise caution when using this tool:**
- Avoid using it with repositories containing sensitive information, credentials, or proprietary code
- Review your changes before running the command to ensure no sensitive data is included
- Consider using `.gitignore` to exclude sensitive files from git tracking

## Requirements

- Python 3.8+
- Git
- Anthropic API key

## Contributing

Contributions are welcome! Please feel free to submit a pull request. @wangjing0

## License

MIT