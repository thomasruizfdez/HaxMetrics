# Personal AI Preferences

## Monorepo exploration with CodeGraph

> **Nunca verifiques la existencia de `.codegraph/` con Glob, Bash o Read.**
> Los directorios ocultos no aparecen en Glob y pueden tener permisos restringidos.
> Llama directamente a `codegraph_explore` — si el índice no existe, la herramienta lo
> indica por sí sola. Omite CodeGraph solo cuando la herramienta misma reporte ausencia
> de índice.

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

## Selección rápida de herramienta CodeGraph

| Pregunta                                          | Herramienta          |
|---------------------------------------------------|----------------------|
| ¿Cómo funciona X? / ¿Dónde está X? / flujo A→B   | `codegraph_explore`  |
| Source + callers de un símbolo concreto           | `codegraph_node`     |
| ¿Qué llama a X? (antes de cambiar una API)        | `codegraph_callers`  |
| Búsqueda por nombre parcial de símbolo            | `codegraph_search`   |
