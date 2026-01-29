---
dks_version: "1.0"
id: "global-security-001"
type: "rule_set"
security_level: "critical"
activation:
    on_files: [ "**/*" ]
    on_topics: [ "security", "auth", "keys" ]
---

# Critical Security Guidelines

## 1. Secrets Management

* **NEVER** output API keys, passwords, or tokens in the chat or logs.
* If you see a hardcoded secret in the code, your highest priority is to suggest moving it to `.env`.

## 2. Dependency Safety

* Do not suggest installing packages from unknown sources.
* Prefer standard libraries over 3rd party solutions for simple tasks.
