// Profile.js - Handle profile page functionality

document.addEventListener('DOMContentLoaded', function() {
    loadProfileData();
});

async function loadProfileData() {
    try {
        const response = await fetch('/api/profile');
        const result = await response.json();
        
        if (result.success) {
            const data = result.data;
            updateProfileUI(data);
        } else {
            console.error('Failed to load profile data:', result.message);
        }
    } catch (error) {
        console.error('Error loading profile data:', error);
    }
}

function updateProfileUI(data) {
    // Update user info
    const studentName = document.querySelector('.profile-info h2');
    const studentLevel = document.querySelector('.profile-info p');
    
    if (studentName) {
        studentName.textContent = data.user.username;
    }
    
    if (studentLevel) {
        studentLevel.textContent = `${data.preferences.experience || 'Beginner'} DSA Learner`;
    }
    
    // Update stats
    const statsElements = document.querySelectorAll('.profile-stats div');
    if (statsElements.length >= 3) {
        // Problems Solved
        statsElements[0].querySelector('p').textContent = data.stats.total_solved;
        
        // Topics Completed
        statsElements[1].querySelector('p').textContent = data.stats.completed_chapters;
        
        // Accuracy (replacing streak for now)
        statsElements[2].querySelector('h4').textContent = 'Accuracy';
        statsElements[2].querySelector('p').textContent = `${data.stats.accuracy}%`;
    }
    
    // Update progress bars with recent activity
    updateProgressBars(data.recent_activity);
    
    // Update achievements
    updateAchievements(data.stats);
}

function updateProgressBars(recentActivity) {
    // Load chapter progress instead of recent activity
    loadChapterProgress();
}

async function loadChapterProgress() {
    try {
        const response = await fetch('/api/chapter-progress');
        const result = await response.json();
        
        if (result.success) {
            updateChapterProgressBars(result.data.chapters);
        }
    } catch (error) {
        console.error('Error loading chapter progress:', error);
    }
}

function updateChapterProgressBars(chapters) {
    const progressItems = document.querySelectorAll('.progress-item');
    
    // Show top 3 chapters with most progress
    const sortedChapters = chapters
        .filter(ch => ch.total_attempts > 0)
        .sort((a, b) => b.progress_percentage - a.progress_percentage)
        .slice(0, 3);
    
    // If less than 3 chapters with progress, fill with not started ones
    const remainingChapters = chapters
        .filter(ch => ch.total_attempts === 0)
        .slice(0, 3 - sortedChapters.length);
    
    const displayChapters = [...sortedChapters, ...remainingChapters];
    
    progressItems.forEach((item, index) => {
        if (index < displayChapters.length) {
            const chapter = displayChapters[index];
            const span = item.querySelector('span');
            const fill = item.querySelector('.fill');
            
            span.textContent = chapter.chapter_name;
            fill.style.width = `${chapter.progress_percentage}%`;
            fill.textContent = `${chapter.progress_percentage}%`;
            
            // Add status-based styling
            fill.className = `fill ${chapter.status}`;
        } else {
            // Hide unused progress bars
            item.style.display = 'none';
        }
    });
}

function updateAchievements(stats) {
    const achievementsContainer = document.querySelector('.achievements');
    if (!achievementsContainer) return;
    
    const achievements = [];
    
    // Dynamic achievements based on stats
    if (stats.total_solved > 0) {
        achievements.push('✅ First Problem');
    }
    
    if (stats.total_solved >= 10) {
        achievements.push('🧠 10+ Problems');
    }
    
    if (stats.total_solved >= 25) {
        achievements.push('🚀 25+ Problems');
    }
    
    if (stats.total_solved >= 50) {
        achievements.push('⭐ 50+ Problems');
    }
    
    if (stats.accuracy >= 80) {
        achievements.push('🎯 High Accuracy');
    }
    
    if (stats.completed_chapters > 0) {
        achievements.push('📘 Chapter Complete');
    }
    
    if (stats.completion_rate >= 50) {
        achievements.push('🏆 Halfway There');
    }
    
    // Update achievements display
    achievementsContainer.innerHTML = achievements.map(achievement => 
        `<span>${achievement}</span>`
    ).join('');
}