# YNAB MCP Server

An MCP (Model Context Protocol) server for the [YNAB (You Need A Budget)](https://www.ynab.com/) API, built with [FastMCP](https://gofastmcp.com/).

This server automatically exposes all YNAB API endpoints as MCP tools, allowing AI assistants like Claude to interact with your YNAB budgets, accounts, transactions, and more.

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- A YNAB account with API access

## Setup

### Option 1: Install via uv tool (Recommended)

Install the YNAB MCP server as a standalone tool:

```bash
uv tool install ynab-mcp-server
```

This will install the `ynab-mcp-server` command globally, making it available from anywhere.

### Option 2: Install from Source

### 1. Clone the Repository

```bash
git clone https://github.com/rgarcia/ynab-mcp-server.git
cd ynab-mcp-server
```

### 2. Get Your YNAB API Token

1. Log in to your YNAB account at [app.ynab.com](https://app.ynab.com)
2. Go to **Account Settings** → **Developer Settings**
3. Click **New Token** under "Personal Access Tokens"
4. Give your token a name and click **Generate**
5. Copy the token (you won't be able to see it again!)

### 3. Install Dependencies (Source Installation Only)

If you installed from source, install the dependencies:

```bash
uv sync
```

## Running the Server

### With Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**If installed via `uv tool`:**

```json
{
  "mcpServers": {
    "ynab": {
      "command": "ynab-mcp-server",
      "args": [],
      "env": {
        "YNAB_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

**If installed from source:**

```json
{
  "mcpServers": {
    "ynab": {
      "command": "/absolute/path/to/this/project/.venv/bin/ynab-mcp-server",
      "args": [],
      "env": {
        "YNAB_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

### With Cursor

Add the following to your Cursor MCP settings (`~/.cursor/mcp.json` for global or `.cursor/mcp.json` in your project):

**If installed via `uv tool`:**

```json
{
  "mcpServers": {
    "ynab": {
      "command": "ynab-mcp-server",
      "args": [],
      "env": {
        "YNAB_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

**If installed from source:**

```json
{
  "mcpServers": {
    "ynab": {
      "command": "/absolute/path/to/this/project/.venv/bin/ynab-mcp-server",
      "args": [],
      "env": {
        "YNAB_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

### With OpenCode

Add the following to your OpenCode configuration file (`~/.config/opencode/opencode.json`):

**If installed via `uv tool`:**

```json
{
  "mcp": {
    "ynab": {
      "type": "local",
      "command": ["ynab-mcp-server"],
      "enabled": true,
      "environment": {
        "YNAB_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

**If installed from source:**

```json
{
  "mcp": {
    "ynab": {
      "type": "local",
      "command": ["/absolute/path/to/this/project/.venv/bin/ynab-mcp-server"],
      "enabled": true,
      "environment": {
        "YNAB_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

## Available Tools

The server automatically exposes all YNAB API endpoints as MCP tools. Here are some of the available operations:

### User

- `getUser` - Get authenticated user information

### Budgets

- `getBudgets` - List all budgets
- `getBudgetById` - Get a single budget with all related entities
- `getBudgetSettingsById` - Get budget settings

### Accounts

- `getAccounts` - List all accounts for a budget
- `getAccountById` - Get a single account
- `createAccount` - Create a new account

### Categories

- `getCategories` - List all categories for a budget
- `getCategoryById` - Get a single category
- `updateCategory` - Update a category
- `getMonthCategoryById` - Get a category for a specific month
- `updateMonthCategory` - Update a category for a specific month

### Transactions

- `getTransactions` - List transactions
- `getTransactionById` - Get a single transaction
- `createTransaction` - Create a new transaction
- `updateTransaction` - Update a transaction
- `deleteTransaction` - Delete a transaction
- `importTransactions` - Import transactions
- `getTransactionsByAccount` - List transactions for an account
- `getTransactionsByCategory` - List transactions for a category
- `getTransactionsByPayee` - List transactions for a payee

### Payees

- `getPayees` - List all payees
- `getPayeeById` - Get a single payee
- `updatePayee` - Update a payee

### Scheduled Transactions

- `getScheduledTransactions` - List scheduled transactions
- `getScheduledTransactionById` - Get a single scheduled transaction
- `createScheduledTransaction` - Create a new scheduled transaction
- `updateScheduledTransaction` - Update a scheduled transaction

### Months

- `getBudgetMonths` - List budget months
- `getBudgetMonth` - Get a single budget month

## Example Usage

Once connected, you can ask Claude things like:

- "Show me my YNAB budgets"
- "What's my current balance in my checking account?"
- "List my transactions from last week"
- "Create a transaction for $50 at the grocery store"
- "How much have I spent on dining out this month?"

## Creating Custom Skills for Your YNAB Workflow

YNAB workflows are personal. Everyone has their own conventions for handling transactions, categorizing expenses, and managing duplicates. You can create custom skills to encode your personal conventions so Claude can learn and apply them consistently.

Skills should be stored in `~/.skills/ynab/` on your local machine (not in this repository). Claude Desktop automatically discovers and loads skills from this directory when working with the YNAB MCP server.

### Step 1: Explore Your Budget

Start by asking Claude to do something useful with your YNAB data:

```
"Show me all my unapproved transactions"
"Help me categorize my uncategorized transactions"
"Find duplicate transactions in my budget"
```

Work through the task interactively. As you do, you'll naturally develop conventions. For example:

- "Venmo transactions always have a matching withdrawal in my checking account - I delete the Venmo one and keep the bank record"
- "Transactions from 'AMZN' should be categorized as 'Shopping' unless the memo mentions 'Kindle'"
- "Any transaction over $500 should be flagged for review"

### Step 2: Set Up the Skill Creator

First, copy the `skill-creator` skill from this repository to your local skills directory.

**If you installed from source**, run this from the repository root:

```bash
mkdir -p ~/.skills/ynab
cp -r .skills/skill-creator ~/.skills/ynab/
```

**If you installed via `uv tool`**, you can download the skill-creator from the repository:

```bash
mkdir -p ~/.skills/ynab
curl -L https://github.com/rgarcia/ynab-mcp-server/archive/refs/heads/main.tar.gz | tar -xz --strip=2 -C ~/.skills/ynab ynab-mcp-server-main/.skills/skill-creator
```

Or clone the repository temporarily and copy the skill:

```bash
mkdir -p ~/.skills/ynab
git clone --depth 1 https://github.com/rgarcia/ynab-mcp-server.git /tmp/ynab-mcp-server
cp -r /tmp/ynab-mcp-server/.skills/skill-creator ~/.skills/ynab/
rm -rf /tmp/ynab-mcp-server
```

### Step 3: Create a Skill to Encode Your Conventions

Once you've established patterns you want to reuse, create a skill to encode them. Ask Claude:

```
"Load the skill-creator skill and help me create a ynab skill that encodes
the conventions we just used for processing transactions"
```

The skill-creator will guide you through:

1. Identifying the reusable patterns from your workflow
2. Creating a SKILL.md file with your conventions
3. Structuring the skill for future use

### Step 4: Use Your Skills

Once created, your skills live in `~/.skills/ynab/` and Claude will automatically apply them when relevant. You can:

- Add more conventions as you discover them
- Share skills with others who have similar YNAB setups
- Create multiple skills for different workflows

### Available Skills

This repository includes:
- `.skills/skill-creator/` - Claude's official guide for creating new skills (copy to `~/.skills/ynab/skill-creator/` to use)

## Development

### Project Structure

```
.
├── pyproject.toml
├── README.md
├── uv.lock
└── src/
    └── ynab_mcp_server/
        ├── __init__.py
        └── server.py
```

### How It Works

This server uses FastMCP's `from_openapi()` method to automatically generate MCP tools from YNAB's OpenAPI specification. When the server starts, it:

1. Fetches the YNAB OpenAPI spec from `https://api.ynab.com/papi/open_api_spec.yaml`
2. Parses the specification
3. Creates an authenticated HTTP client with your API token
4. Generates MCP tools for each API endpoint

## Resources

- [YNAB API Documentation](https://api.ynab.com/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## License

MIT
