from fpdf import FPDF
from datetime import datetime
import os


def save_eval_report(results: list, evaluator_type: str = "auto", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_name = f"evaluation_report_{timestamp}.pdf"
    pdf_path = os.path.join(output_dir, pdf_name)

    font_path = os.path.join("resources", "fonts", "DejaVuSans.ttf")
    font_bold_path = os.path.join("resources", "fonts", "DejaVuSans-Bold.ttf")

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_bold_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(200, 10, txt="Evaluation Report", ln=1, align="C")

    for i, r in enumerate(results):
        pdf.ln(5)
        if pdf.get_y() > 250:
            pdf.add_page()

        pdf.set_font("DejaVu", "B", 12)
        pdf.multi_cell(0, 10, f"Case {i+1}:")

        pdf.set_font("DejaVu", "B", 12)
        pdf.multi_cell(0, 10, "Input:")
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 10, f"{list(r['input'].values())[0]}")

        if "reference" in r:
            pdf.set_font("DejaVu", "B", 12)
            pdf.multi_cell(0, 10, "Expected:")
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(0, 10, f"{r['reference']}")

        pdf.set_font("DejaVu", "B", 12)
        pdf.multi_cell(0, 10, "Output from model:")
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 10, f"{r['prediction']}")

        eval_data = r.get("eval", {})

        if isinstance(eval_data, dict):
            pdf.set_font("DejaVu", "B", 12)
            pdf.multi_cell(0, 10, "Evaluation:")
            pdf.set_font("DejaVu", "", 12)

            has_only_qa_eval_keys = evaluator_type == "qa_eval" or all(
                k in ["score", "value", "reasoning"] for k in eval_data.keys()
            )

            if evaluator_type == "qa_eval" or has_only_qa_eval_keys:
                score = str(eval_data.get("score", "")).strip().lower()
                status = "PASSED" if score in ["1", "pass", "passed"] else "FAILED"
                pdf.multi_cell(0, 10, f"QA Eval: {status}")

            elif evaluator_type == "criteria_eval":
                for key, val in eval_data.items():
                    if key in ["score", "value", "reasoning"]:
                        continue
                    label = key.upper()
                    val_str = str(val).strip().lower()
                    status = (
                        "PASSED" if val_str in ["1", "pass", "passed"] else "FAILED"
                    )
                    pdf.multi_cell(0, 10, f"{label}: {status}")

            else:
                for key, val in eval_data.items():
                    if key == "reasoning":
                        continue
                    label = key.upper()
                    val_str = str(val).strip().lower()
                    status = (
                        "PASSED" if val_str in ["1", "pass", "passed"] else "FAILED"
                    )
                    pdf.multi_cell(0, 10, f"{label}: {status}")

        if "reasoning" in eval_data:
            pdf.set_font("DejaVu", "B", 12)
            pdf.multi_cell(0, 10, "Reasoning:")
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(0, 10, eval_data["reasoning"])

    pdf.output(pdf_path)
    print(f"✅ Report generated: {pdf_path}")
