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
        chapterName.textContent = data.data.latest_chapter_name;
    }
    catch(err){
        console.log(err);
    }
})();