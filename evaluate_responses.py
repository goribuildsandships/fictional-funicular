import argparse
import csv
from pathlib import Path

RATING_FIELDS = ["accuracy", "relevance", "clarity", "instruction_following"]

def main():
    parser = argparse.ArgumentParser(description="Score sample AI response evaluations.")
    parser.add_argument("--input", default="data/sample_responses.csv")
    parser.add_argument("--output", default="outputs/evaluation_results.csv")
    parser.add_argument("--threshold", type=float, default=3.5,
                        help="Rows averaging below this score are flagged for review.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    with input_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("Input CSV has no data rows.")

    results = []
    for line_number, row in enumerate(rows, start=2):
        try:
            scores = [int(row[field]) for field in RATING_FIELDS]
        except (KeyError, ValueError):
            raise SystemExit(f"Invalid or missing rating on CSV line {line_number}.")
        if any(score < 1 or score > 5 for score in scores):
            raise SystemExit(f"Ratings must be from 1 to 5 (CSV line {line_number}).")

        average = sum(scores) / len(scores)
        results.append({
            "response_id": row.get("response_id", ""),
            "average_score": f"{average:.2f}",
            "decision": "REVIEW" if average < args.threshold else "PASS",
            "reviewer_note": row.get("reviewer_note", "")
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["response_id", "average_score", "decision", "reviewer_note"])
        writer.writeheader()
        writer.writerows(results)

    flagged = sum(result["decision"] == "REVIEW" for result in results)
    print(f"Records evaluated: {len(results)}")
    print(f"Flagged for review: {flagged}")
    print(f"Threshold: {args.threshold:.2f}")
    print(f"Results saved to: {output_path}")

if __name__ == "__main__":
    main()
