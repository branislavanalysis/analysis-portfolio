"""Shared PDF report helpers (reportlab) for the portfolio projects."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from PIL import Image as PILImage

NAVY = colors.HexColor("#1F4E5F")
TEAL = colors.HexColor("#3A9AB5")
LIGHT = colors.HexColor("#EEF4F6")
GREY = colors.HexColor("#595959")

ss = getSampleStyleSheet()
S = {
    "title": ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24,
                            textColor=NAVY, alignment=TA_LEFT, spaceAfter=4),
    "sub": ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=11, leading=14, textColor=GREY,
                          spaceAfter=2),
    "h1": ParagraphStyle("h1", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16,
                         textColor=NAVY, spaceBefore=10, spaceAfter=5, keepWithNext=1),
    "body": ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5, spaceAfter=5),
    "bullet": ParagraphStyle("bl", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5,
                             leftIndent=12, bulletIndent=2, spaceAfter=2),
    "cap": ParagraphStyle("c", parent=ss["Normal"], fontName="Helvetica-Oblique", fontSize=8, leading=10,
                          textColor=GREY, spaceAfter=8),
    "cell": ParagraphStyle("cell", parent=ss["Normal"], fontName="Helvetica", fontSize=8, leading=10),
    "cellb": ParagraphStyle("cellb", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=10,
                            textColor=colors.white),
    "box": ParagraphStyle("box", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5),
}
CONTENT_W = A4[0] - 36 * mm


def p(text, style="body"):
    return Paragraph(text, S[style])


def bullets(items):
    return [Paragraph(t, S["bullet"], bulletText="•") for t in items]


def fig(path, caption=None, width=CONTENT_W):
    w, h = PILImage.open(path).size
    img = Image(str(path), width=width, height=width * h / w)
    out = [img]
    if caption:
        out.append(p(caption, "cap"))
    return KeepTogether(out)


def table(df, col_widths=None, fmt=None, index=False, keep=True):
    fmt = fmt or {}
    d = df.reset_index() if index else df
    head = [Paragraph(str(c), S["cellb"]) for c in d.columns]
    rows = []
    for _, r in d.iterrows():
        row = []
        for c in d.columns:
            v = r[c]
            if c in fmt:
                v = fmt[c](v)
            elif isinstance(v, float):
                v = f"{v:,.4f}"
            row.append(Paragraph(str(v), S["cell"]))
        rows.append(row)
    t = Table([head] + rows, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return KeepTogether([t, Spacer(1, 6)]) if keep else t


def keybox(title, lines):
    content = [Paragraph(f"<b>{title}</b>", S["box"])] + [Paragraph("• " + l, S["box"]) for l in lines]
    t = Table([[content]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("LINEBEFORE", (0, 0), (0, -1), 3, TEAL),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return KeepTogether([t, Spacer(1, 8)])


def header_block(title, subtitle, meta):
    return [p(title, "title"), p(subtitle, "sub"), p(meta, "sub"), Spacer(1, 4),
            Table([[""]], colWidths=[CONTENT_W], rowHeights=[2],
                  style=[("BACKGROUND", (0, 0), (-1, -1), NAVY)]), Spacer(1, 8)]


def build(path, story, footer_text):
    def on_page(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GREY)
        c.drawString(18 * mm, 10 * mm, footer_text)
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {d.page}")
        c.restoreState()
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=18 * mm, title=footer_text, author="Branislav Petkovic")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


__all__ = ["p", "bullets", "fig", "table", "keybox", "header_block", "build", "PageBreak", "Spacer", "CONTENT_W", "mm"]
