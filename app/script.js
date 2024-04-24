const questionEl = document.getElementById('question');
const options = document.querySelectorAll('.options input');
const submitBtn = document.getElementById('submit');
const resultEl = document.getElementById('result');

const questions = [
    {
        question: "What level of noise are you willing to tolerate?",
        answers: [
            { text: "A. Low"},
            { text: "B. Medium"},
            { text: "C. High" }
        ]
    },
    // Add more questions here in the same format 
];

let currentQuestion = 0;
let score = 0;

function loadQuestion() {
    deselectAnswers(); // Reset selected options

    const currentQuestionData = questions[currentQuestion];

    questionEl.innerText = currentQuestionData.question;
    currentQuestionData.answers.forEach(answer => {
        const option = document.getElementById('option' + (options.length + 1));
        option.value = answer.text;
        option.nextElementSibling.innerText = answer.text;
    });
}

function deselectAnswers() {
    options.forEach(option => option.checked = false);
}

function getSelected() {
    let selectedAnswer;
    options.forEach(option => {
        if (option.checked) {
            selectedAnswer = option.value;
        }
    });
    return selectedAnswer;
}

submitBtn.addEventListener('click', () => {
    const answer = getSelected();
    if (answer) {
        if (questions[currentQuestion].answers.find(a => a.text === answer).correct) {
            score++;
        }
        currentQuestion++;
        if (currentQuestion < questions.length) {
            loadQuestion();
        } else {
            resultEl.innerHTML = `<h2>You answered ${score}/${questions.length} questions correctly</h2> 
                                  <button onclick="location.reload()">Reload</button>`;
        }
    }
});

loadQuestion(); 
