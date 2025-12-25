function openChapter(card) {
    const title = card.dataset.title;
    const desc = card.dataset.desc;

    document.getElementById("roadmap").style.display = "none";
    document.getElementById("chapterDetail").style.display = "block";

    document.getElementById("chapterTitle").innerText = title;
    document.getElementById("chapterDescription").innerText = desc;
}

function goBack() {
    document.getElementById("roadmap").style.display = "grid";
    document.getElementById("chapterDetail").style.display = "none";
}

const chapters = {
    basics: {
        title: "Basics & Complexity",
        description: "Learn algorithm fundamentals, time & space complexity, and Big-O notation.",
        topics: {
            "What is Algorithm?": "An algorithm is a step-by-step procedure to solve a problem efficiently.",
            "Time Complexity": "Time complexity measures how execution time grows with input size.",
            "Space Complexity": "Space complexity measures extra memory used by an algorithm.",
            "Big-O Notation": "Big-O describes the worst-case performance of an algorithm."
        }
    },

    arrays: {
        title: "Arrays",
        description: "Master arrays using popular techniques and interview problems.",
        topics: {
            "Introduction to Arrays": "Arrays store elements in contiguous memory locations.",
            "Prefix Sum": "Prefix sum helps answer range queries efficiently.",
            "Sliding Window": "Sliding window optimizes subarray problems.",
            "Kadane’s Algorithm": "Finds the maximum subarray sum in linear time."
        }
    },

    strings: {
        title: "Strings",
        description: "Learn string manipulation techniques for coding interviews.",
        topics: {
            "String Basics": "Strings are sequences of characters.",
            "Two Pointer Technique": "Efficiently process strings using two pointers.",
            "Pattern Matching": "Match patterns using brute force or optimized techniques."
        }
    },

};

function openChapter(key) {
    const chapter = chapters[key];

    document.getElementById("roadmap").style.display = "none";
    document.getElementById("chapterDetail").style.display = "block";

    document.getElementById("chapterTitle").innerText = chapter.title;
    document.getElementById("chapterDescription").innerText = chapter.description;

    const subtopicsDiv = document.getElementById("subtopics");
    subtopicsDiv.innerHTML = "";

    Object.keys(chapter.topics).forEach(topic => {
        const btn = document.createElement("button");
        btn.innerText = topic;
        btn.onclick = () => openTopic(topic, chapter.topics[topic]);
        subtopicsDiv.appendChild(btn);
    });

    document.getElementById("topicTitle").innerText = "Select a topic";
    document.getElementById("topicText").innerText = "Click a subtopic to view its content.";

    document.getElementById("testbtn").style.display = "none";
}

function openTopic(title, content) {
    document.getElementById("topicTitle").innerText = title;
    document.getElementById("topicText").innerText = content;

    document.getElementById("testbtn").style.display = "inline-block";
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

function submitQuiz() {
    const options = document.getElementsByName("option");
    let selected = "";

    for (let opt of options) {
        if (opt.checked) {
            selected = opt.value;
        }
    }

    const result = document.getElementById("quizResult");

    if (selected === "") {
        result.innerText = "⚠️ Please select an option";
        return;
    }

    if (selected === "O(log n)") {
        result.innerText = "✅ Correct Answer!";
        result.style.color = "green";
    } else {
        result.innerText = "❌ Wrong Answer!";
        result.style.color = "red";
    }
}

function loadQuiz() {
    const content = document.getElementById("contentArea");

    content.innerHTML = `
        <h3>Quick Quiz 🧠</h3>
        <p>What is the time complexity of Binary Search?</p>

        <form id="quizForm">
            <label>
                <input type="radio" name="option" value="O(n)"> O(n)
            </label><br>

            <label>
                <input type="radio" name="option" value="O(log n)"> O(log n)
            </label><br>

            <label>
                <input type="radio" name="option" value="O(n log n)"> O(n log n)
            </label><br>

            <label>
                <input type="radio" name="option" value="O(1)"> O(1)
            </label><br><br>

            <button type="button" onclick="submitQuiz()">Submit</button>
        </form>

        <p id="quizResult"></p>
    `;
}

function submitQuiz() {
    const options = document.getElementsByName("option");
    let selected = "";

    for (let opt of options) {
        if (opt.checked) {
            selected = opt.value;
        }
    }

    const result = document.getElementById("quizResult");

    if (!selected) {
        result.innerText = "⚠️ Please select an option";
        result.style.color = "orange";
        return;
    }

    if (selected === "O(log n)") {
        result.innerText = "✅ Correct Answer!";
        result.style.color = "lightgreen";
    } else {
        result.innerText = "❌ Wrong Answer. Correct is O(log n)";
        result.style.color = "red";
    }
}
