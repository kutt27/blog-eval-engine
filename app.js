document.addEventListener('DOMContentLoaded', () => {
    const blogEditor = document.getElementById('blog-editor');
    const wordCount = document.getElementById('word-count');
    const btnEvaluate = document.getElementById('btn-evaluate');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Handle Editor Input
    blogEditor.addEventListener('input', () => {
        const text = blogEditor.value.trim();
        
        // Update word count
        const count = text ? text.split(/\s+/).length : 0;
        wordCount.textContent = `${count} words`;
        
        // Enable/Disable evaluate button
        btnEvaluate.disabled = count < 10; // Require at least 10 words
    });

    // Handle Chips Selection
    document.querySelectorAll('.chip-group').forEach(group => {
        const isMulti = group.dataset.multi === 'true';
        
        group.addEventListener('click', (e) => {
            if (e.target.classList.contains('chip')) {
                if (!isMulti) {
                    group.querySelectorAll('.chip').forEach(c => c.classList.remove('selected'));
                    e.target.classList.add('selected');
                } else {
                    e.target.classList.toggle('selected');
                }
            }
        });
    });

    // Evaluation Trigger
    btnEvaluate.addEventListener('click', () => {
        // Collect choices
        const config = {
            content: blogEditor.value,
            audience: Array.from(document.querySelectorAll('[data-group="audience"] .selected')).map(c => c.dataset.value),
            style: Array.from(document.querySelectorAll('[data-group="style"] .selected')).map(c => c.dataset.value),
            purpose: document.getElementById('purpose').value,
            platform: document.getElementById('platform').value,
            depth: document.querySelector('[data-group="depth"] .selected').dataset.value,
            custom: document.getElementById('custom-focus').value
        };

        console.log('Running evaluation with config:', config);
        
        // Show loading state
        loadingOverlay.style.display = 'flex';

        // Simulate API call to the sync engine
        setTimeout(() => {
            loadingOverlay.style.display = 'none';
            alert('Evaluation complete! (Simulation mode). Check console for config details.');
        }, 3000);
    });
});
