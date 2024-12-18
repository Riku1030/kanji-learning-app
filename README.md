<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>漢字学習アプリ</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f8ff;
            color: #333;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .title-screen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #ff9f68, #ff6f61);
            color: #fff;
            animation: fadeIn 2s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .title-screen h1 {
            font-size: 4em;
            margin-bottom: 20px;
            text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
        }
        .title-screen p {
            font-size: 1.5em;
            margin-bottom: 30px;
        }
        .title-screen button {
            padding: 15px 40px;
            font-size: 1.5em;
            background-color: #ff3f3f;
            color: #fff;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
        }
        .title-screen button:hover {
            background-color: #e62e2e;
            transform: scale(1.1);
        }
        .content {
            display: none;
            animation: slideIn 1s;
        }
        @keyframes slideIn {
            from {
                transform: translateY(100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        .correct-feedback {
            color: green;
            font-size: 1.5em;
            font-weight: bold;
            animation: bounce 1s;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-20px);
            }
            60% {
                transform: translateY(-10px);
            }
        }
        .emoji {
            font-size: 2em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="title-screen">
        <h1>漢字学習アプリ</h1>
        <p>楽しく漢字を覚えよう！</p>
        <button id="start-button">ゲームを始める</button>
    </div>

    <div class="content" id="main-content">
        <header>
            <h1>漢字学習アプリ</h1>
            <nav>
                <ul>
                    <li><a href="#practice">練習</a></li>
                    <li><a href="#quiz">クイズ</a></li>
                    <li><a href="#history">学習履歴</a></li>
                </ul>
            </nav>
        </header>

        <main>
            <section id="quiz">
                <h2>漢字の読み方クイズ</h2>
                <p>次の漢字の読みを入力してください: <strong id="quiz-kanji">日</strong></p>
                <input type="text" id="reading-input" placeholder="読み方を入力">
                <button id="submit-answer">答え合わせ</button>
                <p id="feedback"></p>
            </section>
        </main>

        <footer>
            <p>&copy; 2024 漢字学習アプリ</p>
        </footer>
    </div>

    <script>
        const startButton = document.getElementById('start-button');
        const titleScreen = document.querySelector('.title-screen');
        const mainContent = document.getElementById('main-content');

        startButton.addEventListener('click', () => {
            titleScreen.style.display = 'none';
            mainContent.style.display = 'block';
        });

        const quizKanji = document.getElementById('quiz-kanji');
        const readingInput = document.getElementById('reading-input');
        const submitButton = document.getElementById('submit-answer');
        const feedback = document.getElementById('feedback');

        const kanjiQuiz = [
            { kanji: '日', reading: 'にち' },
            { kanji: '月', reading: 'つき' },
            { kanji: '木', reading: 'き' },
            { kanji: '水', reading: 'みず' },
            { kanji: '火', reading: 'ひ' },
            { kanji: '金', reading: 'きん' }
        ];

        let currentIndex = 0;

        function loadQuestion() {
            quizKanji.textContent = kanjiQuiz[currentIndex].kanji;
            feedback.textContent = '';
            readingInput.value = '';
        }

        submitButton.addEventListener('click', () => {
            const userAnswer = readingInput.value.trim();
            const correctAnswer = kanjiQuiz[currentIndex].reading;

            if (userAnswer === correctAnswer) {
                feedback.innerHTML = '<span class="correct-feedback">正解です！🎉</span><div class="emoji">✨👏😊</div>';
            } else {
                feedback.textContent = `正解は "${correctAnswer}" です。😢`;
                feedback.style.color = 'red';
            }

            currentIndex = (currentIndex + 1) % kanjiQuiz.length;
            setTimeout(loadQuestion, 2000);
        });

        loadQuestion();
    </script>
</body>
</html>
