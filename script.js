const titleScreen = document.getElementById('title-screen');
const quizScreen = document.getElementById('quiz-screen');
const startButton = document.getElementById('start-button');
const quizKanji = document.getElementById('quiz-kanji');
const readingInput = document.getElementById('reading-input');
const submitButton = document.getElementById('submit-answer');
const feedback = document.getElementById('feedback');
const returnButton = document.getElementById('return-button');

let kanjiQuiz = [];
let currentIndex = 0;
const maxQuestions = 10;

// スタートボタンをクリックでタイトル画面を非表示、クイズ画面を表示
startButton.addEventListener('click', () => {
    titleScreen.style.display = 'none';
    quizScreen.style.display = 'block';
    returnButton.style.display = 'none';
    currentIndex = 0;
    loadQuestion();
});

// タイトルに戻るボタンの動作
returnButton.addEventListener('click', () => {
    titleScreen.style.display = 'flex';
    quizScreen.style.display = 'none';
    feedback.textContent = '';
    readingInput.value = '';
    submitButton.disabled = false;
});

// 漢字データを外部JSONファイルから読み込む
fetch('extracted_kanji_data.json')
    .then(response => response.json())
    .then(data => {
        // シャッフルしてから10問だけ選ぶ
        kanjiQuiz = shuffleArray(data).slice(0, maxQuestions);
    })
    .catch(error => {
        console.error('Error loading kanji data:', error);
        feedback.textContent = '漢字データの読み込みに失敗しました。';
    });

function loadQuestion() {
    if (kanjiQuiz.length > 0 && currentIndex < maxQuestions) {
        quizKanji.textContent = kanjiQuiz[currentIndex].kanji;
        feedback.textContent = '';
        readingInput.value = '';
    } else {
        feedback.textContent = 'クイズ終了！お疲れ様でした！🎉';
        feedback.style.color = 'blue';
        submitButton.disabled = true;
        returnButton.style.display = 'inline-block';
    }
}

submitButton.addEventListener('click', () => {
    const userAnswer = readingInput.value.trim();
    const correctAnswer = kanjiQuiz[currentIndex].reading;

    if (userAnswer === correctAnswer) {
        feedback.textContent = '正解です！🎉';
        feedback.style.color = 'green';
    } else {
        feedback.textContent = `正解は "${correctAnswer}" です。😢`;
        feedback.style.color = 'red';
    }

    currentIndex++;
    setTimeout(loadQuestion, 2000);
});

// 配列をシャッフルする関数
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
