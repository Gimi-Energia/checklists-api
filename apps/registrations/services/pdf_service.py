import tempfile

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from utils.pdf import generate_header, subtitle_style


def generate_pdf(instance):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name

    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    header_table = generate_header(instance.company, styles)
    elements = [header_table, Spacer(1, 0.25 * inch)]

    elements.append(Spacer(1, 0.25 * inch))

    title = f"Checklist Dados Cadastrais ({instance.process_number})"
    title_para = Paragraph(title, styles["Title"])
    elements.append(title_para)
    elements.append(Spacer(1, 0.2 * inch))

    details_fat = [
        Paragraph(
            f"<b>De Acordo com Faturamento Antecipado:</b> {'Sim' if instance.advance_billing_agreed else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Documento para faturamento:</b> {instance.billing_document}", styles["Normal"]
        ),
        Paragraph(
            f"<b>Contribuinte de ICMS:</b> {'Sim' if instance.is_taxpayer else 'Não'}",
            styles["Normal"],
        ),
        Paragraph(
            f"<b>Destino do Material:</b> {instance.material_destination}",
            styles["Normal"],
        ),
        Paragraph(f"<b>Emails NF:</b> {instance.nf_email}", styles["Normal"]),
        Paragraph(f"<b>Condição de Pagamento:</b> {instance.payment_condition}", styles["Normal"]),
    ]

    if instance.lr_name and instance.lr_email and instance.lr_document and instance.lr_phone:
        lr_data = f"{instance.lr_name} | {instance.lr_email} | {instance.lr_document} | {instance.lr_phone}"
        details_fat.append(
            Paragraph(f"<b>Dados do Responsável Legal:</b> {lr_data}", styles["Normal"]),
        )
    if instance.billing_interval:
        details_fat.append(
            Paragraph(
                f"<b>Intervalo Faturamento NF:</b> Dia {instance.billing_interval}",
                styles["Normal"],
            )
        )
    if instance.minimum_value:
        details_fat.append(
            Paragraph(
                f"<b>Valor Mínimo de Faturamento:</b> {instance.minimum_value}", styles["Normal"]
            )
        )
    if instance.additional_data:
        details_fat.append(
            Paragraph(
                f"<b>Dados Adicionais OBS NF:</b> {instance.additional_data}", styles["Normal"]
            )
        )
    if instance.down_payment_date:
        formatted_down_payment_date = instance.down_payment_date.strftime("%d/%m/%Y")
        details_fat.append(
            Paragraph(
                f"<b>Data Pagamento Sinal:</b> {formatted_down_payment_date}", styles["Normal"]
            )
        )

    details_adress = [
        Paragraph(f"<b>Rua:</b> {instance.street}", styles["Normal"]),
        Paragraph(f"<b>Número:</b> {instance.number}", styles["Normal"]),
        Paragraph(f"<b>Bairro:</b> {instance.neighborhood}", styles["Normal"]),
        Paragraph(f"<b>Cidade:</b> {instance.city}", styles["Normal"]),
        Paragraph(f"<b>Estado:</b> {instance.state}", styles["Normal"]),
    ]

    if instance.zip_code:
        details_adress.append(
            Paragraph(f"<b>CEP:</b> {instance.zip_code}", styles["Normal"]),
        )

    if instance.latitude and instance.longitude:
        coordinates = f"{instance.latitude}, {instance.longitude}"
        details_adress.append(
            Paragraph(f"<b>Coordenadas:</b> {coordinates}", styles["Normal"]),
        )

    if instance.complement:
        details_adress.append(
            Paragraph(f"<b>Complemento:</b> {instance.complement}", styles["Normal"])
        )
    if instance.access_restriction:
        details_adress.append(
            Paragraph(
                f"<b>Restrição de Acesso:</b> {instance.access_restriction}", styles["Normal"]
            )
        )

    details_tr = [
        Paragraph(f"<b>Nome do Responsável Técnico:</b> {instance.tr_name}", styles["Normal"]),
        Paragraph(f"<b>Telefone do Responsável Técnico:</b> {instance.tr_phone}", styles["Normal"]),
        Paragraph(f"<b>Email do Responsável Técnico:</b> {instance.tr_email}", styles["Normal"]),
    ]

    if instance.tr_name_2:
        details_tr.append(
            Paragraph(
                f"<b>Nome do Responsável Técnico 2:</b> {instance.tr_name_2}", styles["Normal"]
            )
        )
    if instance.tr_phone_2:
        details_tr.append(
            Paragraph(
                f"<b>Telefone do Responsável Técnico 2:</b> {instance.tr_phone_2}", styles["Normal"]
            )
        )
    if instance.tr_email_2:
        details_tr.append(
            Paragraph(
                f"<b>Email do Responsável Técnico 2:</b> {instance.tr_email_2}", styles["Normal"]
            )
        )

    details_mr = [
        Paragraph(
            f"<b>Nome do Responsável pelo Material:</b> {instance.mr_name}", styles["Normal"]
        ),
        Paragraph(
            f"<b>Telefone do Responsável pelo Material:</b> {instance.mr_phone}", styles["Normal"]
        ),
        Paragraph(
            f"<b>Email do Responsável pelo Material:</b> {instance.mr_email}", styles["Normal"]
        ),
    ]

    if instance.mr_name_2:
        details_mr.append(
            Paragraph(
                f"<b>Nome do Responsável pelo Material 2:</b> {instance.mr_name_2}",
                styles["Normal"],
            )
        )
    if instance.mr_phone_2:
        details_mr.append(
            Paragraph(
                f"<b>Telefone do Responsável pelo Material 2:</b> {instance.mr_phone_2}",
                styles["Normal"],
            )
        )
    if instance.mr_email_2:
        details_mr.append(
            Paragraph(
                f"<b>Email do Responsável pelo Material 2:</b> {instance.mr_email_2}",
                styles["Normal"],
            )
        )

    details_fr = [
        Paragraph(f"<b>Nome do Responsável Financeiro:</b> {instance.fr_name}", styles["Normal"]),
        Paragraph(
            f"<b>Telefone do Responsável Financeiro:</b> {instance.fr_phone}", styles["Normal"]
        ),
        Paragraph(f"<b>Email do Responsável Financeiro:</b> {instance.fr_email}", styles["Normal"]),
    ]

    if instance.fr_name_2:
        details_fr.append(
            Paragraph(
                f"<b>Nome do Responsável Financeiro 2:</b> {instance.fr_name_2}", styles["Normal"]
            )
        )
    if instance.fr_phone_2:
        details_fr.append(
            Paragraph(
                f"<b>Telefone do Responsável Financeiro 2:</b> {instance.fr_phone_2}",
                styles["Normal"],
            )
        )
    if instance.fr_email_2:
        details_fr.append(
            Paragraph(
                f"<b>Email do Responsável Financeiro 2:</b> {instance.fr_email_2}", styles["Normal"]
            )
        )

    subtitle_fat = "Dados de Faturamento"
    subtitle_fat_para = Paragraph(subtitle_fat, subtitle_style)
    elements.append(subtitle_fat_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_fat:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_adress = "Endereço da Obra"
    subtitle_adress_para = Paragraph(subtitle_adress, subtitle_style)
    elements.append(subtitle_adress_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_adress:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_tr = "Responsável Técnico (recebimento/aprovação dos projetos)"
    subtitle_tr_para = Paragraph(subtitle_tr, subtitle_style)
    elements.append(subtitle_tr_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_tr:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_mr = "Responsável por Coletar ou Receber o Material"
    subtitle_mr_para = Paragraph(subtitle_mr, subtitle_style)
    elements.append(subtitle_mr_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_mr:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    subtitle_fr = "Responsável Financeiro"
    subtitle_fr_para = Paragraph(subtitle_fr, subtitle_style)
    elements.append(subtitle_fr_para)
    elements.append(Spacer(1, 0.2 * inch))

    for detail in details_fr:
        elements.append(detail)
        elements.append(Spacer(1, 0.1 * inch))

    document.build(elements)

    return filename
