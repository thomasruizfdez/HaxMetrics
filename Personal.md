# Personal AI Preferences

## Monorepo exploration with CodeGraph

When CodeGraph is available, use it before broad file exploration.

Default strategy:

1. Use CodeGraph first for architectural, flow, dependency or symbol-discovery questions.
2. Prefer `codegraph_explore` before using `Grep`, `Glob` or reading many files.
3. Use `codegraph_search` to locate symbols by name.
4. Use `codegraph_node` to inspect a specific symbol or file after narrowing the target.
5. Use `codegraph_callers` before changing public functions, use cases, domain behavior or shared utilities.
6. After CodeGraph narrows the relevant area, read only the directly relevant files and tests.
7. Do not scan unrelated packages or generated/build/vendor folders.
8. If CodeGraph results look stale, incomplete or contradictory, verify with direct file reads.

If investigating in Plan Mode, first produce a search strategy:

- likely package/module/bounded context
- symbols to inspect
- tests to inspect
- directories explicitly out of scope
- CodeGraph queries/tools to use
