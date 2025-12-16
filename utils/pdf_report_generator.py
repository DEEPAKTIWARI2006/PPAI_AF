from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def pass_percentage(passed, total):
    return round((passed / total) * 100, 2) if total else 0


# ---------------------------------------------------------
# Charts (DEFENSIVE)
# ---------------------------------------------------------
def create_overall_pie_chart(summary):
    if summary["total"] == 0:
        return None

    drawing = Drawing(300, 200)
    pie = Pie()
    pie.x = 50
    pie.y = 10
    pie.width = 150
    pie.height = 150

    pie.data = [
        summary.get("passed", 0),
        summary.get("failed", 0),
        summary.get("skipped", 0),
    ]
    pie.labels = ["Passed", "Failed", "Skipped"]

    pie.slices[0].fillColor = colors.green
    pie.slices[1].fillColor = colors.red
    pie.slices[2].fillColor = colors.orange

    drawing.add(pie)
    return drawing


def create_marker_bar_chart(summary):
    markers = summary.get("markers", {})

    if not markers:
        return None

    marker_names = list(markers.keys())
    passed = [markers[m].get("passed", 0) for m in marker_names]
    failed = [markers[m].get("failed", 0) for m in marker_names]

    # Guard against empty data
    if not marker_names or not any(passed + failed):
        return None

    drawing = Drawing(450, 250)
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 150
    chart.width = 350

    chart.data = [passed, failed]
    chart.categoryAxis.categoryNames = marker_names
    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = colors.green
    chart.bars[1].fillColor = colors.red

    drawing.add(chart)
    return drawing


# ---------------------------------------------------------
# Main PDF generator (SAFE)
# ---------------------------------------------------------
def generate_pdf_report(summary, output_path="reports/Test_Summary_Report.pdf"):
    """
    Generates a PDF test execution report.
    Safe against:
    - No tests collected
    - Empty markers
    - Partial failures
    """

    # -----------------------------
    # Hard guard: no tests collected
    # -----------------------------
    if not summary or summary.get("total", 0) == 0:
        print("[WARN] No test results available. Skipping PDF generation.")
        return

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # =====================================================
    # Executive Summary
    # =====================================================
    elements.append(Paragraph("<b>Test Execution Summary</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Total Tests: {summary['total']}", styles["Normal"]))
    elements.append(Paragraph(f"Passed: {summary['passed']}", styles["Normal"]))
    elements.append(Paragraph(f"Failed: {summary['failed']}", styles["Normal"]))
    elements.append(Paragraph(f"Skipped: {summary['skipped']}", styles["Normal"]))
    elements.append(
        Paragraph(
            f"Overall Pass Percentage: "
            f"{pass_percentage(summary['passed'], summary['total'])}%",
            styles["Normal"]
        )
    )

    # =====================================================
    # Overall Pie Chart
    # =====================================================
    pie_chart = create_overall_pie_chart(summary)
    if pie_chart:
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Overall Result Distribution", styles["Heading2"]))
        elements.append(pie_chart)

    elements.append(Spacer(1, 30))

    # =====================================================
    # Marker-wise Summary Table
    # =====================================================
    markers = summary.get("markers", {})

    if markers:
        elements.append(Paragraph("Results by Marker", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        table_data = [
            ["Marker", "Passed", "Failed", "Skipped", "Pass %", "Duration (s)"]
        ]

        for marker, data in markers.items():
            total = data["passed"] + data["failed"] + data["skipped"]
            table_data.append([
                marker,
                data["passed"],
                data["failed"],
                data["skipped"],
                f"{pass_percentage(data['passed'], total)}%",
                round(data.get("duration", 0), 2)
            ])

        table = Table(table_data, hAlign="LEFT")
        table.setStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
        ])

        elements.append(table)
        elements.append(Spacer(1, 30))

        # =====================================================
        # Marker-wise Bar Chart
        # =====================================================
        bar_chart = create_marker_bar_chart(summary)
        if bar_chart:
            elements.append(
                Paragraph("Marker-wise Pass / Fail Distribution", styles["Heading2"])
            )
            elements.append(bar_chart)
            elements.append(Spacer(1, 30))

    # =====================================================
    # Failure Categories
    # =====================================================
    if markers:
        elements.append(Paragraph("Failure Categories by Marker", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        for marker, data in markers.items():
            failures = data.get("failures", {})
            if not failures:
                continue

            elements.append(Paragraph(f"Marker: {marker}", styles["Heading3"]))

            failure_table = [["Failure Category", "Count"]]
            for category, count in failures.items():
                failure_table.append([category, count])

            table = Table(failure_table, hAlign="LEFT")
            table.setStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
            ])

            elements.append(table)
            elements.append(Spacer(1, 20))

    # =====================================================
    # Build PDF (FINAL)
    # =====================================================
    try:
        doc.build(elements)
        print(f"[INFO] PDF report generated at: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to generate PDF report: {e}")
