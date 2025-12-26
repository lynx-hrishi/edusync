// let BACKENDURL = "https://fluffy-heidi-monoprotic.ngrok-free.dev";
const level = document.getElementById("level");
const problemSolved = document.getElementById("prbm-slvd");
const chapterComplete = document.getElementById("chp-cmplete");
const chapterName = document.getElementById("chp-name");

(async function () {
    try{
        const response = await fetch("/api/learning-path");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Network response was not ok");
        }

        console.log(data);
        level.textContent = data.data.experience;
        problemSolved.textContent = data.data.correct_attempts;
        chapterComplete.textContent = data.data.completed_chapters;
        chapterName.textContent = data.data.latest_chapter_name ?? "Not Started";
        
        // Load chapter progress for progress bars
        loadChapterProgress();
    }
    catch(err){
        console.log(err);
    }
})();

async function loadChapterProgress() {
    try {
        const response = await fetch("/api/chapter-progress");
        const result = await response.json();
        
        if (result.success) {
            updateProgressBars(result.data.chapters);
        }
    } catch (error) {
        console.error('Error loading chapter progress:', error);
    }
}

function updateProgressBars(chapters) {
    const progressItems = document.querySelectorAll('.progress-item');
    
    chapters.forEach((chapter, index) => {
        if (index < progressItems.length) {
            const item = progressItems[index];
            const span = item.querySelector('span');
            const fill = item.querySelector('.fill');
            
            span.textContent = chapter.chapter_name;
            fill.style.width = `${chapter.progress_percentage}%`;
            fill.textContent = `${chapter.progress_percentage}%`;
            
            // Add status-based styling
            fill.className = `fill ${chapter.status}`;
        }
    });
}