# AI Response Quality Evaluator

A small Python command-line project that calculates a quality score for sample AI-generated responses using a transparent 1–5 rubric.

## What it does

- Reads evaluation records from a CSV file.
- Checks that each rating is between 1 and 5.
- Calculates the average score across accuracy, relevance, clarity, and instruction-following.
- Flags records below the configured review threshold.
- Writes a summary CSV that can be opened in a spreadsheet.

## Dataset

`data/sample_responses.csv` contains fictional prompts and responses created for this demo. Ratings are illustrative examples, not expert or benchmark judgments.

## Requirements

- Python 3.9 or newer
- No third-party packages required

## Run it

From this project folder:

```bash
python src/evaluate_responses.py
```

To use a different input or output file:

```bash
python src/evaluate_responses.py --input data/sample_responses.csv --output outputs/evaluation_results.csv --threshold 3
```

## Scoring approach

The script averages four ratings: accuracy, relevance, clarity, and instruction-following. A row is marked `REVIEW` if its average is below the chosen threshold. This simple score is a demonstration rubric; real evaluation programs should use task-specific guidance and human judgment.

## Example result

The script writes `outputs/evaluation_results.csv` and prints a short summary to the terminal. The included output was generated from the included synthetic dataset.

## Limitations

This tool does not determine truth automatically, use an AI model, or replace human review. The ratings are entered by a reviewer.
