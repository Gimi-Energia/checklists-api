import tempfile

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from utils.pdf import generate_header, translations, subtitle_style


def generate_pdf(instance):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    header_table = generate_header(instance.company, styles)
    elements = [header_table, Spacer(1, 0.25 * inch)]

    elements.append(Spacer(1, 0.25 * inch))

    title = f"Checklist Cabine Primária Simplificada Medição BT ({instance.process_number} - {instance.item})"
    title_para = Paragraph(title, styles["Title"])
    elements.append(title_para)
    elements.append(Spacer(1, 0.2 * inch))

    details_cabin = [
        Paragraph(
            f"<b>Concessionária:</b> {instance.concessionaire if instance.concessionaire else instance.other_concessionaire}",
            styles["Normal"],
        ),
        Paragraph(f"<b>Tensão Primária:</b> {instance.primary_voltage} kV", styles["Normal"]),
        Paragraph(f"<b>Tensão Secundária:</b> {instance.secondary_voltage} V", styles["Normal"]),
        Paragraph(
            f"<b>Uso do Painel:</b> {translations.get(instance.panel_usage)}", styles["Normal"]
        ),
        Paragraph(f"<b>Demanda Contratada:</b> {instance.contracted_demand} kW", styles["Normal"]),
        Paragraph(
            f"<b>Potência do Transformador:</b> {instance.transformer_power} kVA", styles["Normal"]
        ),
        Paragraph(
            f"<b>Tipo do Transformador:</b> {translations.get(instance.transformer_type)}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Definido o Fabricante do Transformador e Possui o Projeto:</b> {'Sim' if instance.manufacturer_project else 'Não'}",
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
    ]

    if instance.contractor_zip_code:
        details_contractor.append(
            Paragraph(
                f"<b>CEP do Contratante:</b> {instance.contractor_zip_code}", styles["Normal"]
            ),
        )

    if instance.contractor_latitude and instance.contractor_longitude:
        contractor_coordinates = f"{instance.contractor_latitude}, {instance.contractor_longitude}"
        details_contractor.append(
            Paragraph(
                f"<b>Coordenadas do Contratante:</b> {contractor_coordinates}", styles["Normal"]
            ),
        )

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
    ]

    if instance.work_zip_code:
        details_owner_work.append(
            Paragraph(f"<b>CEP da Obra:</b> {instance.work_zip_code}", styles["Normal"]),
        )

    if instance.work_latitude and instance.work_longitude:
        work_coordinates = f"{instance.work_latitude}, {instance.work_longitude}"
        details_owner_work.append(
            Paragraph(f"<b>Coordenadas da Obra:</b> {work_coordinates}", styles["Normal"]),
        )

    if instance.work_complement:
        details_owner_work.append(
            Paragraph(
                f"<b>Complemento da Obra:</b> {instance.work_complement}",
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
