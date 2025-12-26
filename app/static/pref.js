document.addEventListener('DOMContentLoaded', function() {
    const saveBtn = document.getElementById('save-btn');
    
    saveBtn.addEventListener('click', async function(e) {
        e.preventDefault();
        
        // Get selected values
        const goal = document.querySelector('input[name="goal"]:checked')?.value;
        const preference = document.querySelector('input[name="pref"]:checked')?.value;
        const experience = document.querySelector('input[name="exp"]:checked')?.value;
        
        // Validate selections
        if (!goal || !preference || !experience) {
            alert('Please select all preferences');
            return;
        }
        
        try {
            const formData = new FormData();
            const payload = {
                goals: goal,
                preference: preference,
                experience: experience
            };
            
            formData.append('payload', JSON.stringify(payload));
            
            const response = await fetch('/api/save-preference', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Redirect to dashboard after successful save
                window.location.href = '/dashboard';
            } else {
                alert(data.message || 'Failed to save preferences');
            }
            
        } catch (error) {
            console.error('Error saving preferences:', error);
            alert('Server error occurred');
        }
    });
});