---
paths:
  - "tests/**"
  - "**/*.test.*"
  - "**/*.spec.*"
---

# Testing Standards

- Write tests verifying behavior, not implementation
- One assertion per test
- Prefer real dependencies over mocks
- Every bug fix includes regression test
- Run full suite before marking complete: `npm test`
