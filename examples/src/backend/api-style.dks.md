---
dks_version: "1.0"
id: "backend-api-standards"
type: "knowledge_node"
security_level: "strict"
activation:
    on_files: [ "src/backend/**/*.go", "src/backend/**/*.py" ]
    on_topics: [ "api", "rest", "endpoint" ]
---

# API Design Standards

| Component      | Standard                 | Example                           |
|----------------|--------------------------|-----------------------------------|
| **URL Naming** | Kebab-case, Plural nouns | `/api/v1/user-orders`             |
| **Methods**    | HTTP Verbs strictly      | `GET` for read, `POST` for create |
| **Auth**       | Bearer Token only        | `Authorization: Bearer <token>`   |

## Error Responses

All errors must return the standard RFC 7807 Problem Details object:json

```
{
  "type": "about:blank",
  "title": "Not Found",
  "status": 404
}
```
