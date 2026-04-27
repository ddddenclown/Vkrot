import jiwer
import json
from pathlib import Path
from typing import List, Dict


def words_to_text(words: List[Dict]) -> str:
    return " ".join(w["word"] for w in words)


def compute_wer(reference: str, hypothesis: str) -> float:
    return jiwer.wer(reference, hypothesis)


def compute_cer(reference: str, hypothesis: str) -> float:
    return jiwer.cer(reference, hypothesis)


def evaluate_timestamps(predicted: List[Dict], ground_truth: List[Dict], tolerance: float = 0.3) -> float:
    if not ground_truth:
        return 0.0
    correct = 0
    for gt in ground_truth:
        for pred in predicted:
            if pred["word"].lower() == gt["word"].lower():
                if abs(pred["start"] - gt["start"]) <= tolerance:
                    correct += 1
                    break
    return correct / len(ground_truth)


def evaluate_file(predicted_path: str, reference_text: str) -> Dict:
    with open(predicted_path) as f:
        predicted = json.load(f)

    hypothesis = words_to_text(predicted)
    wer = compute_wer(reference_text, hypothesis)
    cer = compute_cer(reference_text, hypothesis)

    return {
        "file": predicted_path,
        "wer": round(wer, 4),
        "cer": round(cer, 4),
        "hypothesis": hypothesis,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python eval.py <predicted.json> <reference_text>")
        sys.exit(1)

    result = evaluate_file(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, indent=2))
