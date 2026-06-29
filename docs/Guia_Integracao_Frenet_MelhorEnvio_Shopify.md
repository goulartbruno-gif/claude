# Guia de Integração: Frenet + Melhor Envio + Shopify

**Andrômeda Coffee Co.**
**Data:** 29 de junho de 2026

---

## Por que Frenet?

O Melhor Envio sozinho não calcula frete no checkout da Shopify. O **Frenet** é o intermediário que:
- Puxa as cotações do Melhor Envio (Correios, Jadlog, etc.)
- Exibe as opções de frete com preço e prazo no checkout
- Permite configurar regras de frete (grátis acima de X, adicional por região, etc.)

---

## Passo 1 — Criar conta no Frenet

1. Acesse: **app.frenet.com.br**
2. Clique em **Criar conta**
3. Preencha com os dados da **Cafeína Diária LTDA**:
   - CNPJ da empresa
   - E-mail: contato.andromedacoffee@gmail.com
   - CEP de origem (endereço da torrefação)
4. Confirme o e-mail de verificação

---

## Passo 2 — Conectar Melhor Envio ao Frenet

1. No painel do Frenet, vá em **Configurações → Transportadoras**
2. Clique em **Melhor Envio**
3. Clique em **Conectar**
4. Você será redirecionado para o Melhor Envio — faça login com sua conta
5. Autorize o Frenet a acessar sua conta
6. Após autorizar, volte ao Frenet — deve aparecer **"Conectado"**

### Transportadoras habilitadas via Melhor Envio:
- **Correios PAC** (econômico, 5-12 dias úteis)
- **Correios SEDEX** (expresso, 1-5 dias úteis)
- **Jadlog .Package** (alternativa econômica)
- **Jadlog .Com** (alternativa expressa)

> **Dica:** Deixe todas habilitadas. O cliente escolhe no checkout qual prefere.

---

## Passo 3 — Instalar Frenet na Shopify

1. No admin da Shopify: **Apps → Shopify App Store**
2. Pesquise **"Frenet"**
3. Clique em **"Frenet - Gateway de Frete"**
4. Clique **Instalar** → Confirmar permissões
5. O app vai pedir o **token de integração do Frenet**:
   - Volte ao painel do Frenet → **Configurações → Integrações**
   - Copie o **Token de acesso**
   - Cole no campo da Shopify
6. Clique **Salvar**

---

## Passo 4 — Configurar dados de origem

No painel do Frenet → **Configurações → Remetente**:

| Campo | Valor |
|-------|-------|
| Nome | Cafeína Diária LTDA |
| CEP | *(CEP da torrefação)* |
| Endereço | *(endereço completo)* |
| Documento | *(CNPJ)* |

> Esse CEP é o ponto de partida do cálculo de frete. Precisa ser o endereço de onde os pacotes saem.

---

## Passo 5 — Configurar dimensões dos produtos

Para o cálculo funcionar, cada produto precisa de **peso e dimensões** cadastrados na Shopify.

### Medidas dos pacotes Andrômeda (estimadas para 250g):

| Campo | Valor |
|-------|-------|
| Peso | 0.30 kg (250g café + embalagem) |
| Comprimento | 20 cm |
| Largura | 12 cm |
| Altura | 8 cm |

### Como cadastrar na Shopify:

1. Admin → **Produtos** → Selecione o produto (ex: Café Dona Néia)
2. Na seção **Envio**, marque **"Este é um produto físico"**
3. Preencha o **Peso**: 0.30 kg
4. Em cada **variante**, verifique se o peso está correto
5. Repita para todos os 5 produtos

> **Importante:** Se o peso não estiver cadastrado, o Frenet não consegue calcular o frete.

### Tabela de pesos por produto:

| Produto | Peso bruto (com embalagem) |
|---------|---------------------------|
| Dona Néia 250g | 0.30 kg |
| Vésper 250g | 0.30 kg |
| Nocturne 250g | 0.30 kg |
| Jujubs 250g | 0.30 kg |
| Zora 150g | 0.22 kg |

> Confira esses pesos na balança com um pacote embalado — o exato importa para o frete.

---

## Passo 6 — Testar no checkout

1. No admin da Shopify → **Loja online → Personalizar**
2. Clique em **Visualizar loja** (preview)
3. Adicione um produto ao carrinho
4. Vá até o checkout
5. Digite um CEP de teste (ex: 01001-000 São Paulo, ou 20040-020 Rio)
6. Verifique se aparecem as opções de frete com preço e prazo

### O que deve aparecer:

```
Correios PAC — R$ XX,XX (8 dias úteis)
Correios SEDEX — R$ XX,XX (3 dias úteis)
Jadlog .Package — R$ XX,XX (6 dias úteis)
```

> Se não aparecer nada, verifique:
> - Token do Frenet está correto na Shopify?
> - Melhor Envio está conectado no Frenet?
> - Os produtos têm peso cadastrado?

---

## Passo 7 — Regras opcionais

### Frete grátis acima de R$ X (recomendado para estimular ticket médio)

No Frenet → **Regras de frete → Adicionar regra**:
- Condição: Valor do pedido **maior que** R$ 250
- Ação: Frete grátis para **SEDEX** ou **PAC**

> **Sugestão:** Frete grátis PAC acima de R$ 250 (2 pacotes de Vésper + 1 Dona Néia já atinge). Incentiva o segundo pacote.

### Adicionar prazo extra de preparação

No Frenet → **Configurações → Prazos adicionais**:
- Adicionar **3 dias úteis** ao prazo de todas as transportadoras

> Isso reflete o tempo de torra + descanso + embalagem. O cliente vê "PAC — 11 dias úteis" ao invés de "8 dias úteis", evitando expectativa errada.

---

## Passo 8 — Gerar etiquetas pelo Melhor Envio

Quando um pedido chegar:

1. Acesse **app.melhorenvio.com.br**
2. Vá em **Envios → Novo envio**
3. Preencha destinatário (dados do pedido Shopify)
4. Selecione a transportadora que o cliente escolheu
5. Gere a **etiqueta**
6. Pague a etiqueta (saldo Melhor Envio ou cartão)
7. Imprima e cole no pacote
8. Leve ao ponto de postagem

> **Automação futura:** O app do Melhor Envio para Shopify pode importar pedidos direto. Mas o Frenet já resolve o cálculo no checkout — a geração de etiqueta pode ser manual por enquanto.

---

## Resumo do fluxo completo

```
Cliente acessa a loja
       ↓
Adiciona café ao carrinho
       ↓
No checkout, digita o CEP
       ↓
Frenet consulta Melhor Envio → exibe opções com preço/prazo
       ↓
Cliente escolhe (PAC / SEDEX / Jadlog)
       ↓
Cliente paga (Pagar.me)
       ↓
Bruno recebe pedido no Shopify
       ↓
Torra + descanso + embala
       ↓
Gera etiqueta no Melhor Envio
       ↓
Posta no Correios/Jadlog
       ↓
Shopify marca como "Enviado" + rastreio automático
```

---

## Checklist final

- [ ] Conta no Frenet criada
- [ ] Melhor Envio conectado ao Frenet
- [ ] App Frenet instalado na Shopify
- [ ] Token colado na configuração
- [ ] CEP de origem configurado
- [ ] Peso cadastrado em todos os 5 produtos (20 variantes)
- [ ] Checkout testado com CEP de São Paulo
- [ ] Checkout testado com CEP do Rio de Janeiro
- [ ] Checkout testado com CEP distante (ex: Manaus)
- [ ] Prazo adicional de 3 dias configurado
- [ ] (Opcional) Regra de frete grátis acima de R$ 250
