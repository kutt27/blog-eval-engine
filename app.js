document.addEventListener('DOMContentLoaded', () => {
    const blogEditor = document.getElementById('blog-editor');
    const wordCount = document.getElementById('word-count');
    const btnEvaluate = document.getElementById('btn-evaluate');
    const loadingOverlay = document.getElementById('loading-overlay');
    const dashboard = document.getElementById('results-dashboard');

    // Handle Editor Input
    blogEditor.addEventListener('input', () => {
        const text = blogEditor.value.trim();

        // Update word count
        const count = text ? text.split(/\s+/).length : 0;
        if (wordCount) wordCount.textContent = `${count} words`;

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
    btnEvaluate.addEventListener('click', async () => {
        const depthChip = document.querySelector('[data-group="depth"] .selected');
        const config = {
            content: blogEditor.value,
            audience: Array.from(document.querySelectorAll('[data-group="audience"] .selected')).map(c => c.dataset.value),
            style: Array.from(document.querySelectorAll('[data-group="style"] .selected')).map(c => c.dataset.value),
            purpose: document.getElementById('purpose').value,
            blog_type: document.getElementById('blog-type').value,
            platform: document.getElementById('platform').value,
            depth: depthChip ? depthChip.dataset.value : 'Standard',
            custom: document.getElementById('custom-focus').value,
            prompt_injection: null
        };

        loadingOverlay.style.display = 'flex';

        try {
            const res = await fetch('/evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            });
            if (!res.ok) {
                throw new Error(`Server returned ${res.status}`);
            }
            const data = await res.json();
            renderResults(data);
        } catch (err) {
            console.error('Evaluation failed:', err);
            alert(`Evaluation failed: ${err.message}`);
        } finally {
            loadingOverlay.style.display = 'none';
        }
    });

    // ---------- Dashboard rendering ----------

    function renderResults(data) {
        document.getElementById('overall-score').textContent = data.overall_score ?? '--';
        document.getElementById('results-summary').textContent = data.summary ?? '';

        renderBreakdown(data.score_breakdown || []);
        renderList('strengths-list', data.strengths || []);
        renderImprovements(data.improvement_priorities || []);
        renderLineEdits(data.line_edits || []);
        renderList('comparative-list', data.comparative_analysis || []);

        dashboard.style.display = 'block';
        dashboard.classList.add('fade-in');
        if (window.lucide) lucide.createIcons();
        dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function renderList(id, items) {
        const el = document.getElementById(id);
        el.innerHTML = '';
        items.forEach(text => {
            const li = document.createElement('li');
            li.textContent = text;
            el.appendChild(li);
        });
    }

    function renderBreakdown(dims) {
        const el = document.getElementById('score-breakdown-list');
        el.innerHTML = '';
        dims.forEach(d => {
            const row = document.createElement('div');
            row.className = 'breakdown-row';
            row.innerHTML = `
                <div class="breakdown-meta">
                    <span class="breakdown-name">${escapeHtml(d.name)}</span>
                    <span class="breakdown-score">${d.score}</span>
                </div>
                <div class="breakdown-bar"><div class="breakdown-fill" style="width:${d.score}%"></div></div>
                <p class="breakdown-rationale">${escapeHtml(d.rationale || '')}</p>
            `;
            el.appendChild(row);
        });
    }

    function renderImprovements(items) {
        const el = document.getElementById('improvements-list');
        el.innerHTML = '';
        items.forEach(item => {
            const li = document.createElement('li');
            li.className = `improvement priority-${item.priority}`;
            li.innerHTML = `
                <div class="improvement-head">
                    <span class="priority-tag">${escapeHtml(item.priority)}</span>
                    <strong>${escapeHtml(item.title)}</strong>
                </div>
                <p>${escapeHtml(item.description)}</p>
            `;
            el.appendChild(li);
        });
    }

    function renderLineEdits(edits) {
        const el = document.getElementById('line-edits-list');
        el.innerHTML = '';
        edits.forEach(edit => {
            const card = document.createElement('div');
            card.className = 'line-edit';
            card.innerHTML = `
                <div class="line-edit-before"><span class="line-edit-label">Before</span><p>${escapeHtml(edit.before)}</p></div>
                <div class="line-edit-after"><span class="line-edit-label">After</span><p>${escapeHtml(edit.after)}</p></div>
                <p class="line-edit-rationale">${escapeHtml(edit.rationale || '')}</p>
            `;
            el.appendChild(card);
        });
    }

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }
});
