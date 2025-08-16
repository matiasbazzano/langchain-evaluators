from fpdf import FPDF
from datetime import datetime
import os
from typing import Any, Dict, List, Tuple


def _ensure_fonts(pdf: FPDF, font_path: str, font_bold_path: str) -> None:
    if os.path.exists(font_path) and os.path.exists(font_bold_path):
        try:
            pdf.add_font("DejaVu", "", font_path, uni=True)
            pdf.add_font("DejaVu", "B", font_bold_path, uni=True)
        except Exception:
            pass


def _to_pass(value: Any) -> bool:
    if isinstance(value, (bool, int, float)):
        return bool(value)
    s = str(value).strip().lower()
    return s in {
        "y",
        "yes",
        "true",
        "1",
        "pass",
        "passed",
        "met",
        "meets",
        "correct",
        "ok",
    }


def _detect_evaluator_type(eval_data: Dict[str, Any]) -> str:
    if any(
        k in eval_data
        for k in (
            "criteria",
            "score_dict",
            "clarity",
            "conciseness",
            "relevance",
            "coherence",
        )
    ):
        return "criteria_eval"
    if any(k in eval_data for k in ("correct", "score", "value")):
        return "qa_eval"
    return "qa_eval"


def _extract_criteria(eval_data: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(eval_data.get("criteria"), dict):
        return eval_data["criteria"]
    if isinstance(eval_data.get("score_dict"), dict):
        return eval_data["score_dict"]

    crits = {}
    for k in (
        "clarity",
        "conciseness",
        "relevance",
        "coherence",
        "helpfulness",
        "correctness",
    ):
        if k in eval_data:
            crits[k] = eval_data[k]
    return crits


def _draw_header(pdf: FPDF, title: str) -> None:
    pdf.set_font("DejaVu" if "DejaVu" in pdf.fonts else "Arial", "B", 18)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(2)
    pdf.set_font("DejaVu" if "DejaVu" in pdf.fonts else "Arial", "", 11)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"Generated: {ts}", ln=True)
    pdf.ln(4)


def _draw_item_block(
    pdf: FPDF,
    index: int,
    input_text: str,
    prediction: str,
    reference: Any,
    eval_data: Dict[str, Any],
    evaluator_type: str,
) -> Tuple[int, int]:
    base_font = "DejaVu" if "DejaVu" in pdf.fonts else "Arial"

    pdf.set_font(base_font, "B", 13)
    pdf.cell(0, 8, f"Example #{index}", ln=True)
    pdf.ln(1)

    pdf.set_font(base_font, "B", 12)
    pdf.cell(0, 7, "Input:", ln=True)
    pdf.set_font(base_font, "", 12)
    pdf.multi_cell(0, 6, _normalize_input_text(input_text))
    pdf.ln(1)

    if reference is not None and str(reference).strip():
        pdf.set_font(base_font, "B", 12)
        pdf.cell(0, 7, "Reference:", ln=True)
        pdf.set_font(base_font, "", 12)
        pdf.multi_cell(0, 6, str(reference))
        pdf.ln(1)

    pdf.set_font(base_font, "B", 12)
    pdf.cell(0, 7, "Prediction:", ln=True)
    pdf.set_font(base_font, "", 12)
    pdf.multi_cell(0, 6, str(prediction) if prediction is not None else "-")
    pdf.ln(1)

    passed_count = 0
    failed_count = 0

    if evaluator_type == "qa_eval":
        val = eval_data.get("correct")
        if val is None:
            val = eval_data.get("score", eval_data.get("value"))
        status = "PASSED" if _to_pass(val) else "FAILED"
        passed_count += 1 if status == "PASSED" else 0
        failed_count += 1 if status == "FAILED" else 0

        pdf.set_font(base_font, "B", 12)
        pdf.cell(0, 7, f"QA Eval: {status}", ln=True)

    elif evaluator_type == "criteria_eval":
        crits = _extract_criteria(eval_data)

        pdf.set_font(base_font, "B", 12)
        pdf.cell(0, 7, "Criteria:", ln=True)

        if not crits:
            pdf.set_font(base_font, "", 12)
            pdf.multi_cell(0, 6, "No criteria details found in evaluator output.")
        else:
            for label, val in crits.items():
                status = "PASSED" if _to_pass(val) else "FAILED"
                if status == "PASSED":
                    passed_count += 1
                else:
                    failed_count += 1
                pdf.set_font(base_font, "B", 12)
                pdf.multi_cell(0, 6, f"{str(label).upper()}: {status}")

    reasoning = eval_data.get("reasoning")
    if reasoning:
        pdf.ln(1)
        pdf.set_font(base_font, "B", 12)
        pdf.cell(0, 7, "Reasoning:", ln=True)
        pdf.set_font(base_font, "", 12)
        pdf.multi_cell(0, 6, str(reasoning))

    pdf.ln(4)
    return passed_count, failed_count


def save_eval_report(
    results: List[Dict[str, Any]],
    evaluator_type: str = "auto",
    output_dir: str = "output",
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_name = f"evaluation_report_{timestamp}.pdf"
    pdf_path = os.path.join(output_dir, pdf_name)

    font_path = os.path.join("resources", "fonts", "DejaVuSans.ttf")
    font_bold_path = os.path.join("resources", "fonts", "DejaVuSans-Bold.ttf")

    pdf = FPDF()
    pdf.add_page()
    _ensure_fonts(pdf, font_path, font_bold_path)

    _draw_header(pdf, "Evaluation Report")

    total_pass = 0
    total_fail = 0
    total_cases = 0

    if not results:
        base_font = "DejaVu" if "DejaVu" in pdf.fonts else "Arial"
        pdf.set_font(base_font, "", 12)
        pdf.multi_cell(0, 8, "No results to display.")
    else:
        for idx, item in enumerate(results, start=1):
            input_text = item.get("input")
            prediction = item.get("prediction")
            reference = item.get("reference")
            eval_data = item.get("eval") or {}

            etype = evaluator_type
            if etype == "auto":
                etype = _detect_evaluator_type(eval_data)

            p, f = _draw_item_block(
                pdf=pdf,
                index=idx,
                input_text=input_text,
                prediction=prediction,
                reference=reference,
                eval_data=eval_data,
                evaluator_type=etype,
            )
            total_pass += p
            total_fail += f
            total_cases += 1

    base_font = "DejaVu" if "DejaVu" in pdf.fonts else "Arial"
    pdf.set_font(base_font, "B", 14)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.ln(2)
    pdf.set_font(base_font, "", 12)
    pdf.cell(0, 7, f"Total examples: {total_cases}", ln=True)
    pdf.cell(0, 7, f"Total PASSED: {total_pass}", ln=True)
    pdf.cell(0, 7, f"Total FAILED: {total_fail}", ln=True)

    pdf.output(pdf_path)
    print(f"✅ Report generated: {pdf_path}")


def _normalize_input_text(input_text):
    if isinstance(input_text, dict):
        for k in ("input", "question", "prompt", "text"):
            v = input_text.get(k)
            if isinstance(v, str):
                return v
    return str(input_text) if input_text is not None else "-"
