# blog-type-blueprints.md

**Purpose:** Provides structural "maps" and evaluation checklists for specific content types, and validates if the structure serves its intended purpose. Used by the evaluation engine to score Dimensions 7 and 9.

---

## Part 1: Blog-Type Specific Rubrics (Dimension 9)
*The engine will attempt to auto-detect the blog type based on structural markers (e.g., presence of a feature matrix = Comparison). If the user-selected type does not match the detected structure, a "Structural Mismatch" warning is issued.*

### 1. The Tutorial (Step-by-Step Guide)
**Goal:** Guide a user from Point A to Point B without getting stuck.
**Required Structural Elements:**
*   **Prerequisites Block:** Explicitly listed before Step 1 (e.g., "Node v18+", "Basic SQL knowledge").
*   **Expected Outcome:** A brief description or screenshot of what the user will have built by the end.
*   **Sequential Steps:** Numbered lists. Each step should represent a single, atomic action.
*   **Verification/Testing Step:** A dedicated step near the end to prove it worked (e.g., "Run `npm test`," "Visit `localhost:3000`").
*   **Troubleshooting Section:** A "Common Pitfalls" or "FAQ" block addressing frequent errors.

**Engine Penalty Triggers:**
*   Skipping steps (e.g., Step 1: Create DB. Step 2: Query DB. *Wait, how did the tables get there?*).
*   No way to verify success.
*   "Magic hand-waving" (e.g., "Now simply configure your OAuth provider...").

### 2. The Comparison (X vs. Y)
**Goal:** Help the reader make a purchasing or architectural decision.
**Required Structural Elements:**
*   **Context/Introduction:** Why are we comparing these two specifically? (e.g., "Both are NoSQL databases, but they serve vastly different use cases").
*   **Feature Matrix:** A table comparing key attributes (Pricing, Language, Performance, Learning Curve).
*   **Use-Case Mapping:** "Choose X if...", "Choose Y if..." sections.
*   **The "Nuance" Section:** Acknowledging that neither is objectively "best" and highlighting hidden trade-offs.

**Engine Penalty Triggers:**
*   Comparing apples to oranges without context (e.g., comparing a full framework to a lightweight library without noting the difference).
*   Missing pricing or licensing comparisons.
*   A clear winner declared without backing up *why* it wins for specific scenarios.

### 3. The Opinion / Editorial
**Goal:** Present a subjective viewpoint, challenge the status quo, or provoke thought.
**Required Structural Elements:**
*   **Clear Thesis Statement:** The core argument must be stated in the first 10% of the post (e.g., "TypeScript is slowing down your prototyping phase and here is why").
*   **Supporting Pillars:** 3-5 distinct points that support the thesis.
*   **The "Steel Man" Counterpoint:** Acknowledging the strongest argument *against* the thesis, treating it fairly, and then explaining why the author still holds their position.
*   **Conclusive Stance:** Reiterating the thesis in the conclusion, often with a call to action or a thought-provoking question.

**Engine Penalty Triggers:**
*   "Straw man" arguments (misrepresenting the opposing side to easily defeat it).
*   Stating an opinion as an absolute fact without evidence or anecdotal backing.
*   Fence-sitting (failing to actually take a stance by the end of the article).

### 4. The Review (Tool / Product)
**Goal:** Evaluate a specific tool based on defined criteria.
**Required Structural Elements:**
*   **Scoring Criteria:** Defined upfront (e.g., "I will be scoring this on Performance, DX, and Pricing").
*   **The "First 5 Minutes" Experience:** Describing the onboarding, installation, or initial setup.
*   **Balanced Pros & Cons:** Explicitly listed lists. A review with no cons is flagged as biased/untrustworthy.
*   **The Verdict:** A final summary of who the tool is actually for.

**Engine Penalty Triggers:**
*   Reading like a rewritten press release.
*   Failing to mention competing tools that do it better/faster/cheaper.

### 5. The News / Update (Changelog / Release)
**Goal:** Inform the audience about a change in the ecosystem.
**Required Structural Elements:**
*   **The TL;DR:** A 1-2 sentence summary of the news.
*   **Context (Before vs. After):** What was broken/slow/missing before this update?
*   **Deep-dive on "What's New":** Explaining the *mechanics* of the update, not just the feature name.
*   **Impact Analysis:** How does this break existing code? What does the migration path look like?

**Engine Penalty Triggers:**
*   Just copy-pasting the official changelog without adding value or context.
*   Missing the "Why should the reader care?" element.

---

## Part 2: Purpose-Driven Evaluation (Dimension 7)
*Once the blog type is identified, the engine checks if the structure actually serves the selected Primary Purpose.*

### Purpose: EDUCATE
*   **Focus:** Clarity, learning curve management, knowledge retention.
*   **Structural Markers:** Summaries at the end of sections, progressive disclosure of complex information (start simple, add complexity), analogies for abstract concepts.
*   **Success Metric:** Can a reader accurately explain the concept back after reading?

### Purpose: PERSUADE
*   **Focus:** Argument strength, evidence quality, emotional/logical appeal.
*   **Structural Markers:** Strong data points, authoritative citations, addressing and dismantling objections early (pre-empting dissent).
*   **Success Metric:** Does the text change a neutral reader's perspective?

### Purpose: CONVERT
*   **Focus:** Funnel alignment, frictionless next steps, value demonstration.
*   **Structural Markers:** Agitate a painful problem -> Present the tool/solution as the painkiller -> Clear, contextual CTA. No "bait and switch" (the product should be introduced organically, not hidden until the end).
*   **Success Metric:** Is the CTA a logical next step based on the problem discussed?

### Purpose: DOCUMENT (Reference)
*   **Focus:** Completeness, accuracy, scannability.
*   **Structural Markers:** Extensive use of tables, parameter lists, return types. Minimal prose. Search-optimized headings.
*   **Success Metric:** Can a developer find the exact syntax they need in under 10 seconds?

---

## Part 3: Engine Logic - Purpose vs. Type Mismatch

The evaluation engine will apply a heavy penalty if the Purpose and Type contradict each other structurally:

*   **Mismatch Example 1:** User selects Purpose = *Educate*, but Blog Type = *Opinion*. (Opinions are poor vehicles for objective education).
*   **Mismatch Example 2:** User selects Purpose = *Document*, but Blog Type = *Storytelling*. (Narrative arcs actively harm the scannability required for reference documentation).
*   **Mismatch Example 3:** User selects Purpose = *Convert*, but Blog Type = *Comparison* where the author's product is not included or is unfairly favored without a matrix. (Fails the trust requirement for conversion).