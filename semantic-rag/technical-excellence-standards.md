# technical-excellence-standards.md

**Purpose:** Establishes non-negotiable quality benchmarks for technical artifacts within a blog post. Used by the evaluation engine to score Dimension 4.

---

## 1. Code Snippet Standards
*The engine will parse markdown code blocks and evaluate them against the following criteria based on the post's stated language/framework.*

### Syntax & Formatting
*   **Language Tagging:** Every code block *must* have a language specifier (e.g., ` ```python `, ` ```javascript `). Untagged blocks ( ` ``` `) receive an automatic penalty.
*   **Linting/Best Practices:** Code should not exhibit obvious anti-patterns (e.g., `var` in modern JS, mutable default arguments in Python). The engine flags code that looks like it was written for an older version of the language unless explicitly discussing legacy systems.

### Runnability & Completeness
*   **No "Magic" Omissions:** Code should not rely on unseen variables or hidden setup. If a snippet requires a 10-line setup, either include it or explicitly state: *"Assuming you have initialized `client` with your API key..."*
*   **Import Statements:** Include necessary imports/dependencies at the top of the first relevant block or clearly state them in the prerequisites.
*   **Pseudo-code Exceptions:** If the code is intentionally pseudo-code, it *must* be explicitly labeled as such. Unlabeled pseudo-code in a tutorial receives a heavy penalty.

### Commenting Quality
*   **The "Why" Rule:** Comments should explain *why* something is being done, not *what* is being done. The code itself shows the "what."
    *   *Poor (Describes What):* `// Loop through the array` -> `[Avoid]`
    *   *Good (Explains Why):* `// Filter out null values to prevent downstream TypeError in the mapping step` -> `[Require]`
*   **Annotation:** Use inline comments (`//` or `#`) to point out specific lines the author is discussing in the prose (e.g., `// [1] This is where the memory leak occurs`).

---

## 2. Visual Aid & Diagram Standards
*Technical concepts often require spatial or visual representation to be understood fully.*

### Architecture / System Diagrams
*   **Requirement:** Any post explaining system design, data flow, or infrastructure *must* include at least one architecture diagram.
*   **Format Preference:** Text-based diagrams using Mermaid.js or PlantUML are highly rated because readers can copy-paste them to render or edit them. High-resolution SVGs or crisp PNGs are acceptable alternatives.
*   **Clarity Check:** Diagrams must have clear boundaries (e.g., dashed lines for VPCs), labeled arrows (e.g., "REST API / JSON"), and a legend if colors/shapes represent different states.

### Screenshots & UI Walkthroughs
*   **Cropping:** Screenshots must be cropped to the relevant window or panel. Full-desktop screenshots (showing the author's browser tabs, clock, and taskbar) are flagged as unprofessional.
*   **Callouts:** Critical UI elements must be highlighted using red boxes, circles, or arrows. 
*   **Text vs. Image:** Do not use a screenshot of a block of text or a short terminal output. Use a code block instead. Screenshots are only for visual layouts, GUIs, or un-copyable environments.

### Contextual Anchoring
*   **No Orphan Images:** Every image must be referenced in the surrounding text. 
    *   *Poor:* `[Image of Dashboard]`
    *   *Good:* `As shown in Figure 1 below, the dashboard highlights the spike in latency...`
*   **Captions:** All images should have a brief caption describing the takeaway, not just the title (e.g., *"Figure 1: CPU usage spikes correlate directly with the batch job kickoff at 00:00 UTC."*)

---

## 3. Example & Evidence Quality
*How the author proves their technical claims.*

### Real-World vs. Hypothetical
*   **Hypothetical (Acceptable but weak):** `const user = { name: "John Doe" };`
*   **Real-World (Strong):** Using a recognizable structure or actual API response shape (e.g., a stripped-down GitHub API payload or a realistic database schema).
*   **Benchmark Rule:** If a post makes a performance claim (e.g., "Library X is 3x faster than Library Y"), it *must* include a methodology section, the hardware specs used, and a reproducible benchmark graph/output.

### Edge Case Coverage
*   **Evaluation Point:** Does the post acknowledge what happens when things go wrong?
*   **Signals of Excellence:** 
    *   Handling empty states (e.g., "What if the API returns an empty array?").
    *   Error handling blocks (`try/catch`, `.catch()`).
    *   Timeouts and retries for network requests.
*   *Note: A tutorial doesn't need to implement every edge case in the primary code block, but it must at least include a "Handling Errors" section or a callout mentioning them.*

---

## 4. Citation & Resource Linking
*Technical writing sits on the shoulders of documentation and prior art.*

### Primary Source Linking
*   **Rule:** When mentioning a library, tool, or specification, link directly to the *official documentation* or *RFC/spec*, not a third-party blog post about it.
    *   *Poor:* Linking to a Medium article about React Hooks.
    *   *Good:* Linking to `react.dev/reference/react`.

### Source Code Availability
*   **Multi-file Penalty:** If a tutorial requires creating 3 or more files (e.g., `index.html`, `styles.css`, `app.js`), the author *must* provide a link to a complete, runnable repository (GitHub, StackBlitz, CodeSandbox). Forcing the reader to assemble 5 separate code blocks is a poor UX.

### "Further Reading" Curation
*   A high-quality post doesn't just drop links; it contextualizes them.
    *   *Poor:* "Here are some links to read: [Link 1] [Link 2]"
    *   *Good:* "To understand the underlying V8 engine optimizations at play here, I highly recommend Vyacheslav Egorov's deep-dive on TurboFan: [Link]"