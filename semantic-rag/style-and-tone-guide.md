# style-and-tone-guide.md

**Purpose:** Defines linguistic consistency rules, tone profiles, and voice mechanics. Used by the evaluation engine to score Dimension 3 and ensure the writing style matches the stated intent and audience.

---

## 1. Tone Profiles
*The evaluation engine will analyze word choice, sentence structure, and punctuation to classify the post's dominant tone. A high-scoring post maintains a single dominant tone without unintentional drift.*

### Authoritative
**Vibe:** Confident, decisive, expert. The writer is a subject matter authority who has "been there, done that."
*   **Characteristics:** Uses definitive statements. Avoids weak modifiers ("very," "really," "I think"). Uses imperatives for instructions.
*   **Do this:** "Kubernetes solves container orchestration at scale. Deploying a multi-node cluster requires three core components."
*   **Don't do this:** "Kubernetes is a really great tool that I think solves container orchestration. You might want to consider deploying a cluster, which usually requires a few components."

### Conversational
**Vibe:** Friendly, approachable, peer-to-peer. Like a senior dev explaining something over coffee.
*   **Characteristics:** Uses second-person ("you"), contractions ("don't," "it's"), and occasional rhetorical questions. Sentence lengths vary.
*   **Do this:** "We've all been there: it's Friday at 5 PM, and your latest merge just broke production. Let's roll up our sleeves and fix it."
*   **Don't do this:** "Software developers frequently experience production failures on Friday afternoons. The following methodology outlines a remediation strategy."

### Skeptical / Critical
**Vibe:** Analytical, questioning, hype-averse. Focuses on tradeoffs and hidden costs.
*   **Characteristics:** Uses contrastive conjunctions ("however," "but," "despite"). Acknowledges marketing claims but demands evidence. Highlights limitations.
*   **Do this:** "While the documentation promises 'zero-downtime deployments,' our benchmarks revealed a 300ms latency spike during the health check phase."
*   **Don't do this:** "This tool promises zero-downtime deployments, and it is amazing and works perfectly."

### Professional / Formal
**Vibe:** Polished, objective, corporate-safe.
*   **Characteristics:** Third-person perspective, strict adherence to grammar rules, absence of slang or colloquialisms.
*   **Do this:** "The migration to a microservices architecture resulted in a 15% reduction in deployment times and improved system fault isolation."
*   **Don't do this:** "We chopped the monolith into microservices and now deploying is a breeze."

### Enthusiastic
**Vibe:** Energetic, optimistic, evangelist.
*   **Characteristics:** Uses strong adjectives ("incredible," "game-changing"), exclamation points (used sparingly but effectively), and focuses on the "cool factor."
*   **Do this:** "The new Rust compiler macros are an absolute game-changer. You can eliminate entire classes of memory bugs before they even compile!"

---

## 2. Voice Rules: Active vs. Passive Voice
*The engine will run syntax analysis to determine the ratio of passive to active sentences. Default target: **> 85% Active Voice (< 15% Passive).***

### Active Voice (Default Standard)
**Rule:** The subject of the sentence performs the action.
*   **Example:** "The database query retrieves the user records."
*   **Why it scores well:** Direct, easier to read, clearly assigns responsibility for the action (crucial in technical troubleshooting).

### Passive Voice (Acceptable Exceptions)
**Rule:** The subject receives the action. While generally discouraged, passive voice is acceptable *only* in these specific technical contexts:
1.  **Describing system processes where the actor is irrelevant:**
    *   *Acceptable:* "The data is serialized into JSON and sent over the wire." (We don't care *who* or *what* serializes it, just that it happens).
2.  **Focusing on the object of an error or state change:**
    *   *Acceptable:* "The pipeline was blocked due to a missing dependency."
3.  **Softening bad news or avoiding blame (Post-mortems):**
    *   *Acceptable:* "A configuration error was introduced during the rollout."

---

## 3. Jargon Density & Integration Rules
*Jargon isn't inherently bad, but its *management* is what the engine evaluates.*

### Rule 1: Definition on First Use
If a term is specific to a niche (e.g., "Idempotency," "Memoization," "Sidecar pattern"), it must be briefly defined or contextualized the first time it appears.
*   **Failure:** "We achieve idempotency by using a UUID."
*   **Success:** "We achieve idempotency—meaning the same request can be made multiple times without changing the result—by using a UUID."

### Rule 2: Context Over Dictionary
Do not just link to an external glossary or Wikipedia page. Provide an inline micro-context.
*   **Failure:** "This utilizes a DAG (https://en.wikipedia.org/wiki/Directed_acyclic_graph)."
*   **Success:** "This utilizes a DAG (Directed Acyclic Graph), meaning the workflow flows in one direction without looping back on itself."

### Rule 3: Lexical Consistency (Terminology Lock-in)
Once a technical term is introduced, the engine will check for inconsistent synonym swapping, which confuses readers.
*   **Failure (Inconsistent):** Introducing "function," then calling it a "method," then a "sub-routine," then a "procedure" in the same post.
*   **Success (Consistent):** Sticking to "function" throughout (unless technically distinguishing between a function and a method).

---

## 4. Consistency Checks (Tone Drift Detection)
*The engine will segment the blog post (Intro, Body, Conclusion) and compare tone markers.*

*   **Hook-to-Body Drift:** Opening with a highly Conversational/Enthusiastic hook ("Let's dive into the crazy world of WebSockets!"), but shifting to a dry, Academic tone in the body ("WebSocket protocols facilitate full-duplex communication channels over a single TCP connection...").
*   **Penalty Trigger:** If the semantic sentiment analysis detects a > 30% variance in tone markers between the first 10% and the final 50% of the text, flag as "Tone Inconsistent."