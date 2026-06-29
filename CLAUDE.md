# Ruflo — Claude Code Configuration

## Rules

- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary — prefer editing existing files
- NEVER create documentation files unless explicitly requested
- NEVER save working files or tests to root — use `/src`, `/tests`, `/docs`, `/config`, `/scripts`
- ALWAYS read a file before editing it
- NEVER commit secrets, credentials, or .env files
- NEVER add a `Co-Authored-By` trailer to user commits unless this project's `.claude/settings.json` has `attribution.commit` set (#2078). The Claude Code Bash tool may suggest one in its default commit-message template — ignore it. `Co-Authored-By` is semantic authorship attribution under git/GitHub convention; the tool is the facilitator, not a co-author.
- Keep files under 500 lines
- Validate input at system boundaries

## Agent Comms (SendMessage-First Coordination)

Named agents coordinate via `SendMessage`, not polling or shared state.

```
Lead (you) ←→ architect ←→ developer ←→ tester ←→ reviewer
              (named agents message each other directly)
```

### Spawning a Coordinated Team

```javascript
// ALL agents in ONE message, each knows WHO to message next
Agent({ prompt: "Research the codebase. SendMessage findings to 'architect'.",
  subagent_type: "researcher", name: "researcher", run_in_background: true })
Agent({ prompt: "Wait for 'researcher'. Design solution. SendMessage to 'coder'.",
  subagent_type: "system-architect", name: "architect", run_in_background: true })
Agent({ prompt: "Wait for 'architect'. Implement it. SendMessage to 'tester'.",
  subagent_type: "coder", name: "coder", run_in_background: true })
Agent({ prompt: "Wait for 'coder'. Write tests. SendMessage results to 'reviewer'.",
  subagent_type: "tester", name: "tester", run_in_background: true })
Agent({ prompt: "Wait for 'tester'. Review code quality and security.",
  subagent_type: "reviewer", name: "reviewer", run_in_background: true })

// Kick off the pipeline
SendMessage({ to: "researcher", summary: "Start", message: "[task context]" })
```

### Patterns

| Pattern | Flow | Use When |
|---------|------|----------|
| **Pipeline** | A → B → C → D | Sequential dependencies (feature dev) |
| **Fan-out** | Lead → A, B, C → Lead | Independent parallel work (research) |
| **Supervisor** | Lead ↔ workers | Ongoing coordination (complex refactor) |

### Rules

- ALWAYS name agents — `name: "role"` makes them addressable
- ALWAYS include comms instructions in prompts — who to message, what to send
- Spawn ALL agents in ONE message with `run_in_background: true`
- After spawning: STOP, tell user what's running, wait for results
- NEVER poll status — agents message back or complete automatically

## Swarm & Routing

### Config
- **Topology**: hierarchical-mesh (anti-drift)
- **Max Agents**: 15
- **Memory**: hybrid
- **HNSW**: Enabled
- **Neural**: Enabled

```bash
npx @claude-flow/cli@latest swarm init --topology hierarchical --max-agents 8 --strategy specialized
```

### Agent Routing

| Task | Agents | Topology |
|------|--------|----------|
| Bug Fix | researcher, coder, tester | hierarchical |
| Feature | architect, coder, tester, reviewer | hierarchical |
| Refactor | architect, coder, reviewer | hierarchical |
| Performance | perf-engineer, coder | hierarchical |
| Security | security-architect, auditor | hierarchical |

### When to Swarm
- **YES**: 3+ files, new features, cross-module refactoring, API changes, security, performance
- **NO**: single file edits, 1-2 line fixes, docs updates, config changes, questions

### 3-Tier Model Routing

| Tier | Handler | Use Cases |
|------|---------|-----------|
| 1 | Agent Booster (WASM) | Simple transforms — skip LLM, use Edit directly |
| 2 | Haiku | Simple tasks, low complexity |
| 3 | Sonnet/Opus | Architecture, security, complex reasoning |

## Memory & Learning

### Before Any Task
```bash
npx @claude-flow/cli@latest memory search --query "[task keywords]" --namespace patterns
npx @claude-flow/cli@latest hooks route --task "[task description]"
```

### After Success
```bash
npx @claude-flow/cli@latest memory store --namespace patterns --key "[name]" --value "[what worked]"
npx @claude-flow/cli@latest hooks post-task --task-id "[id]" --success true --store-results true
```

### MCP Tools (use `ToolSearch("keyword")` to discover)

| Category | Key Tools |
|----------|-----------|
| **Memory** | `memory_store`, `memory_search`, `memory_search_unified` |
| **Bridge** | `memory_import_claude`, `memory_bridge_status` |
| **Swarm** | `swarm_init`, `swarm_status`, `swarm_health` |
| **Agents** | `agent_spawn`, `agent_list`, `agent_status` |
| **Hooks** | `hooks_route`, `hooks_post-task`, `hooks_worker-dispatch` |
| **Security** | `aidefence_scan`, `aidefence_is_safe`, `aidefence_has_pii` |
| **Hive-Mind** | `hive-mind_init`, `hive-mind_consensus`, `hive-mind_spawn` |

### Background Workers

| Worker | When |
|--------|------|
| `audit` | After security changes |
| `optimize` | After performance work |
| `testgaps` | After adding features |
| `map` | Every 5+ file changes |
| `document` | After API changes |

```bash
npx @claude-flow/cli@latest hooks worker dispatch --trigger audit
```

## Agents

**Core**: `coder`, `reviewer`, `tester`, `planner`, `researcher`
**Architecture**: `system-architect`, `backend-dev`, `mobile-dev`
**Security**: `security-architect`, `security-auditor`
**Performance**: `performance-engineer`, `perf-analyzer`
**Coordination**: `hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`
**GitHub**: `pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`

Any string works as a custom agent type.

## Build & Test

- ALWAYS run tests after code changes
- ALWAYS verify build succeeds before committing

```bash
npm run build && npm test
```

## CLI Quick Reference

```bash
npx @claude-flow/cli@latest init --wizard           # Setup
npx @claude-flow/cli@latest swarm init --v3-mode     # Start swarm
npx @claude-flow/cli@latest memory search --query "" # Vector search
npx @claude-flow/cli@latest hooks route --task ""    # Route to agent
npx @claude-flow/cli@latest doctor --fix             # Diagnostics
npx @claude-flow/cli@latest security scan            # Security scan
npx @claude-flow/cli@latest performance benchmark    # Benchmarks
```

26 commands, 140+ subcommands. Use `--help` on any command for details.

## Setup

```bash
claude mcp add claude-flow -- npx -y ruflo@latest mcp start
npx ruflo@latest doctor --fix
```

> The background `daemon` is optional. It runs interval workers that each spawn
> a headless `claude` session, so it consumes tokens continuously. Start it only
> if you want those sweeps: `npx ruflo@latest daemon start` (self-stops after 12h
> by default; `--ttl 0` to disable, `daemon status --all` to audit running daemons).

**Agent tool** handles execution (agents, files, code, git). **MCP tools** handle coordination (swarm, memory, hooks). **CLI** is the same via Bash.

## Andrômeda Coffee Co.

Microtorrefação de cafés especiais. Fundadores: Bruno Goulart e Jéssica. ~60 clientes B2C, meta R$30k/mês em 12 meses. Founder Led Growth, 100% orgânico.

### Regras de privacidade e compliance (INEGOCIÁVEIS)

- Filha referida só como "minha/nossa filha" — nome NUNCA em material público
- Vida pessoal da família NÃO é conteúdo
- Identidade médica discreta — método sim, título não (CFM inegociável)
- Notas sensoriais só de cupping conjunto Bruno + Jéssica — NUNCA inventadas
- Produtor como colaborador, não fornecedor — não negociamos preço de saca
- "Região Vulcânica, São Paulo" — NUNCA "interior"
- Crescimento 100% orgânico / zero Ads — proibido por princípio
- Rótulo físico manda mais que qualquer documento — em caso de conflito, rótulo vence
- Markup 5x inegociável (preço venda = 5× custo/kg rendimento útil)

### Produtos

| Café | Posição | Gramatura | Preço |
|------|---------|-----------|-------|
| Dona Néia | Entrada | 250g | R$45 |
| Vésper | Intermediário | 250g | R$65 |
| Nocturne | Intermediário | 250g | R$65 |
| Jujubs | Raridade / microlote | 250g | R$130 |
| Zora (Laurina) | Off-catalog / peça rara proposital | 150g | R$90 |

### Stack técnico

- **Shopify** (produtos em DRAFT) → **Bling** (NF-e) → **Melhor Envio + Frenet** (frete) → **Pagar.me** (pagamento, KYC pendente)
- Frenet = bridge que puxa cotações do Melhor Envio pro checkout da Shopify
- Shopify Flow: pedido pago → tag, entregue → e-mail, estoque total produto < 3 → alerta de torra
- Estoque configurado: 10 unidades/variante (5 produtos × 4 moagens = 20 variantes)
- Cropster: perfis de torra

### Arquivos do repo

| Arquivo | Função |
|---------|--------|
| `andromeda/site/index.html` | Site completo — 11 seções, 499 linhas |
| `andromeda/site/style.css` | Design system preto/dourado/creme, responsivo, 347 linhas |
| `andromeda/site/app.js` | Menu mobile, FAQ accordion, scroll animations, 54 linhas |
| `andromeda/docs/Andromeda_Precificacao_B2B_Cafeteria.md` | Tabela de preços B2B — 4 grupos por volume, margens auditadas |
| `andromeda/docs/Andromeda_Orcamento_B2B.pdf` | PDF de orçamento gerado pelo script |
| `andromeda/docs/Guia_Integracao_Frenet_MelhorEnvio_Shopify.md` | Guia 8 passos para configurar frete no checkout |
| `andromeda/docs/Andromeda_Brainstorm_Automacao_Marketing_Site.md` | Brainstorm consolidado: automação, marketing, site, auditoria |
| `andromeda/docs/Andromeda_Respostas_Rapidas_WhatsApp.md` | Roteiro de respostas rápidas do WhatsApp Business — ciclo de venda + SAC, com guardrails de marca |
| `andromeda/scripts/gerar_orcamento_b2b.py` | Gerador de PDF de orçamento B2B (ReportLab) |
| `andromeda/pyproject.toml` | Projeto uv da Andrômeda — isolado do notebooklm-assistant (dep: reportlab) |
| `andromeda/uv.lock` | Lockfile do ambiente da Andrômeda (reprodutível com `uv sync`) |

### Ambiente Python da Andrômeda

`andromeda/` é um projeto **uv próprio**, isolado do `notebooklm-assistant` da raiz.
Rode os scripts sempre de dentro de `andromeda/` com `uv run` — ele resolve o venv
isolado sozinho, sem ativar nada manualmente:

```bash
cd andromeda
uv sync                              # recria .venv + deps a partir do uv.lock
uv run scripts/gerar_orcamento_b2b.py  # gera andromeda/docs/Andromeda_Orcamento_B2B.pdf
```

### Design system do site

| Token | Valor | Uso |
|-------|-------|-----|
| --preto | #1A1A1A | Hero, seções escuras, footer |
| --dourado | #C8A96E | Destaques, títulos, CTAs |
| --creme | #FDF8F0 | Background principal |
| --cinza-claro | #F5F0E8 | Seções alternadas |
| --font-heading | Cormorant Garamond | Títulos |
| --font-body | Inter | Corpo |

### Google Drive

- Pasta Andrômeda: `1ytf3VjXqBbPc-bTS-aIncomxWXAeP_0v`
- Documentos-chave: Plano Estratégico, Consolidação de Contexto, sessões (11/06, 16/06, 19/06), Pedidos, Calendário Julho

### Pendências estacionadas

- Reposicionamento de marca — parked, revisitar depois
- Conteúdo congelado desde 21/06 — nova rota a definir
- Pagar.me KYC — Bruno precisa enviar documentos
- WhatsApp Business Catalog — a montar quando Bruno pedir
- Planilhas COUNTIF — a montar conforme Bruno pedir tabelas
