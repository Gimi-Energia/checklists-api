import tempfile

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from apps.checklistsC.models import ChecklistC
from setup.pdf.pdf_utils import (
    generate_header,
    subtitle_style,
    thirdtitle_style,
    translations,
)


def generate_pdf(instance):
    checklist = ChecklistC.objects.filter(id=instance.id).first()
    consumers_data = checklist.consumers.all()
    current_transformers_data = checklist.current_transformers.all()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    header_table = generate_header(instance.company, styles)
    elements = [header_table, Spacer(1, 0.25 * inch)]

    elements.append(Spacer(1, 0.25 * inch))

    title = f"Checklist Cabine Primária Convencional Multimedição ({instance.process_number} - {instance.item})"
    title_para = Paragraph(title, styles["Title"])
    elements.append(title_para)
    elements.append(Spacer(1, 0.2 * inch))

    details_cabin = [
        Paragraph(
            f"<b>Concessionária:</b> {instance.concessionaire if instance.concessionaire else instance.other_concessionarie}",
            styles["Normal"],
        ),
        Paragraph(f"<b>Tensão Primária:</b> {instance.primary_voltage} kV", styles["Normal"]),
        Paragraph(
            f"<b>Uso do painel:</b> {translations.get(instance.panel_usage)}", styles["Normal"]
        ),
        Paragraph(
            f"<b>Lado da Entrada dos Cabos:</b> {translations.get(instance.cable_side)}",
            styles["Normal"],
        ),
        Paragraph(f"<b>Demanda Contratada:</b> {instance.contracted_demand} kW", styles["Normal"]),
        Paragraph(
            f"<b>Quantidade de Medição/Consumidores:</b> {instance.measurements_consumers_quantity}",
            styles["Normal"],
        ),
    ]

    details_contractor = [
        Paragraph(f"<b>Nome do Contratante:</b> {instance.contractor_name}", styles["Normal"]),
        Paragraph(
            f"<b>Documento do Contratante:</b> {instance.contractor_document}", styles["Normal"]
        ),
        Paragraph(
            f"<b>Contato do Contratante:</b> {instance.contractor_contact}", styles["Normal"]
        ),
        Paragraph(f"<b>Telefone do Contratante:</b> {instance.contractor_phone}", styles["Normal"]),
        Paragraph(f"<b>Rua do Contratante:</b> {instance.contractor_street}", styles["Normal"]),
        Paragraph(f"<b>Número do Contratante:</b> {instance.contractor_number}", styles["Normal"]),
        Paragraph(
            f"<b>Bairro do Contratante:</b> {instance.contractor_neighborhood}", styles["Normal"]
        ),
        Paragraph(f"<b>Cidade do Contratante:</b> {instance.contractor_city}", styles["Normal"]),
        Paragraph(f"<b>Estado do Contratante:</b> {instance.contractor_state}", styles["Normal"]),
        Paragraph(
            f"<b>CEP/Coordenadas do Contratante:</b> {instance.contractor_zip_code}",
            styles["Normal"],
        ),
    ]

    if instance.contractor_complement:
        details_contractor.append(
            Paragraph(
                f"<b>Complemento do Contratante:</b> {instance.contractor_complement}",
                styles["Normal"],
            )
        )

    details_owner_work = [
        Paragraph(f"<b>Nome do Proprietário:</b> {instance.owner_name}", styles["Normal"]),
        Paragraph(f"<b>Documento do Proprietário:</b> {instance.owner_document}", styles["Normal"]),
        Paragraph(f"<b>Contato do Proprietário:</b> {instance.owner_contact}", styles["Normal"]),
        Paragraph(f"<b>Telefone do Proprietário:</b> {instance.owner_phone}", styles["Normal"]),
        Paragraph(f"<b>Rua da Obra:</b> {instance.work_street}", styles["Normal"]),
        Paragraph(f"<b>Número da Obra:</b> {instance.work_number}", styles["Normal"]),
        Paragraph(f"<b>Bairro da Obra:</b> {instance.work_neighborhood}", styles["Normal"]),
        Paragraph(f"<b>Cidade da Obra:</b> {instance.work_city}", styles["Normal"]),
        Paragraph(f"<b>Estado da Obra:</b> {instance.work_state}", styles["Normal"]),
        Paragraph(f"<b>CEP/Coordenadas da Obra:</b> {instance.work_zip_code}", styles["Normal"]),
    ]

    if instance.work_complement:
        details_owner_work.append(
            Paragraph(
                f"<b>Complemento da Obra:</b> {instance.work_complement}",
                styles["Normal"],
            )
        )

    details_fire_exit = [
        Paragraph(
            f"<b>Saída Exclusiva para Transformador de Incêndio:</b> {'Sim' if instance.fire_exit else 'Não'}",
            styles["Normal"],
        ),
    ]

    if instance.fire_exit:
        details_fire_exit.append(
            Paragraph(
                f"<b>Potência:</b> {instance.fire_transformer_power} kVA",
                styles["Normal"],
            )
        )
        details_fire_exit.append(
            Paragraph(
                f"<b>Demanda:</b> {instance.fire_transformer_demand} kW",
                styles["Normal"],
            )
        )
        details_fire_exit.append(
            Paragraph(
                f"<b>Impedância:</b> {instance.fire_transformer_impedance} %",
                styles["Normal"],
            )
        )
        details_fire_exit.append(
            Paragraph(
                f"<b>Tipo:</b> {translations.get(instance.fire_transformer_type)}",
                styles["Normal"],
            )
        )

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
            formatted_study_prediction = instance.study_prediction.strftime("%d/%m/%Y")
            details_study.append(
                Paragraph(
                    f"<b>Previsão do envio do estudo:</b> {formatted_study_prediction}",
                    styles["Normal"],
                )
            )
        else:
            details_study.append(
                Paragraph(
                    f"<b>Quantidade de Disjuntores:</b> {instance.breakers_quantity}",
                    styles["Normal"],
                )
            )

    subtitle_cabin = "Dados da Cabine Primária"
    subtitle_cabin_para = Paragraph(subtitle_cabin, subtitle_style)
    elements.append(subtitle_cabin_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_cabin:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_cabin = "Dados de Medição/Consumidores"
    subtitle_cabin_para = Paragraph(subtitle_cabin, subtitle_style)
    elements.append(subtitle_cabin_para)
    elements.append(Spacer(1, 0.2 * inch))

    for i, consumer_data in enumerate(consumers_data, start=1):
        subtitle_consumer = f"Medição/Consumidores {i}"
        subtitle_consumer_para = Paragraph(subtitle_consumer, thirdtitle_style)
        elements.append(subtitle_consumer_para)
        elements.append(Spacer(1, 0.15 * inch))

        paragraph = Paragraph(
            f"<b>Quantidade de Transformadores:</b> {consumer_data.transformers_quantity}",
            styles["Normal"],
        )
        elements.append(paragraph)
        elements.append(Spacer(1, 0.1 * inch))

        for j, transformer_data in enumerate(consumer_data.transformers.all(), start=1):
            subtitle_transformer = f"Transformador {j}"
            subtitle_transformer_para = Paragraph(subtitle_transformer, thirdtitle_style)
            elements.append(subtitle_transformer_para)
            elements.append(Spacer(1, 0.15 * inch))

            paragraph = Paragraph(
                f"<b>Potência:</b> {transformer_data.power} kVA",
                styles["Normal"],
            )
            elements.append(paragraph)
            paragraph = Paragraph(
                f"<b>Demanda:</b> {transformer_data.demand} kW",
                styles["Normal"],
            )
            elements.append(paragraph)
            paragraph = Paragraph(
                f"<b>Impedância:</b> {transformer_data.impedance} %",
                styles["Normal"],
            )
            elements.append(paragraph)
            paragraph = Paragraph(
                f"<b>Tipo:</b> {translations.get(transformer_data.type)}",
                styles["Normal"],
            )
            elements.append(paragraph)
            elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_fire_exit = "Dados Transformador de Incêndio"
    subtitle_fire_exit_para = Paragraph(subtitle_fire_exit, subtitle_style)
    elements.append(subtitle_fire_exit_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_fire_exit:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_study = "Dados do Estudo"
    subtitle_study_para = Paragraph(subtitle_study, subtitle_style)
    elements.append(subtitle_study_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_study:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    if not instance.gimi_study and instance.have_study:
        for i, current_transformer_data in enumerate(current_transformers_data, start=1):
            elements.append(Spacer(1, 0.2 * inch))
            subtitle_current_transformer = f"Definição do grupo {i} de TCs de proteção"
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

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_contractor = "Dados Contrato"
    subtitle_contractor_para = Paragraph(subtitle_contractor, subtitle_style)
    elements.append(subtitle_contractor_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_contractor:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_owner_work_ = "Dados Obra / Serviço"
    subtitle_owner_work__para = Paragraph(subtitle_owner_work_, subtitle_style)
    elements.append(subtitle_owner_work__para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_owner_work:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    document.build(elements)

    return filename
