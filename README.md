# DKS: Declarative Knowledge Schema

**A lightweight, structured context standard for Autonomous AI Agents.**

> "Markdown for Humans, YAML for Machines."

## Overview

**Declarative Knowledge Schema (DKS)** is a file format specification designed to bridge the gap between unstructured context files (like `AGENTS.md` or `.cursorrules`) and complex protocol-based solutions (like MCP).

DKS solves the **"Context Pollution"** problem. Instead of dumping all project knowledge into the AI's context window, DKS files use strict **metadata triggers** to load instructions only when they are relevant to the current task.

### Why DKS?

| Feature | AGENTS.md / Cursor Rules | Model Context Protocol (MCP) | **DKS (This Spec)** |
| --- | --- | --- | --- |
| **Format** | Plain Markdown | JSON-RPC Servers | **Markdown + YAML Frontmatter** |
| **Context Control** | Low (All or nothing) | High (Dynamic) | **High (Trigger-based)** |
| **Setup Difficulty** | Zero | High (Requires running server) | **Low (Static files)** |
| **Security** | Low (Prompt Injection risk) | High | **High (Signatures & Scoping)** |

---

## The Specification

A `.dks.md` file consists of two parts:

1. **Control Header (YAML Frontmatter):** Defines *when* and *how* to use this knowledge.
2. **Knowledge Body (Markdown):** The actual instructions for the LLM.

### File Structure Example

```markdown
---
dks_version: "1.0"
id: "backend-db-standards"
type: "knowledge_node"
security_level: "strict"
activation:
    on_files: ["src/db/**/*.go", "migrations/*.sql"]
    on_topics: ["sql", "database", "query optimization"]
validates_against: "./schemas/dks-header.schema.json"
---

# Database Standards

## 1. Connection Pooling

Never create a new connection per request. Use the global `PgPool`.

## 2. SQL Injection Prevention

* **DO NOT** use string concatenation for queries.
* **MUST** use parameterized queries (`$1`, `$2`).
```

## Directory Structure

We recommend placing DKS files either in a central `.dks/` directory or co-located with the code they govern.

```text
my-project/
├──.dks/
│   ├── global-security.dks.md   # Applies to the whole project
│   └── architecture.dks.md      # General architectural decisions
├── src/
│   ├── auth/
│   │   └── auth-flow.dks.md     # Specific rules for Auth module
│   └──...
├── schemas/
│   └── dks-header.schema.json   # Validation schema for CI/CD
└── README.md
```

## Tooling

This repository includes a reference **Linter** (`tools/dks-linter.py`).

### Installation & Usage

```bash
# Install dependencies
pip install pyyaml jsonschema

# Run linter on your project
python tools/dks-linter.py ./path/to/your/project
```

The linter ensures:

1. All `.dks.md` files have valid YAML frontmatter.
2. Required fields (`id`, `activation`) are present.
3. IDs are unique across the project.

## Integration with Agents

To use DKS with your AI agent (Claude, Cursor, Windsurf), you currently need a small "Context Loader" script (coming soon in v0.2) or simply reference the files manually. The goal is to build plugins for IDEs that automatically read the `activation` triggers.

## Rules examples (`examples/`)

 - [global-security.dks.md](examples/.dks/global-security.dks.md) - An example of a "strict" rule that should always be loaded or when working with sensitive files.
 - [api-style.dks.md](examples/src/backend/api-style.dks.md) - An example of a local rule. It doesn't pollute the context if the agent is working on the frontend, since triggers are configured only for the Go/Python backend.
