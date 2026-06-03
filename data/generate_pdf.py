import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "hotel_policies.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0A1128'),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#D4AF37'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4A4E69'),
        spaceAfter=10
    )

    story = []
    
    story.append(Paragraph("THE GRAND ESTATE — HOTEL POLICIES", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("CHECK-IN / CHECK-OUT", heading_style))
    story.append(Paragraph("Check-in: 3:00 PM | Check-out: 12:00 PM. Early check-in and late check-out subject to availability. Charges may apply.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("PET POLICY", heading_style))
    story.append(Paragraph("Pets not permitted in guest rooms or public areas.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("SMOKING POLICY", heading_style))
    story.append(Paragraph("The Grand Estate is a smoke-free property. Designated smoking areas on Level B1 exterior.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("NOISE POLICY", heading_style))
    story.append(Paragraph("Quiet hours: 11:00 PM – 7:00 AM.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("CANCELLATION POLICY", heading_style))
    story.append(Paragraph("Free cancellation up to 48 hours before check-in.", body_style))
    
    doc.build(story)
    print(f"Generated PDF at: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
