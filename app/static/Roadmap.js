let chapters = [];
let currentChapterId = null;
let currentConceptId = null;
let currentQuestions = [];
let currentQuestionIndex = 0;

async function loadChapters() {
    try {
        const response = await fetch('/api/chapters');
        const data = await response.json();
        chapters = data.data.chapters;
        renderRoadmap();
    } catch (error) {
        console.error('Error loading chapters:', error);
    }
}

function renderRoadmap() {
    const roadmapSection = document.getElementById('roadmap');
    roadmapSection.innerHTML = '';
    
    chapters.forEach((chapter, index) => {
        const card = document.createElement('div');
        card.className = 'roadmap-card';
        card.onclick = () => openChapter(chapter.id);
        
        card.innerHTML = `
            <h4>${index + 1}. ${chapter.title}</h4>
            <p>${chapter.description}</p>
            <span>🔓 Available</span>
        `;
        
        roadmapSection.appendChild(card);
    });
}

async function openChapter(chapterId) {
    currentChapterId = chapterId;
    const chapter = chapters.find(c => c.id === chapterId);
    
    document.getElementById("roadmap").style.display = "none";
    document.getElementById("chapterDetail").style.display = "block";
    
    document.getElementById("chapterTitle").innerText = chapter.title;
    document.getElementById("chapterDescription").innerText = chapter.description;
    
    const subtopicsDiv = document.getElementById("subtopics");
    subtopicsDiv.innerHTML = "";
    
    chapter.concepts.forEach(concept => {
        const btn = document.createElement("button");
        btn.innerText = concept.concept_name;
        btn.onclick = () => openConcept(chapterId, concept.concept_id);
        subtopicsDiv.appendChild(btn);
    });
    
    document.getElementById("topicTitle").innerText = "Select a concept";
    document.getElementById("topicText").innerText = "Click a concept to view its content.";
    document.getElementById("testbtn").style.display = "none";
}

async function openConcept(chapterId, conceptId) {
    currentConceptId = conceptId;
    try {
        const response = await fetch(`/api/concepts/${chapterId}/${conceptId}`);
        const data = await response.json();
        const concept = data.data.concept;
        
        document.getElementById("topicTitle").innerText = concept.concept_name;
        document.getElementById("topicText").innerText = concept.concept_desc;
        document.getElementById("testbtn").style.display = "inline-block";
    } catch (error) {
        console.error('Error loading concept:', error);
    }
}

function goBack() {
    document.getElementById("chapterDetail").style.display = "none";
    document.getElementById("roadmap").style.display = "grid";
    document.getElementById("testbtn").style.display = "none";
}

function openQuiz() {
    document.getElementById("quizModal").style.display = "flex";
}

function closeQuiz() {
    document.getElementById("quizModal").style.display = "none";
    document.getElementById("quizResult").innerText = "";
    document.getElementById("quizForm").reset();
}

async function loadQuiz() {
    if (!currentChapterId || !currentConceptId) return;
    
    try {
        const response = await fetch(`/api/test-concept/${currentChapterId}/${currentConceptId}`);
        const data = await response.json();
        currentQuestions = data.data.questions;
        currentQuestionIndex = 0;
        
        displayQuestionInContent();
    } catch (error) {
        console.error('Error loading quiz:', error);
    }
}

function displayQuestionInContent() {
    if (currentQuestionIndex >= currentQuestions.length) {
        document.getElementById("contentArea").innerHTML = `
            <h3>Quiz Complete! 🎉</h3>
            <p>You have completed all questions for this concept.</p>
            <button onclick="resetToContent()">Back to Content</button>
        `;
        return;
    }
    
    const question = currentQuestions[currentQuestionIndex];
    
    document.getElementById("contentArea").innerHTML = `
        <h3>Quick Quiz 🧠</h3>
        <p>${question.question}</p>
        
        <form id="quizForm">
            ${question.options.map(option => `
                <label>
                    <input type="radio" name="option" value="${option}"> ${option}
                </label><br>
            `).join('')}
            
            <button type="button" onclick="submitQuiz()">Submit</button>
        </form>
        
        <p id="quizResult"></p>
    `;
}

function resetToContent() {
    const chapter = chapters.find(c => c.id === currentChapterId);
    const concept = chapter.concepts.find(c => c.concept_id === currentConceptId);
    
    document.getElementById("contentArea").innerHTML = `
        <h3 id="topicTitle">${concept.concept_name}</h3>
        <p id="topicText">Click a concept to view its content.</p>
        <button id="testbtn" onclick="loadQuiz()">Test Concept</button>
    `;
}

async function submitQuiz() {
    const options = document.getElementsByName("option");
    let selected = "";
    
    for (let opt of options) {
        if (opt.checked) {
            selected = opt.value;
        }
    }
    
    if (!selected) {
        document.getElementById("quizResult").innerText = "⚠️ Please select an option";
        return;
    }
    
    const question = currentQuestions[currentQuestionIndex];
    
    try {
        const formData = new FormData();
        formData.append('payload', JSON.stringify({
            question_id: question.question_id,
            chosen_option: selected
        }));
        
        const response = await fetch('/api/check-answer', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        const resultDiv = document.getElementById("quizResult");
        
        if (data.data.correct) {
            resultDiv.innerHTML = `
                <div style="color: green;">✅ Correct Answer!</div>
                <div style="margin: 10px 0;">${data.data.explanation || ''}</div>
                <button onclick="nextQuestion()" style="margin-top: 10px;">Next Question</button>
            `;
        } else {
            resultDiv.innerHTML = `
                <div style="color: red;">❌ Wrong Answer! Correct: ${data.data.correct_answer}</div>
                <button onclick="nextQuestion()" style="margin-top: 10px;">Next Question</button>
            `;
        }
        
    } catch (error) {
        console.error('Error checking answer:', error);
    }
}

function nextQuestion() {
    currentQuestionIndex++;
    displayQuestionInContent();
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadChapters();
});