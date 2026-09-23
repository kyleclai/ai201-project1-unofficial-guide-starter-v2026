def judge(question, expects, answer, results) -> bool:
    """
    q: 'give', expect: 'give'
    the epext is in the answer
    """
    # run code: python run_eval.py
    return expects.lower().strip() in answer.lower()

    """
    typically in industry you'll run: "llm as judge"
    use rapidfuzz to write a judge function, use the judge function above as a template to check expected answers.
    """
