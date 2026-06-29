"""
Gera Andromeda_Orcamento_B2B.pdf — apresentação de orçamento B2B
baseada no layout do catálogo B2B (sem preço), agora COM preços.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Table, TableStyle
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Andromeda_Orcamento_B2B.pdf")

PRETO = HexColor("#1a1a1a")
DOURADO = HexColor("#C8A96E")
DOURADO_CLARO = HexColor("#E8D5A8")
CINZA_ESCURO = HexColor("#2D2D2D")
CINZA_MEDIO = HexColor("#4A4A4A")
CINZA_CLARO = HexColor("#F5F0E8")
BRANCO = HexColor("#FFFFFF")
CREME = HexColor("#FDF8F0")

W, H = A4

PRODUTOS = [
    {
        "nome": "Dona Néia",
        "produtor": "Roberta Bazilli — Sítio Boa Vista do Engano",
        "origem": "Caconde, SP — Região Vulcânica",
        "variedade": "Catuaí Amarelo",
        "processo": "Cereja Descascada",
        "torra": "Média",
        "altitude": "1.100 m",
        "sensorial": "Perfil clássico e acolhedor. Caramelo e mel silvestre, com acidez delicada e agradável.",
        "preco_250g": 45,
        "preco_1kg": 180,
        "preco_2kg": 360,
    },
    {
        "nome": "Vésper",
        "produtor": "Pedro Lotti — Agrofloresta Córrego da Anta",
        "origem": "São Sebastião da Grama, SP",
        "variedade": "Aranãs",
        "processo": "Natural",
        "torra": "Média",
        "altitude": "1.283 m",
        "sensorial": "Café delicado, de acidez equilibrada e dulçor agradável. Notas de tangerina com um toque de damasco.",
        "preco_250g": 65,
        "preco_1kg": 260,
        "preco_2kg": 520,
    },
    {
        "nome": "Nocturne",
        "produtor": "Pedro Lotti — Agrofloresta Córrego da Anta",
        "origem": "São Sebastião da Grama, SP",
        "variedade": "Aranãs",
        "processo": "Natural",
        "torra": "Média",
        "altitude": "1.283 m",
        "sensorial": "Envolvente, de dulçor acentuado. Notas de frutas vermelhas maduras — ameixa e cereja.",
        "preco_250g": 65,
        "preco_1kg": 260,
        "preco_2kg": 520,
    },
    {
        "nome": "Jujubs",
        "produtor": "Pedro Lotti — Agrofloresta Córrego da Anta",
        "origem": "São Sebastião da Grama, SP",
        "variedade": "Gesha",
        "processo": "Natural",
        "torra": "Média",
        "altitude": "1.285 m",
        "sensorial": "Floral e frutado, com dulçor marcante e acidez sutil. A delicadeza de um Gesha em sua expressão mais refinada.",
        "preco_250g": 130,
        "preco_1kg": 520,
        "preco_2kg": 1040,
    },
]

GRUPOS = [
    ("A — Entrada", "5–10 kg", "0%"),
    ("B — Recorrente", "10–20 kg", "5%"),
    ("C — Prioritário", "20–35 kg", "8%"),
    ("D — Premium", "35+ kg", "10%"),
]

DESCONTOS = [0, 0.05, 0.08, 0.10]


def draw_header_bar(c, y, text, width=W):
    c.setFillColor(CINZA_ESCURO)
    c.rect(0, y - 2*mm, width, 10*mm, fill=1, stroke=0)
    c.setFillColor(DOURADO)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, y + 1*mm, text)


def draw_separator(c, y, width=W):
    c.setStrokeColor(DOURADO)
    c.setLineWidth(0.5)
    c.line(20*mm, y, width - 20*mm, y)


def fmt(val):
    if val >= 1000:
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {val:,.2f}".replace(".", ",")


def page_capa(c):
    c.setFillColor(PRETO)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(DOURADO)
    c.setLineWidth(1)
    c.setStrokeColor(DOURADO)
    c.rect(15*mm, 15*mm, W - 30*mm, H - 30*mm, fill=0, stroke=1)

    y = H - 80*mm
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(DOURADO)
    c.drawCentredString(W/2, y, "ANDRÔMEDA")

    y -= 14*mm
    c.setFont("Helvetica", 14)
    c.setFillColor(DOURADO_CLARO)
    c.drawCentredString(W/2, y, "C O F F E E   C O.")

    y -= 30*mm
    c.setStrokeColor(DOURADO)
    c.setLineWidth(0.5)
    c.line(W/2 - 40*mm, y, W/2 + 40*mm, y)

    y -= 20*mm
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(BRANCO)
    c.drawCentredString(W/2, y, "Orçamento B2B")

    y -= 12*mm
    c.setFont("Helvetica", 13)
    c.setFillColor(DOURADO_CLARO)
    c.drawCentredString(W/2, y, "Cafeterias & Parceiros Comerciais")

    y -= 40*mm
    c.setFont("Helvetica", 10)
    c.setFillColor(DOURADO_CLARO)
    c.drawCentredString(W/2, y, "100% Arábica  ·  Origem Única  ·  Microtorrefação Artesanal")

    y -= 8*mm
    c.drawCentredString(W/2, y, "Região Vulcânica, São Paulo")

    y = 35*mm
    c.setFont("Helvetica", 9)
    c.setFillColor(DOURADO_CLARO)
    c.drawCentredString(W/2, y, "Validade: 90 dias  ·  Junho 2026")

    y -= 6*mm
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, y, "Documento confidencial — uso exclusivo do destinatário")


def page_produtos(c):
    c.showPage()
    c.setFillColor(CREME)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    y = H - 25*mm
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(CINZA_ESCURO)
    c.drawString(20*mm, y, "Linha de Produtos")

    y -= 3*mm
    draw_separator(c, y)

    y -= 5*mm
    c.setFont("Helvetica", 9)
    c.setFillColor(CINZA_MEDIO)
    c.drawString(20*mm, y, "Todos: 100% Arábica · Origem Única · Torra Média · Validade 6 meses")

    y -= 15*mm

    for prod in PRODUTOS:
        if y < 60*mm:
            c.showPage()
            c.setFillColor(CREME)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            y = H - 25*mm

        c.setFillColor(CINZA_ESCURO)
        c.rect(18*mm, y - 3*mm, W - 36*mm, 12*mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(DOURADO)
        c.drawString(22*mm, y + 1*mm, prod["nome"])

        ref_250 = f'250g: {fmt(prod["preco_250g"])}'
        ref_1kg = f'1 kg: {fmt(prod["preco_1kg"])}'
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(DOURADO_CLARO)
        c.drawRightString(W - 22*mm, y + 1*mm, f"{ref_250}  |  {ref_1kg}")

        y -= 18*mm
        col1_x = 22*mm
        col2_x = W/2 + 5*mm

        specs_left = [
            ("Produtor", prod["produtor"]),
            ("Origem", prod["origem"]),
            ("Variedade", prod["variedade"]),
        ]
        specs_right = [
            ("Processo", prod["processo"]),
            ("Altitude", prod["altitude"]),
        ]

        ly = y
        for label, value in specs_left:
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(CINZA_ESCURO)
            c.drawString(col1_x, ly, f"{label}:")
            c.setFont("Helvetica", 8.5)
            c.setFillColor(CINZA_MEDIO)
            c.drawString(col1_x + 22*mm, ly, value)
            ly -= 4.5*mm

        ly2 = y
        for label, value in specs_right:
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(CINZA_ESCURO)
            c.drawString(col2_x, ly2, f"{label}:")
            c.setFont("Helvetica", 8.5)
            c.setFillColor(CINZA_MEDIO)
            c.drawString(col2_x + 20*mm, ly2, value)
            ly2 -= 4.5*mm

        y = min(ly, ly2) - 3*mm

        c.setFont("Helvetica-Oblique", 8.5)
        c.setFillColor(CINZA_MEDIO)
        max_w = W - 44*mm
        text_obj = c.beginText(col1_x, y)
        text_obj.setFont("Helvetica-Oblique", 8.5)
        text_obj.setFillColor(CINZA_MEDIO)

        words = prod["sensorial"].split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if c.stringWidth(test, "Helvetica-Oblique", 8.5) > max_w:
                text_obj.textLine(line)
                line = word
            else:
                line = test
        if line:
            text_obj.textLine(line)
        c.drawText(text_obj)

        y -= 6*mm * (1 + len(prod["sensorial"]) // 80)
        y -= 8*mm


def page_tabela_precos(c):
    c.showPage()
    c.setFillColor(CREME)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    y = H - 25*mm
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(CINZA_ESCURO)
    c.drawString(20*mm, y, "Tabela de Preços B2B")

    y -= 3*mm
    draw_separator(c, y)

    y -= 12*mm
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(CINZA_ESCURO)
    c.drawString(20*mm, y, "Grupos de Volume")

    y -= 8*mm

    grupo_data = [
        ["Grupo", "Pedido Total", "Desconto"],
    ]
    for g in GRUPOS:
        grupo_data.append(list(g))

    t = Table(grupo_data, colWidths=[55*mm, 45*mm, 30*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CINZA_ESCURO),
        ("TEXTCOLOR", (0, 0), (-1, 0), DOURADO),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BACKGROUND", (0, 1), (-1, -1), BRANCO),
        ("TEXTCOLOR", (0, 1), (-1, -1), CINZA_ESCURO),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, DOURADO),
        ("ROWHEIGHT", (0, 0), (-1, -1), 8*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
        ("TOPPADDING", (0, 0), (-1, -1), 2*mm),
    ]))

    tw, th = t.wrapOn(c, W, H)
    t.drawOn(c, 20*mm, y - th)
    y -= th + 12*mm

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(CINZA_ESCURO)
    c.drawString(20*mm, y, "Pedido mínimo: 5 kg  (~R$ 900)")

    y -= 18*mm

    formatos = [
        ("250g — Prateleira", "preco_250g", 1),
        ("1 kg — Cafeteria", "preco_1kg", 1),
        ("2 kg — Cafeteria", "preco_2kg", 1),
    ]

    for titulo, campo, mult in formatos:
        if y < 70*mm:
            c.showPage()
            c.setFillColor(CREME)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            y = H - 25*mm

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(CINZA_ESCURO)
        c.drawString(20*mm, y, titulo)
        y -= 8*mm

        header = ["Produto", "Grupo A\n(0%)", "Grupo B\n(-5%)", "Grupo C\n(-8%)", "Grupo D\n(-10%)"]
        data = [header]

        for prod in PRODUTOS:
            base = prod[campo]
            row = [prod["nome"]]
            for desc in DESCONTOS:
                val = base * (1 - desc)
                row.append(fmt(val))
            data.append(row)

        col_w = [35*mm] + [33*mm] * 4
        t = Table(data, colWidths=col_w)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), CINZA_ESCURO),
            ("TEXTCOLOR", (0, 0), (-1, 0), DOURADO),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), BRANCO),
            ("TEXTCOLOR", (0, 1), (-1, -1), CINZA_ESCURO),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, DOURADO),
            ("ROWHEIGHT", (0, 0), (-1, -1), 9*mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
            ("TOPPADDING", (0, 0), (-1, -1), 2*mm),
        ]))

        tw, th = t.wrapOn(c, W, H)
        t.drawOn(c, 20*mm, y - th)
        y -= th + 14*mm


def page_condicoes(c):
    c.showPage()
    c.setFillColor(CREME)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    y = H - 25*mm
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(CINZA_ESCURO)
    c.drawString(20*mm, y, "Condições Comerciais")

    y -= 3*mm
    draw_separator(c, y)

    y -= 15*mm

    condicoes = [
        ("Pedido Mínimo", "5 kg por pedido (~R$ 900)"),
        ("Pagamento", "Pix antecipado ou no ato da entrega"),
        ("Faturamento", "NF-e via Bling (Simples Nacional)"),
        ("Entrega", "A combinar — frete por conta do parceiro ou a negociar"),
        ("Prazo de Produção", "3–5 dias úteis após confirmação do pedido"),
        ("Validade", "Este orçamento é válido por 90 dias"),
        ("Formatos", "250g (prateleira) · 1 kg e 2 kg (uso na cafeteria)"),
        ("Personalização", "Mesma identidade visual em todos os formatos — sem retrabalho de rótulo"),
    ]

    for label, value in condicoes:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(CINZA_ESCURO)
        c.drawString(22*mm, y, label)

        y -= 6*mm
        c.setFont("Helvetica", 9.5)
        c.setFillColor(CINZA_MEDIO)
        c.drawString(22*mm, y, value)

        y -= 12*mm

    y -= 5*mm
    draw_separator(c, y)

    y -= 15*mm
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(CINZA_ESCURO)
    c.drawString(22*mm, y, "Vantagem para a Cafeteria")

    y -= 10*mm
    vantagens = [
        "Café especial de origem única — diferencial real no cardápio",
        "Embalagens de 1–2 kg com a mesma identidade visual das 250g",
        "Descontos progressivos conforme o volume cresce",
        "Produção artesanal sob demanda — frescor garantido",
        "Parceiro pode revender as 250g nas prateleiras com a mesma marca",
    ]

    for v in vantagens:
        c.setFont("Helvetica", 9)
        c.setFillColor(CINZA_MEDIO)
        c.drawString(25*mm, y, f"·  {v}")
        y -= 7*mm


def page_contato(c):
    c.showPage()
    c.setFillColor(PRETO)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setStrokeColor(DOURADO)
    c.setLineWidth(1)
    c.rect(15*mm, 15*mm, W - 30*mm, H - 30*mm, fill=0, stroke=1)

    y = H/2 + 30*mm

    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(DOURADO)
    c.drawCentredString(W/2, y, "ANDRÔMEDA")

    y -= 10*mm
    c.setFont("Helvetica", 12)
    c.setFillColor(DOURADO_CLARO)
    c.drawCentredString(W/2, y, "C O F F E E   C O.")

    y -= 20*mm
    c.setStrokeColor(DOURADO)
    c.setLineWidth(0.5)
    c.line(W/2 - 30*mm, y, W/2 + 30*mm, y)

    y -= 18*mm
    c.setFont("Helvetica", 11)
    c.setFillColor(BRANCO)
    c.drawCentredString(W/2, y, "Vamos conversar sobre sua próxima safra?")

    y -= 25*mm
    contatos = [
        "Bruno Goulart",
        "andromeda.coffee.co",
        "Região Vulcânica, São Paulo",
    ]

    for texto in contatos:
        c.setFont("Helvetica", 10)
        c.setFillColor(DOURADO_CLARO)
        c.drawCentredString(W/2, y, texto)
        y -= 8*mm

    y = 35*mm
    c.setFont("Helvetica", 8)
    c.setFillColor(DOURADO_CLARO)
    c.drawCentredString(W/2, y, "100% Arábica  ·  Origem Única  ·  Microtorrefação Artesanal")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle("Andrômeda Coffee Co. — Orçamento B2B")
    c.setAuthor("Andrômeda Coffee Co.")
    c.setSubject("Orçamento B2B — Cafeterias & Parceiros Comerciais")

    page_capa(c)
    page_produtos(c)
    page_tabela_precos(c)
    page_condicoes(c)
    page_contato(c)

    c.save()
    print(f"PDF gerado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
