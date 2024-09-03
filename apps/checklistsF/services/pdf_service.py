import tempfile

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from utils.pdf import (
    generate_header,
    subtitle_style,
    thirdtitle_style,
    translations,
    units,
)


def generate_pdf(instance, transformers_data, current_transformers_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    header_table = generate_header(instance.company, styles)
    elements = [header_table, Spacer(1, 0.25 * inch)]

    elements.append(Spacer(1, 0.25 * inch))

    title = f"Checklist Subestações PMT ({instance.process_number} - {instance.item})"
    title_para = Paragraph(title, styles["Title"])
    elements.append(title_para)
    elements.append(Spacer(1, 0.2 * inch))

    details_cabin = [
        Paragraph(f"<b>Tensão Primária:</b> {instance.primary_voltage} kV", styles["Normal"]),
        Paragraph(
            f"<b>Uso do painel:</b> {translations.get(instance.panel_usage)}", styles["Normal"]
        ),
        Paragraph(
            f"<b>Lado da Entrada dos Cabos:</b> {translations.get(instance.cable_side)}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Quantidade de Transformadores:</b> {instance.transformers_quantity}",
            styles["Normal"],
        ),
    ]

    details_study = [
        Paragraph(
            f"<b>Estudo de fornecimento Gimi:</b> {'Sim' if instance.gimi_study else 'Não'}",
            styles["Normal"],
        ),
    ]

    if instance.gimi_study:
        details_study.append(
            Paragraph(
                f"<b>Trifásico (Icc3f):</b> {instance.icc3f}",
                styles["Normal"],
            ),
        )
        details_study.append(
            Paragraph(
                f"<b>Bifásico (Icc2f):</b> {instance.icc2f}",
                styles["Normal"],
            ),
        )
        details_study.append(
            Paragraph(
                f"<b>Fase e Terra Máximo (IccfTmáx):</b> {instance.iccftmax}",
                styles["Normal"],
            ),
        )
        details_study.append(
            Paragraph(
                f"<b>Fase e Terra Mínimo (IccfTmín):</b> {instance.iccftmin}",
                styles["Normal"],
            ),
        )
    else:
        details_study.append(
            Paragraph(
                f"<b>Já possui o estudo:</b> {'Sim' if instance.have_study else 'Não'}",
                styles["Normal"],
            ),
        )

        if not instance.have_study:
            if instance.study_prediction:
                formatted_study_prediction = instance.study_prediction.strftime("%d/%m/%Y")
                details_study.append(
                    Paragraph(
                        f"<b>Previsão do envio do estudo:</b> {formatted_study_prediction}",
                        styles["Normal"],
                    )
                )
        else:
            if instance.breakers_quantity > 0:
                details_study.append(
                    Paragraph(
                        f"<b>Quantidade de Disjuntores:</b> {instance.breakers_quantity}",
                        styles["Normal"],
                    )
                )

    subtitle_cabin = "Dados da Subestação"
    subtitle_cabin_para = Paragraph(subtitle_cabin, subtitle_style)
    elements.append(subtitle_cabin_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_cabin:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_cabin = "Dados dos Transformadores"
    subtitle_cabin_para = Paragraph(subtitle_cabin, subtitle_style)
    elements.append(subtitle_cabin_para)
    elements.append(Spacer(1, 0.2 * inch))

    for index, transformer_data in enumerate(transformers_data, start=1):
        subtitle_transformer = f"Transformador {index}"
        subtitle_transformer_para = Paragraph(subtitle_transformer, thirdtitle_style)
        elements.append(subtitle_transformer_para)
        elements.append(Spacer(1, 0.15 * inch))

        for key, value in transformer_data.items():
            paragraph = Paragraph(
                f"<b>{translations.get(key.capitalize())}:</b> {translations.get(value, value)} {units.get(key.capitalize(), '')}",
                styles["Normal"],
            )
            elements.append(paragraph)
            elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_no_breakers = "Dados do Estudo"
    subtitle_study_para = Paragraph(subtitle_no_breakers, subtitle_style)
    elements.append(subtitle_study_para)
    elements.append(Spacer(1, 0.2 * inch))

    if instance.have_study or instance.breakers_quantity > 0:
        for detail in details_study:
            elements.append(detail)
            elements.append(Spacer(1, 0.1 * inch))

        if not instance.gimi_study and instance.have_study:
            for index, current_transformer_data in enumerate(current_transformers_data, start=1):
                elements.append(Spacer(1, 0.2 * inch))
                subtitle_current_transformer = f"Definição do grupo {index} de TCs de proteção"
                subtitle_current_transformer_para = Paragraph(
                    subtitle_current_transformer, thirdtitle_style
                )
                elements.append(subtitle_current_transformer_para)
                elements.append(Spacer(1, 0.15 * inch))

                for key, value in current_transformer_data.items():
                    paragraph = Paragraph(
                        f"<b>{translations.get(key.capitalize())}:</b> {value}",
                        styles["Normal"],
                    )
                    elements.append(paragraph)
                    elements.append(Spacer(1, 0.1 * inch))
    else:
        subtitle_no_breakers = "Sem disjuntores"
        subtitle_study_para = Paragraph(subtitle_no_breakers, thirdtitle_style)
        elements.append(subtitle_study_para)

    document.build(elements)

    return filename
