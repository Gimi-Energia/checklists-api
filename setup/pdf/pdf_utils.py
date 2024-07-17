import os

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

translations = {
    "Sheltered": "Abrigado",
    "Unsheltered": "Ao tempo",
    "Left": "Esquerda",
    "Right": "Direita",
    "Dried": "Seco",
    "Air": "Ar",
    "Oil": "Óleo",
    "Mineral Oil": "Óleo Mineral",
    "Vegetable Oil": "Óleo Vegetal",
    "Cables (Not Coupled)": "Cabos (Não Acoplados)",
    "Coupled Transformer": "Transformador Acoplado",
    "Flanged Transformer": "Transformador Flangeado",
    "Power": "Potência",
    "Impedance": "Impendância",
    "Demand": "Demanda",
    "Type": "Tipo",
}

subtitle_style = ParagraphStyle(
    name="Subtitle",
    fontSize=14,
    leading=16,
)

thirdtitle_style = ParagraphStyle(
    name="Thirdtitle",
    fontSize=12,
    leading=14,
)


def generate_header(company, styles):
    small_style = ParagraphStyle("SmallStyle", parent=styles["Normal"], fontSize=8, leading=10)

    company_info_dict = {
        "GIMI": [
            "IND MONTAGEM E INSTALACOES GIMI",
            "https://www.gimi.com.br/",
            "43.030.931/0001-45",
            "Estrada Portão Honda, 3530 - Jardim Revista",
            "08694-080",
            "(11) 4752-9900",
        ],
        "GBL": [
            "GIMI BONOMI LATIN AMERICA",
            "https://www.gimibonomi.com.br/",
            "41.517.310/0001-65",
            "Estrada Portão do Ronda, 3.500 (galpão unidades 1a e 1b) - Jardim Revista",
            "08694-080",
            "(11) 2500-4550",
        ],
        "GPB": [
            "GIMI POGLIANO BLINDOSBARRA",
            "https://www.gimipogliano.com.br/",
            "21.046.295/0001-07",
            "Estrada Portão do Ronda, 3.500 (galpão 2) - Jardim Revista",
            "08694-080",
            "(11) 4752-9900",
        ],
        "GIR": [
            "GIR-GIMI ITAIPU RENOVAVEIS",
            "https://www.grupogimi.com.br/",
            "50.791.922/0001-32",
            "Rua Maria de Lourdes Vessoni Porto Francischetti, 750 - Distrito Industrial II",
            "14900-000",
            "(16) 3263-9400",
        ],
    }

    company_details = company_info_dict.get(company.upper())
    city = "Itápolis" if company == "GIR" else "Suzano"

    company_details_content = "<br/>".join(
        [
            f"<b>{company_details[0]}</b>",
            f"<link href='{company_details[1]}'>{company_details[1]}</link>",
            f"CNPJ: {company_details[2]}",
            f"{company_details[3]}",
            f"{city} - SP - CEP: {company_details[4]}",
            f"Telefone: {company_details[5]}",
        ]
    )
    company_details_paragraph = Paragraph(company_details_content, small_style)

    logo_path = f"setup/images/logo_{company.lower()}.png"
    logo = (
        Image(logo_path, width=2 * inch, height=1 * inch)
        if os.path.exists(logo_path)
        else Spacer(1, 2 * inch)
    )

    header_data = [[logo, company_details_paragraph]]
    header_table = Table(header_data, colWidths=[2 * inch, 5 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (1, 0), (1, 0), 14),
            ]
        )
    )

    return header_table
