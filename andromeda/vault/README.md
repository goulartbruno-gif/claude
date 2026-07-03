# Vault Andrômeda — Negócio

Vault Obsidian da **Andrômeda Coffee Co.** Este vault contém **apenas material de negócio**.
É a pasta que o MCP do Claude enxerga.

> ⚠️ **REGRA DE OURO — separação negócio × privado**
> Nada de família, saúde ou vida pessoal entra aqui. O vault privado vive **fora deste repositório**,
> em outra pasta na máquina, e o MCP **nunca** aponta pra ele. Se está em dúvida se algo é sensível,
> não coloca no vault de negócio.

## Regras de compliance (INEGOCIÁVEIS)

Todo conteúdo neste vault segue as regras do `CLAUDE.md` da raiz:

- Filha referida só como "minha/nossa filha" — **nome NUNCA** em nota que possa virar material público
- Vida pessoal da família **não é conteúdo**
- Identidade médica discreta — método sim, título não (CFM)
- **Notas sensoriais só de cupping conjunto Bruno + Jéssica — NUNCA inventadas.** Campo de sensorial
  em branco = ainda não foi cupado. Não preencher de cabeça.
- Produtor como colaborador, não fornecedor — não negociar preço de saca em nota pública
- "Região Vulcânica, São Paulo" — nunca "interior"
- Crescimento 100% orgânico / zero Ads
- Rótulo físico manda mais que qualquer documento — em conflito, **rótulo vence**
- Markup 5x inegociável (preço venda = 5× custo/kg rendimento útil)

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `00-Inbox/` | Captura rápida — tudo entra aqui antes de ser organizado |
| `10-Negócio/` | Plano estratégico, contexto consolidado, decisões |
| `20-Produtos/` | Uma nota por café (Dona Néia, Vésper, Nocturne, Jujubs, Zora) |
| `30-Torra/` | Perfis Cropster, curvas, notas de torra |
| `40-Clientes/` | B2C e B2B — só dados de negócio, sem PII sensível desnecessária |
| `50-Conteúdo/` | Ideias, rascunhos, calendário editorial |
| `60-Sessões/` | Registros das sessões de trabalho (11/06, 16/06, 19/06, ...) |
| `70-Operação/` | Shopify, Bling, frete, Pagar.me, integrações, automações |
| `99-Templates/` | Templates de nota (usar com o plugin Templates do Obsidian) |

## Segredos — proibido no vault

Tokens (Shopify, Bling, Pagar.me), documentos de KYC, credenciais: **nunca** neste vault.
O MCP lê tudo que está aqui — trate a pasta como se fosse pública.

## Configurando o MCP com escopo mínimo

Aponte o servidor MCP de Obsidian **para esta pasta** (`andromeda/vault/`), não pra raiz do repo
nem pro vault inteiro da máquina. Assim o Claude só enxerga o negócio.

**Se usar MCP de filesystem** (recomendado — mais simples e seguro): configure o path do vault como
`andromeda/vault`.

**Se usar o plugin "Local REST API" do Obsidian:** token forte, porta só em `127.0.0.1`, nunca exposta
na rede.

## Convenções de nota

- Frontmatter YAML no topo (`tags`, `status`, datas)
- Links internos com `[[Nota]]` pra conectar produto ↔ torra ↔ cliente ↔ conteúdo
- Tags: `#produto`, `#torra`, `#cliente`, `#b2b`, `#conteúdo`, `#sessão`, `#operação`, `#decisão`
