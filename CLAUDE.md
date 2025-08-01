# thingity

Terminal-based thing and todo management system with sophisticated context filtering and search capabilities.

## Project Overview

thingity is a Python CLI tool that provides:
- **Todo management** with context-based organisation and natural language date parsing
- **Note taking** ("things") with automatic file organisation and timestamping
- **Powerful search** across all content using ripgrep/ag with fzf integration
- **Git sync** integration for collaboration and backup

## Development Commands

### Setup
```bash
# Install dependencies
brew install fzf ripgrep the_silver_searcher bat
pipx install -e .

# Set up development environment
pip install pre-commit
pre-commit install
```

### Testing
```bash
# Watch tests during development
ptw

# Run specific test pattern
ptw -- -k task

# Run all linting checks
pre-commit run --all-files

# Integration testing in container
./isolation-test.sh
```

### CLI Commands
- `todo` - Create and manage todos with context filtering
- `thing` - Create individual notes/documents
- `things` - Search and navigate all content
- `things-search` - Backend search engine
- `things-with-modified` - Sort files by modification time

## Product Roadmap

### 1. Technical Goal - Search Backend Consolidation
**Priority: High | Effort: Medium**

Consolidate the dual search backend approach (ag.py and rg.py) into a single ripgrep-based implementation.

**Current Issue:** The system maintains two parallel search engines which creates maintenance overhead and complexity.

**Benefits:**
- Reduces code duplication and maintenance burden
- Ripgrep is more performant and actively maintained
- Simplifies the search abstraction layer
- Enables more consistent search behaviour across all commands

**Implementation Steps:**
- Deprecate ag.py module
- Enhance rg.py with any missing ag features
- Update all search callsites to use unified interface
- Remove ag dependencies from requirements

### 2. User Experience - Enhanced Todo Context Management
**Priority: High | Effort: Medium**

Improve the context filter system which currently uses complex string syntax (`-GEE,-PER:PER>FAM,DIY`).

**Current Issue:** The powerful context system has a steep learning curve and error-prone configuration syntax.

**Benefits:**
- Lower barrier to entry for new users
- Reduces configuration errors
- Makes the powerful context system more discoverable
- Improves user retention through better onboarding

**Implementation Steps:**
- Add `todo --configure` command with interactive prompts
- Create context preview and validation modes
- Add context hierarchy visualisation
- Implement context templates for common workflows

### 3. Product Growth - Collaborative Sharing Features
**Priority: Medium | Effort: High**

Add capability to share individual things or todo contexts with others, building on the existing git-sync foundation.

**Current Limitation:** Users can only share entire repositories, limiting collaborative use cases.

**Benefits:**
- Expands use cases to team collaboration
- Leverages existing git infrastructure
- Creates network effects for user acquisition
- Differentiates from basic note-taking tools

**Implementation Steps:**
- Add sharing commands that create filtered exports
- Implement access controls and permissions
- Add sharing metadata tracking
- Create shared context synchronisation

## Architecture Notes

### Key Components
- **Environment** - Configuration management with INI file support
- **Task** - Rich todo parsing with natural language date/time processing
- **Thing** - File organisation with automatic path normalisation
- **Search Infrastructure** - Abstract base with concrete implementations
- **ContextFilter** - Sophisticated todo categorisation system

### Technical Debt
- Mixed search backends create maintenance overhead
- Complex regex patterns reduce flexibility
- CLI modules could benefit from refactoring (todo.py: 352 lines)
- Limited error handling and logging

### Testing Strategy
- Unit tests using pytest with BDD-style feature files
- Integration tests using bats for CLI workflows
- Container-based isolation testing available

## Configuration

Edit `~/.config/thingity/thingity.ini`:
```ini
[DEFAULT]
MY_NOTES = my-notes
MY_DO = -GEE,-PER:PER>FAM,DIY
THINGS_DIR = /Users/me/projects/things
```
