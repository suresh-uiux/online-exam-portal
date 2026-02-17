import json
import os
import time
import threading

DB_FILE = "mcq_data.json"
TIME_LIMIT = 10 



def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"questions": [], "results": []}


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)


db = load_db()


# ---------------- TIMED INPUT ----------------
def timed_input(prompt, timeout):
    answer = [None]

    def get_input():
        answer[0] = input(prompt)

    t = threading.Thread(target=get_input)
    t.start()

    t.join(timeout)

    if t.is_alive():
        print("\n⏰ Time's up!")
        return None

    return answer[0]


# ---------------- ADMIN ----------------
def add_question():
    q = input("Question: ")

    opts = []
    for i in range(4):
        opts.append(input(f"Option {i+1}: "))

    ans = int(input("Correct option (1-4): "))

    db["questions"].append({
        "question": q,
        "options": opts,
        "answer": ans
    })

    save_db(db)
    print("✅ Added!")


# ---------------- EXAM ----------------
def take_exam():
    if not db["questions"]:
        print("No questions!")
        return

    name = input("Student name: ")
    score = 0
    total = len(db["questions"])

    print(f"\n⏱ You have {TIME_LIMIT} seconds per question!")

    for i, q in enumerate(db["questions"], 1):
        print(f"\nQ{i}: {q['question']}")

        for idx, opt in enumerate(q["options"], 1):
            print(f"{idx}. {opt}")

        ans = timed_input("Answer (1-4): ", TIME_LIMIT)

        if ans and ans.isdigit() and int(ans) == q["answer"]:
            score += 1

    result = {"name": name, "score": score, "total": total}
    db["results"].append(result)
    save_db(db)

    print(f"\n✅ Finished! Score: {score}/{total}")


# ---------------- RESULTS ----------------
def view_results():
    for r in db["results"]:
        print(f"{r['name']} → {r['score']}/{r['total']}")


# ---------------- MENU ----------------
while True:
    print("\n=== MCQ TIMER EXAM ===")
    print("1.Add Question")
    print("2.Take Exam")
    print("3.Results")
    print("4.Exit")

    ch = input("Choose: ")

    if ch == "1":
        add_question()

    elif ch == "2":
        take_exam()

    elif ch == "3":
        view_results()

    else:
        break
