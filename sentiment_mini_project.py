import argparse

from textblob import TextBlob


def validate_input(text):
    """Validate input type and non-empty content."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    if not text.strip():
        raise ValueError("Input cannot be empty.")


def predict_sentiment(text, positive_threshold=0.15, negative_threshold=-0.15):
    """
    Return sentiment label and polarity score.
    Label logic:
    - polarity > positive_threshold -> Positive
    - polarity < negative_threshold -> Negative
    - otherwise -> Neutral
    """
    validate_input(text)
    polarity = TextBlob(text).sentiment.polarity

    if polarity > positive_threshold:
        label = "Positive"
    elif polarity < negative_threshold:
        label = "Negative"
    else:
        label = "Neutral"

    return {"text": text, "label": label, "polarity": round(polarity, 3)}


def run_demo_tests():
    """
    Run 12 fixed test sentences:
    - 4 positive
    - 4 negative
    - 4 neutral
    """
    test_samples = [
        # Positive (4)
        ("I absolutely loved the food and the service was excellent.", "Positive"),
        ("This new phone is amazing and works perfectly.", "Positive"),
        ("What a wonderful experience, I am very happy.", "Positive"),
        ("The team did a great job and delivered early.", "Positive"),
        # Negative (4)
        ("I hate this app; it crashes all the time.", "Negative"),
        ("The movie was terrible and extremely boring.", "Negative"),
        ("This is the worst customer support I have ever seen.", "Negative"),
        ("I am disappointed and frustrated with the results.", "Negative"),
        # Neutral (4)
        ("The meeting starts at 10 AM tomorrow.", "Neutral"),
        ("I bought a notebook and two pens.", "Neutral"),
        ("The package arrived on Tuesday afternoon.", "Neutral"),
        ("We discussed the project timeline for next quarter.", "Neutral"),
    ]

    print("Sentiment Analysis Mini Project")
    print("-" * 80)
    print(f"{'Expected':<10} {'Predicted':<10} {'Polarity':<10} Text")
    print("-" * 80)

    correct = 0
    uncertain_items = []
    results = []

    for text, expected in test_samples:
        result = predict_sentiment(text)
        predicted = result["label"]
        polarity = result["polarity"]

        if expected == predicted:
            correct += 1
        if abs(polarity) < 0.2:
            uncertain_items.append((text, expected, predicted, polarity))

        results.append((text, expected, predicted, polarity))
        print(f"{expected:<10} {predicted:<10} {polarity:<10} {text}")

    total = len(test_samples)
    accuracy = correct / total
    print("-" * 80)
    print(f"Accuracy: {correct}/{total} = {accuracy:.2%}")

    print("\nBasic validation examples:")
    try:
        predict_sentiment("")
    except Exception as exc:
        print(f"- Empty input check: {type(exc).__name__}: {exc}")

    try:
        predict_sentiment(123)  # non-string
    except Exception as exc:
        print(f"- Non-string input check: {type(exc).__name__}: {exc}")

    return results, uncertain_items


def analyze_uncertain_or_incorrect(results, uncertain_items):
    print("\nBrief analysis of 2 incorrect or uncertain predictions:")

    incorrect = [row for row in results if row[1] != row[2]]
    candidates = incorrect[:2]

    if len(candidates) < 2:
        for item in uncertain_items:
            row = (item[0], item[1], item[2], item[3])
            if row not in candidates:
                candidates.append(row)
            if len(candidates) == 2:
                break

    if not candidates:
        print("- No incorrect or uncertain predictions found in this run.")
        return

    for idx, (text, expected, predicted, polarity) in enumerate(candidates, start=1):
        print(f"\n{idx}) Text: {text}")
        print(f"   Expected: {expected}, Predicted: {predicted}, Polarity: {polarity}")
        if expected != predicted:
            print(
                "   Why this may happen: The lexical model can miss context, "
                "domain cues, or subtle tone."
            )
        else:
            print(
                "   Why uncertain: Polarity is close to zero, so wording looks "
                "mostly factual with weak emotional signals."
            )


def analyze_user_inputs(entries):
    """Analyze 2 predictions from interactive user inputs."""
    print("\nBrief analysis of 2 predictions from your input:")

    if not entries:
        print("- No user inputs found to analyze.")
        return

    for idx, item in enumerate(entries[:2], start=1):
        print(f"\n{idx}) Text: {item['text']}")
        print(f"   Predicted: {item['label']}, Polarity: {item['polarity']}")
        if abs(item["polarity"]) < 0.2:
            print(
                "   Why uncertain: Score is close to neutral, so the sentence has "
                "limited emotional words or mixed tone."
            )
        else:
            print(
                "   Why this label: The polarity is farther from zero, so the model "
                "detects clearer positive or negative wording."
            )


def run_interactive_mode(show_analysis=False):
    """Accept user text repeatedly until they type 'quit'."""
    print("Interactive mode enabled. Type a sentence and press Enter.")
    print("Type 'quit' to exit.")
    if show_analysis:
        print("Analysis mode enabled: summary shown when you exit.")

    history = []

    while True:
        user_text = input("\nEnter text: ")
        if user_text.strip().lower() == "quit":
            print("Exiting interactive mode.")
            break

        try:
            result = predict_sentiment(user_text)
            history.append(result)
            print(
                f"Sentiment: {result['label']} | "
                f"Polarity: {result['polarity']} | "
                f"Text: {result['text']}"
            )
        except Exception as exc:
            print(f"Input error: {type(exc).__name__}: {exc}")

    if show_analysis:
        analyze_user_inputs(history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sentiment analysis mini project.")
    parser.add_argument(
        "--text",
        type=str,
        help="Analyze one sentence directly from command line.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run interactive mode to input multiple sentences.",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Show brief analysis of 2 incorrect/uncertain predictions in demo mode, or 2 user inputs in interactive mode.",
    )
    args = parser.parse_args()

    if args.text is not None:
        try:
            output = predict_sentiment(args.text)
            print(output)
        except Exception as exc:
            print(f"Input error: {type(exc).__name__}: {exc}")
    elif args.interactive:
        run_interactive_mode(show_analysis=args.analyze)
    else:
        all_results, uncertain = run_demo_tests()
        if args.analyze or not args.text:
            analyze_uncertain_or_incorrect(all_results, uncertain)
