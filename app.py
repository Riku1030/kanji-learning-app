
from flask import Flask, request, render_template, session, redirect, url_for
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import random
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = "your-secret-key"
HISTORY_FILE = "history.json"

def load_vocab(level):
    with open("n5.json", "r", encoding="utf-8") as f:
        vocab_data = json.load(f)
    return [item for item in vocab_data if item.get("level", "N5") == level]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        level = request.form["level"]
        session.pop("quiz", None)

        vocab_data = load_vocab(level)
        random.shuffle(vocab_data)
        remaining = vocab_data

        selected = remaining[:50]
        vocab_list = [item["word"] for item in selected]
        vocab_text = ", ".join(vocab_list)

        prompt = f'''
あなたは日本語教師です。以下の形式で、語彙リストから1語を選び「その読み」を問う問題を作成してください。

【質問文】
「問題：＿＿の ことばは ひらがなで どう かきますか？」

【例文条件】
- 読みを問う語を文中に入れてください（自然な例文）
- その語を <span class="underline">〜</span> で囲んでください
  例：「<span class='underline'>新しい</span> くるまですね。」

【選択肢条件】
- すべてひらがな、正解は1つ
- distractors（ひっかけ）も自然に

【語彙リスト】
{vocab_text}

【出力形式】
{{
  "question": "問題：＿＿の ことばは ひらがなで どう かきますか？\n<span class='underline'>部屋番号</span> を 覚えていますか？",
  "options": ["へやばんごう", "へあばんごー", "へやはんこう", "へやばんこ"],
  "answer": "へやばんごう",
  "explanation": "「部屋番号」は「へやばんごう」と読みます。"
}}

※マークダウンや装飾（``` や json 表記）は不要です  
※文中には <span class="underline">〜</span> を必ず使ってください
'''

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=1.0,
                messages=[
                    {"role": "system", "content": "あなたは優秀な日本語教師です"},
                    {"role": "user", "content": prompt}
                ]
            )

            message = response.choices[0].message.content.strip()
            if not message:
                return "GPTの応答が空でした"

            if message.startswith("```"):
                message = message.strip("`").replace("json\n", "").replace("json", "")

            data = json.loads(message)
            data["level"] = level
            session["quiz"] = data

            return render_template("quiz.html", question=data["question"], options=data["options"])

        except Exception as e:
            return f"エラーが発生しました: {e}"

    return render_template("index.html")

@app.route("/quiz", methods=["GET"])
def quiz():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("index"))
    return render_template("quiz.html", question=quiz["question"], options=quiz["options"])

@app.route("/answer", methods=["POST"])
def answer():
    selected = request.form.get("selected_option")
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("index"))

    correct = quiz["answer"]
    explanation = quiz["explanation"]
    level = quiz.get("level", "不明")

    history_data = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_data = json.load(f)

    new_entry = {
        "id": len(history_data) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "question": quiz["question"],
        "options": quiz["options"],
        "selected": selected,
        "answer": correct,
        "explanation": explanation,
        "is_correct": selected == correct
    }

    history_data.append(new_entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)

    return render_template("result.html",
                           question=quiz["question"],
                           options=quiz["options"],
                           selected=selected,
                           correct=correct,
                           explanation=explanation)

@app.route("/history")
def history():
    PER_PAGE = 10
    page = int(request.args.get("page", 1))

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_data = json.load(f)
    else:
        history_data = []

    history_data = history_data[-50:]
    total = len(history_data)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_data = history_data[start:end]
    total_pages = (total + PER_PAGE - 1) // PER_PAGE

    return render_template("history.html",
                           history=page_data,
                           page=page,
                           total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)
