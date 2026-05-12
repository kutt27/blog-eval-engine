# quality-rubrics.md

**Purpose:** Defines objective content standards for structure, readability, and engagement. Used by the evaluation engine to score Dimensions 1, 5, and 6.

## 1. Structural Definitions (Dimension 1)
*The evaluation engine should identify the dominant structure and check for alignment with the chosen format.*

### Inverted Pyramid
*   **Definition:** Leads with the most critical information (the "bottom line" or conclusion), followed by supporting details, and ending with background or minor details.
*   **Criteria:** The core answer or thesis must appear in the first 10% of the text. No "buried ledes."
*   **Best For:** News updates, executive summaries, high-level overviews.

### Storytelling (Narrative Arc)
*   **Definition:** Follows a chronological or logical arc: Setup (Context/Status Quo) → Conflict (Problem/Pain Point) → Resolution (Solution/Takeaway).
*   **Criteria:** Must have a clear inciting incident (the problem), rising action (the investigation/implementation), and a denouement (the result).
*   **Best For:** Case studies, personal experience posts, opinion pieces.

### Problem-Solution
*   **Definition:** Explicitly frames a specific pain point before introducing the tool, method, or concept being discussed.
*   **Criteria:** The problem must be validated (e.g., "If you've ever seen error X...") before the solution is provided.
*   **Best For:** Tutorial introductions, tool reviews, technical deep-dives.

### Listicle / How-To Steps
*   **Definition:** Content broken into numbered or bulleted sequential items.
*   **Criteria:** Items must be mutually exclusive and collectively exhaustive (MECE). Headers should be actionable, not just labels.

## 2. Readability Targets (Dimension 5)
*Metrics based on text analysis. These thresholds adjust based on the selected Audience Persona.*

### Flesch-Kincaid Grade Level Targets
*   **General/Business Audience:** 7.0 – 9.0 (Accessible, clear language)
*   **Technical/Developer Audience:** 10.0 – 13.0 (Allows for complex syntax and technical terminology)
*   **Academic/Research:** 14.0+ (Highly technical, formal structure)

### Sentence & Paragraph Complexity
*   **Average Sentence Length:** 15–20 words. (Flag sentences > 35 words as "too complex" for web reading).
*   **Passive Voice Ratio:** Must be < 15%. (Technical writing allows slightly more passive voice for describing processes, but active voice is preferred for actions).
*   **Paragraph Length:** Maximum 4 sentences or 80 words. Single-sentence paragraphs are acceptable for emphasis or transitions, but not for bulk content.

### Jargon Density Control
*   **Metric:** Count of domain-specific terms per 100 words.
*   **Thresholds:**
    *   *Low Density (< 2/100):* Appropriate for "Beginner" or "Manager" personas.
    *   *Medium Density (3-5/100):* Appropriate for "Mid-level" practitioners.
    *   *High Density (> 5/100):* Only acceptable for "Senior/Expert" personas, **provided** terms are defined on first use or linked to a glossary.

## 3. Engagement Benchmarks (Dimension 6)
*Evaluation of the "stickiness" and user experience of the text.*

### Hook Strength (First 100 Words)
*   **Tier 1 (High):** Opens with a surprising statistic, a provocative question, or a relatable scenario. Immediately establishes "What's in it for me?" (WIIFM).
*   **Tier 2 (Medium):** Clear statement of topic, but lacks emotional or intellectual pull.
*   **Tier 3 (Low):** "In this article, I will discuss..." or lengthy philosophical preamble unrelated to the specific technical problem.

### Time-to-Value (TTV)
*   **Definition:** The word count position where the user receives their first actionable piece of information, code snippet, or key insight.
*   **Target:** Within the first 150 words (typically after the Hook/Intro).
*   **Penalty:** If TTV is > 300 words, flag as "Excessive preamble."

### Call-to-Action (CTA) Clarity
*   **Effective CTA Characteristics:**
    *   **Verb-led:** Starts with an action word (e.g., "Clone," "Download," "Subscribe," "Try").
    *   **Specific:** Describes exactly what happens next (e.g., "Get the starter template" vs. "Click here").
    *   **Contextual:** Placed logically (e.g., CTA for a repo link appears immediately after the code walkthrough, not just at the footer).
*   **Weak CTA:** "Let me know your thoughts in the comments" (too generic, low effort).

### Shareability & Interaction
*   **Tweetable Quote:** Must contain at least one standalone sentence (< 120 characters) that encapsulates a strong opinion or key takeaway.
*   **Comment Prompts:** The engine should check if the post ends with a specific question to the reader (e.g., "How are you handling X in your stack?") rather than a dead-end conclusion.