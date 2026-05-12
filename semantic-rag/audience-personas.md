# audience-personas.md

**Purpose:** Defines target reader profiles, their expectations, and the evaluation criteria used to determine if a blog post successfully serves its intended audience. Used by the evaluation engine for Dimension 2.

---

## 1. The Developer (Practitioner / Engineer)
**Core Desire:** "How do I implement this right now, and how will it perform in production?"
**Learning Goal:** Implementation guide, Quick reference, Deep-dive expert content.

### What They Value
*   **Code-to-Text Ratio:** High. They skim prose to find the code blocks.
*   **Practicality:** Real-world scenarios over theoretical math or academic concepts.
*   **Completeness:** Code snippets that are runnable (copy-pasteable), not pseudo-code.
*   **Edge Cases:** Mentions of performance bottlenecks, memory leaks, or security implications.
*   **Directness:** No fluff. Get to the point.

### Evaluation Signals (What the Engine Looks For)
*   Presence of multiple, well-formatted code blocks.
*   Links to GitHub repositories, Sandboxes (CodeSandbox, StackBlitz), or playgrounds.
*   Use of terminal output/logs to prove the code works.
*   Low "Time-to-Value" (TTV) – actionable content should appear within the first 150 words.

### Red Flags (Penalty Triggers)
*   Long philosophical introductions about "the future of tech" before showing any syntax.
*   Code snippets missing imports, type definitions, or setup steps.
*   Over-explaining basic concepts (e.g., explaining what a variable is to a senior backend developer).

---

## 2. The Manager / Decision-Maker
**Core Desire:** "Why should we care about this, what are the tradeoffs, and what is the business impact?"
**Learning Goal:** Conceptual overview, Deep understanding (of business value).

### What They Value
*   **The "So What?":** Immediate translation of technical features into business outcomes (e.g., "Reduces latency by 40%, improving user retention").
*   **High-Level Visuals:** Architecture diagrams, flowcharts, and comparison matrices. They rarely read code blocks.
*   **Cost/Risk Analysis:** Discussions on pricing, vendor lock-in, migration effort, or maintenance overhead.
*   **Brevity:** Bullet points, executive summaries, and bolded key takeaways.

### Evaluation Signals (What the Engine Looks For)
*   Clear thesis statements aligning technology with ROI, efficiency, or risk mitigation.
*   Presence of charts (pie charts, bar graphs) or architectural block diagrams.
*   "Pros and Cons" or "When to use / When to avoid" sections.
*   Flesch-Kincaid grade level between 7.0 and 9.0 (accessible, jargon-light).

### Red Flags (Penalty Triggers)
*   Untranslated acronyms or deep technical jargon without plain-English definitions.
*   Buried ledes (making them read 3 paragraphs before knowing what the technology does).
*   Lack of context (e.g., introducing a new framework without explaining *why* it's better than the current industry standard).

---

## 3. The Student / Beginner
**Core Desire:** "How does this work from the ground up? Please don't assume I know anything."
**Learning Goal:** Deep understanding, Conceptual overview, Educate.

### What They Value
*   **Mental Models:** Analogies and metaphors that map technical concepts to everyday life.
*   **The "Why" Before the "How":** Explaining the underlying problem before presenting the solution.
*   **Explicit Prerequisites:** Clear statements like, "Before starting, you should know basic HTML and how to open a terminal."
*   **Micro-Steps:** Granular, numbered instructions where no step is skipped.
*   **Encouragement:** A friendly, supportive tone that acknowledges the learning curve.

### Evaluation Signals (What the Engine Looks For)
*   Inclusion of analogies (e.g., "Think of a Docker container like a shipping container...").
*   Extremely low jargon density; any jargon used must be immediately defined.
*   Short paragraphs (max 3-4 sentences) to prevent visual overwhelm.
*   Screenshots of UI elements or IDEs (e.g., "Click the green 'Run' button in the top right").

### Red Flags (Penalty Triggers)
*   "Magic steps" (e.g., "Now simply configure your Webpack loader..." without explaining what Webpack is or how to do it).
*   Condescending tone or passive-aggressive language ("Obviously," "As everyone knows").
*   High Flesch-Kincaid scores (above 10.0) indicating overly complex sentence structures for a beginner.

---

### Engine Logic: Persona Mismatch Detection
The evaluation engine will flag a **Persona Mismatch** if the following occurs:
*   *Text signals Developer intent* (high code ratio, GitHub links) *but targets Beginner persona* (high Flesch-Kincaid, lack of prerequisites).
*   *Text signals Manager intent* (high-level overview, ROI mentions) *but includes 200 lines of raw code* without a high-level summary wrapper.
*   *Text targets Student persona* *but assumes prior knowledge of adjacent technologies* without listing them.