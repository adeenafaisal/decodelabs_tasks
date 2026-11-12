QUESTIONS = [
    ("What is the capital of France?", ("paris",)),
    ("What is the largest planet in our solar system?", ("jupiter",)),
    ("What is the chemical formula for water?", ("h2o",)),
]


def ask_question(prompt, accepted_answers):
    """One question block. Returns True if the user answered correctly."""
  
    raw_answer = input(f"{prompt} ")

    answer = raw_answer.strip().lower()

    is_correct = answer in accepted_answers

    if is_correct:
        print("  Correct! +1 point\n")
    else:
        print(f"  Incorrect. The answer was: {accepted_answers[0].title()}\n")
    return is_correct


def main():
    score = 0 
    total = len(QUESTIONS)

    print("=== General Knowledge Quiz ===")
    print(f"Answer {total} questions. 1 point for each correct answer.\n")

    for number, (prompt, accepted) in enumerate(QUESTIONS, start=1):
        print(f"Question {number} of {total}")
        if ask_question(prompt, accepted):
            score += 1  
    print("=== Quiz Complete ===")
    print(f"Final score: {score:>2} / {total}")


if __name__ == "__main__":
    main()