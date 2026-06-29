# Andrômeda Coffee Co. — Brainstorm Consolidado

**Data:** 29 de junho de 2026
**Status:** Entregue para aprovação

---

## A. Automação da Rotina

### Prioridade 1 — Eliminar atrito (custo zero, esta semana)

| # | Ação | Ferramenta | Status |
|---|------|-----------|--------|
| 1 | Template de proposta B2B | Google Docs / WhatsApp | A fazer |
| 2 | WhatsApp Business Catalog (4 cafés + variantes) | WhatsApp Business | A fazer |
| 3 | Mensagens rápidas pré-prontas (status pedido, Pix, prazo) | WhatsApp Business | A fazer |
| 4 | Planilha com COUNTIF (substituir contagem manual) | Google Sheets | Aguardando estrutura |

### Prioridade 2 — Automatizar com stack existente

| # | Ação | Ferramenta | Status |
|---|------|-----------|--------|
| 1 | Links recorrentes para Clube (quando lançar) | Pagar.me (conta PJ) | KYC pendente |
| 2 | Cálculo de frete no checkout | Frenet + Melhor Envio | Guia entregue |
| 3 | Agendamento de posts em lote (8/mês) | Meta Business Suite | A fazer |
| 4 | Automações pós-pedido | Shopify Flow | Passos entregues |

### Prioridade 3 — Delegar conforme caixa

| # | Ação | Quando |
|---|------|--------|
| 1 | Breno como quarto-bombeiro de torra | Picos de demanda |
| 2 | Freelancer empacotamento | Picos B2B (Dia dos Pais, fim de ano) |
| 3 | Edição de vídeo/foto | Primeiro candidato a terceirizar |

---

## B. Marketing — Ideias Founder Led (100% orgânico)

### Conteúdo recorrente

| Série | Formato | Frequência | Descrição |
|-------|---------|------------|-----------|
| "De onde vem" | Vídeo curto 30-60s | 2x/mês | Fazenda → grão → torra. Pedro Lotti como convidado natural |
| "O método" | Post carrossel | 2x/mês | Curva de torra, cupping, degasamento. Autoridade sem pedantismo |
| "Escuta ativa" | Post texto/stories | 1x/mês | Respostas reais dos clientes transformadas em conteúdo |
| "Backstage" | Stories/reels | Semanal | Torra do dia, embalagem, despacho. Sem roteiro |

### Ações pontuais

| Ação | Quando | Detalhes |
|------|--------|----------|
| Parceria Prosa na Cozinha (Chef Manu Zappa) | Agosto — Dia dos Pais | Conteúdo cruzado, kit especial |
| Sistema de indicação com papelaria | Ao lançar site | Cartão escrito à mão + cartão Jéssica |
| Caderno sensorial como pertencimento | Clube / super-indicadores | Exclusivo, não brinde |
| Unboxing como experiência | Contínuo | Incentivar clientes a compartilhar a abertura |

### SEO e posicionamento

- Vocabulário real dos clientes (da escuta ativa) nas descrições do site
- "Região Vulcânica de São Paulo" em toda comunicação (nunca "interior")
- Descrições de produto com termos buscados: "café especial", "microtorrefação", "café arábica", "café artesanal"

---

## C. História do Site — Narrativa em 3 Camadas

### Camada 1 — Emocional (as três mulheres)

| Nome | Papel | Café associado |
|------|-------|---------------|
| Dona Néia | A avó. Cozinha cheia, manhã sem pressa | Dona Néia (entrada, equilíbrio) |
| A Filha | Motivo de tudo que se faz com cuidado | Jujubs (raridade) |
| Andrômeda | Princesa etíope, galáxia, vastidão | A marca inteira |

### Camada 2 — Autoridade (o condutor)

- Bruno Goulart — médico de formação, torrefador por ofício
- Precisão como método: curva documentada, cupping em dupla, protocolo rigoroso
- "Não estou tentando ser o maior. Estou tentando ser consistente."
- Identidade médica discreta: método sim, título não

### Camada 3 — Produto (a curadoria)

- 100% Arábica, origem única, Região Vulcânica de SP
- Cada café tem função no repertório (entrada → curadoria → raridade)
- Janela de 90 dias — café que não gera ansiedade
- Produtor como colaborador, nunca fornecedor

---

## D. Site — Estrutura Entregue

### Arquivos

| Arquivo | Localização | Linhas |
|---------|------------|--------|
| index.html | src/site/index.html | 499 |
| style.css | src/site/style.css | 347 |
| app.js | src/site/app.js | 54 |

### Seções (11 blocos)

| # | Seção | Background | Conteúdo |
|---|-------|-----------|----------|
| 1 | Hero | Preto | "Café que aguenta o tempo" + CTA |
| 2 | Posicionamento | Cinza escuro | Frase-manifesto |
| 3 | Três Mulheres | Creme | Dona Néia / A Filha / Andrômeda |
| 4 | Cafés | Preto | 4 cards com ficha técnica + preço |
| 5 | Edições Limitadas | Creme | Zora (Laurina, off-catalog) |
| 6 | O Método | Cinza claro | 11–13 min / Cupping 100% / 90 dias |
| 7 | Sobre (Founder) | Creme | Bruno + princípios + dedicatória |
| 8 | B2B | Cinza claro | 3 kits + cafeterias |
| 9 | Entrega | Preto | Torrado sob encomenda / embalagem / atendimento |
| 10 | FAQ | Creme | 7 perguntas com accordion |
| 11 | Contato | Preto | Canais + Pedidos Especiais |

### Elementos extras

- **WhatsApp flutuante** — botão verde fixo no canto inferior direito
- **Selo de confiança** — barra pré-footer com 3 mensagens
- **Meta tags OG** — Open Graph para compartilhamento em redes sociais
- **Menu "Edições Limitadas"** — link direto na navegação
- **Animações de scroll** — fade-in nos cards ao entrar na viewport

### Design system

| Token | Valor | Uso |
|-------|-------|-----|
| --preto | #1A1A1A | Hero, seções escuras, footer |
| --dourado | #C8A96E | Destaques, títulos, CTAs |
| --dourado-claro | #E8D5A8 | Subtextos, badges |
| --creme | #FDF8F0 | Background principal |
| --cinza-claro | #F5F0E8 | Seções alternadas |
| --font-heading | Cormorant Garamond | Títulos (serif, elegante) |
| --font-body | Inter | Corpo (sans-serif, legível) |

---

## E. Lacunas Pendentes

| Item | Depende de | Urgência |
|------|-----------|----------|
| WhatsApp / e-mail / Instagram (URLs reais) | Bruno definir | Alta — site não publica sem |
| Fotos (hero, produtos, Bruno) | Sessão de fotos / acervo | Alta |
| Pagar.me KYC | Bruno enviar documentos | Alta — checkout não funciona sem |
| Frenet configurado | Bruno seguir o guia | Alta — sem frete no checkout |
| Conteúdo/pilares congelados desde 21/06 | Nova rota a definir | Média |
| Shopify Flow (3 workflows) | Bruno configurar no admin | Média |
| Curva de torra 11–13 min | Validar no cupping | Baixa |

---

## F. Shopify — Configurações Feitas

| Ação | Status |
|------|--------|
| Estoque de todos os 5 produtos setado em 10/variante | Feito |
| 20 variantes atualizadas (5 produtos × 4 moagens) | Feito |
| Produtos ainda em DRAFT (não publicados) | Mantido |

---

## G. Auditoria de Conformidade

| Regra | Status |
|-------|--------|
| Filha referida como "A Filha" / "nossa filha" (nome nunca usado publicamente) | OK |
| Identidade médica discreta (método sim, título não) | OK |
| Vida pessoal da família não é conteúdo | OK |
| Notas sensoriais do cupping conjunto (não inventadas) | OK |
| Produtor como colaborador, não fornecedor | OK |
| "Região Vulcânica, São Paulo" (nunca "interior") | OK |
| Crescimento 100% orgânico / sem tráfego pago | OK |
| Markup 5x preservado nos preços | OK |
| Sem secrets/credentials no código | OK |
| Arquivos < 500 linhas | OK |
