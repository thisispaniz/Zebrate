const questionEl = document.getElementById('question');
const options = document.querySelectorAll('.options input');
const submitBtn = document.getElementById('submit');
const resultEl = document.getElementById('result');

const questions = [
    {
        question: "What level of noise are you willing to tolerate?",
        answers: [
            { text: "A. Low", correct: false },
            { text: "B. Medium", correct: true },
            { text: "C. High", correct: false }
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
    currentQuestionData.answers.forEach((answer, index) => {
        const option = options[index];
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

// password stuff
let passwordInp = document.querySelector('.password-input');
let passwordChecklist = document.querySelectorAll('.list-item');


let validationRegex = [
    { regex: /.{8,}/ },
    { regex: /[0-9]/ },
    { regex: /[a-z]/},
    { regex: /[A-Z]/},
    { regex: /[^A-Za-z0-9]/ } 
];

passwordInp.addEventListener('keyup', () => {
    validationRegex.forEach((item, i) => {
        let isValid = item.regex.test(passwordInp.value);

        if (isValid) {
            passwordChecklist[i].classList.add('checked');
        } else {
            passwordChecklist[i].classList.remove('checked');
        }
    });
});

function myFunction() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
}

// Define selected filters
let selectedFilters = {};

// Function to toggle filter selection and update the list of selected filters
function toggleFilter(element, filterName) {
    if (element.classList.contains('unselected')) {
        element.classList.remove('unselected');
        element.classList.add('selected');
        selectedFilters[filterName] = true; // Add filter to the selected list
    } else {
        element.classList.remove('selected');
        element.classList.add('unselected');
        delete selectedFilters[filterName]; // Remove filter from the selected list
    }
    filterVenues(); // Apply the filter on the venue list
}

// Function to filter venues based on selected filters
function filterVenues() {
    const venues = document.querySelectorAll('.listedvenue');

    venues.forEach(venue => {
        let show = true;

        for (let filter in selectedFilters) {
            if (selectedFilters[filter]) {
                // If any selected filter doesn't match, hide the venue
                if (venue.dataset[filter] !== 'yes') {
                    show = false;
                    break;
                }
            }
        }

        if (show) {
            venue.style.display = 'block';
        } else {
            venue.style.display = 'none';
        }
    });
}

// Search functionality to filter based on text input
document.getElementById('searchButton').addEventListener('click', () => {
    const query = document.getElementById('inputbox').value.toLowerCase();
    const venues = document.querySelectorAll('.listedvenue');

    venues.forEach(venue => {
        const name = venue.querySelector('.listtitle').innerText.toLowerCase();
        if (name.includes(query)) {
            venue.style.display = 'block';
        } else {
            venue.style.display = 'none';
        }
    });
});
