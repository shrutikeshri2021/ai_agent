import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ---------------- JSON REPORT ----------------
def generate_report(results, logs=[]):
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)

    report = {
        "summary": {
            "total_steps": total,
            "passed": passed,
            "failed": total - passed,
            "pass_percentage": round((passed / total) * 100, 2) if total else 0
        },
        "steps": results,
        "logs": logs
    }


    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    os.makedirs(REPORT_DIR, exist_ok=True)

    json_path = os.path.join(REPORT_DIR, "test_report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=4)

    return report


# ---------------- PDF REPORT ----------------
def generate_pdf_report(report):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    os.makedirs(REPORT_DIR, exist_ok=True)

    pdf_path = os.path.join(REPORT_DIR, "test_report.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "AI Agent Web Test Report")
    y -= 30

    c.setFont("Helvetica", 12)
    summary = report["summary"]

    c.drawString(40, y, f"Total Steps: {summary['total_steps']}")
    y -= 20
    c.drawString(40, y, f"Passed: {summary['passed']}")
    y -= 20
    c.drawString(40, y, f"Failed: {summary['failed']}")
    y -= 20
    c.drawString(40, y, f"Pass Percentage: {summary['pass_percentage']}%")
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Step Details")
    y -= 20

    c.setFont("Helvetica", 11)
    for step in report["steps"]:
        # Check if we need a new page for text
        if y < 50:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 11)

        line = f"Step {step['step_no']}: {step['action']} → {step['target']} | {step['status']}"
        c.drawString(40, y, line)
        y -= 20

        # Embed Screenshot if available
        if "screenshot" in step and step["screenshot"]:
            screenshot_path = os.path.join(REPORT_DIR, "screenshots", step["screenshot"])
            if os.path.exists(screenshot_path):
                try:
                    img = ImageReader(screenshot_path)
                    img_width, img_height = img.getSize()
                    aspect = img_height / float(img_width)
                    
                    # Scale image to fit nicely
                    display_width = 400
                    display_height = display_width * aspect
                    
                    # Check if image fits on page
                    if y - display_height < 50:
                        c.showPage()
                        y = height - 40
                        c.setFont("Helvetica", 11)
                    
                    c.drawImage(img, 60, y - display_height, width=display_width, height=display_height)
                    y -= (display_height + 30) # Space after image
                except Exception as e:
                    print(f"Error adding image to PDF: {e}")

    c.save()
    return pdf_path
