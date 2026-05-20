# anti-pattern-library.md

**Purpose:** Catalogues common writing mistakes, structural anti-patterns, and engagement killers across blog types. The evaluation engine cross-references detected patterns in the content against these entries to flag issues.

---

## 1. The "In This Article..." Over-Introduction

**Type:** Structure / Engagement
**Affects:** All blog types, especially Tutorials and How-tos

### Symptom
The content opens with 3+ paragraphs of preamble before getting to the actual topic. Common variants:
- "In this article, we will discuss..."
- "Over the past few years, technology X has evolved significantly..."
- "Before we dive in, let's first understand the history of..."

### Why It's Bad
- Violates the "Time-to-Value" (TTV) rule: readers don't get actionable content until word 300+
- Increases bounce rate (especially on mobile where the fold is smaller)
- The Hook rubric expects engagement within the first 100 words

### Detection
- The first 100 words contain no code, no data, no specific claim, and no question
- More than 2 paragraphs before the first H2 or actionable content

### Suggested Fix
- Move the preamble to an optional "Background" section after the hook
- Open with a specific problem statement, statistic, or code snippet

---

## 2. "Magic Step" Omission

**Type:** Technical / Completeness
**Affects:** Tutorials, How-tos, Case Studies

### Symptom
A step in the tutorial assumes intermediate knowledge without declaring it. The author "hand-waves" a complex setup or configuration.

### Examples
- "Now simply configure your Webpack loader..." (without explaining what a loader is or how to configure it)
- "Deploy to your cloud provider of choice..." (without giving specific instructions for any provider)
- "Assuming you have a running Kubernetes cluster..." (in a post targeting beginners)

### Why It's Bad
- The reader gets stuck and cannot proceed
- Creates frustration and erodes trust in the author

### Detection
- Presence of hedge words like "simply," "just," "obviously," "of course" before a technical instruction
- Missing prerequisites section at the top
- Steps that reference external tools without linking to setup instructions

### Suggested Fix
- Add a "Prerequisites" section before Step 1
- Either provide the specific setup steps or link to official documentation
- If a step is complex, break it into sub-steps

---

## 3. "Wall of Text" — No Visual Breaks

**Type:** Readability / Engagement
**Affects:** All blog types, especially educational content

### Symptom
Large, unbroken paragraphs of 8+ sentences or 150+ words. No images, no code blocks, no headings breaking up the text.

### Why It's Bad
- Overwhelming on mobile screens
- Readers lose their place and skim-read, missing key points
- Increases cognitive load

### Detection
- Any paragraph exceeding 5 sentences or 100 words
- More than 300 words of continuous prose without a heading, image, code block, or list

### Suggested Fix
- Break long paragraphs into 2–3 sentence chunks
- Add descriptive subheadings every 200–300 words
- Insert relevant code snippets, diagrams, or screenshots

---

## 4. "Humblebrag" Overwrites

**Type:** Tone / Credibility
**Affects:** Opinion pieces, Case Studies, Reviews

### Symptom
The author spends more time describing their own expertise or credentials than providing useful content. The post becomes a vehicle for self-promotion rather than information.

### Examples
- "At my FAANG company, we solved this by..." (without sharing the actual solution)
- "I've been doing X for 15 years, so trust me when I say..."
- Excessive use of "I," "me," "my" in the problem statement section rather than the conclusion

### Why It's Bad
- Erodes trust rather than building it (readers see through obvious self-promotion)
- Delays the delivery of value to the reader

### Detection
- More than 3 uses of first-person pronouns in the first 200 words that are not part of a specific anecdote
- No technical evidence (code, data, benchmarks) to back up claims of expertise

### Suggested Fix
- Move credentials to a brief author bio at the end
- Lead with the problem and solution, not the author's background

---

## 5. "Fence-Sitting" Conclusion

**Type:** Structure / Purpose Mismatch
**Affects:** Opinion pieces, Comparisons, Reviews

### Symptom
The author presents arguments for both sides but fails to take a definitive stance. The conclusion reads as "it depends" without providing actionable decision criteria.

### Examples
- "Both tools are great for different reasons. It really depends on your needs." (without explaining how to evaluate those needs)
- "Ultimately, you should choose what works best for your team." (vague, no guidance)

### Why It's Bad
- The reader finishes the post without a clear takeaway or decision
- For Comparison posts specifically, this is a structural failure — the purpose is to help the reader decide

### Detection
- Conclusion paragraph lacks a definitive recommendation
- No "Choose X if..." / "Choose Y if..." section in Comparison posts
- Use of "depends," "your mileage may vary," "both are great" without qualification

### Suggested Fix
- Create a decision matrix or "Use X when..." / "Use Y when..." section
- State your recommendation clearly, even if contingent on specific conditions

---

## 6. "Orphaned Code" Anti-Pattern

**Type:** Technical / Completeness
**Affects:** Tutorials, Technical Deep-dives

### Symptom
Code blocks that reference variables, functions, or imports that are not defined anywhere in the post or its prerequisites.

### Examples
- Using `client.query(...)` without showing how `client` was initialized
- Calling `transform(data)` without defining or importing `transform`
- Showing only the "changed lines" in a diff without the surrounding context

### Why It's Bad
- The reader cannot run the code without guessing the missing pieces
- Makes the post feel incomplete or carelessly edited

### Detection
- First code block in a technical post has no preceding imports or setup comments
- Code references identifiers that don't appear earlier in the post or in linked files

### Suggested Fix
- Include the full file or repository link
- Add a comment like `// [1] client initialized on line 15` to reference earlier setup
- If providing diffs, show 2–3 lines of context around each change

---

## 7. "Reply-All" FAQ Placement

**Type:** Structure / UX
**Affects:** Tutorials, How-tos

### Symptom
A Frequently Asked Questions (FAQ) section is placed *before* the main content or tutorial steps.

### Why It's Bad
- The reader hasn't encountered the problems yet, so the FAQ is meaningless noise
- Delays the actual content and increases TTV

### Detection
- FAQ or "Common Issues" section appears before the first H2 or main content section

### Suggested Fix
- Move the FAQ to the end of the post, after the conclusion
- Convert content from the FAQ into inline troubleshooting callouts after the relevant step

---

## 8. "Synonym Shuffle" (Lexical Inconsistency)

**Type:** Clarity / Style
**Affects:** All blog types

### Symptom
The author uses multiple different terms for the same concept within a single post, confusing readers about whether they refer to the same thing.

### Examples
- Switching between "function," "method," "routine," "procedure" for the same concept
- Using "client," "customer," "user," "consumer" interchangeably when they have distinct meanings
- Referring to "Docker," then "containers," then "images," then "Docker containers" without consistency

### Detection
- Multiple synonyms for a key technical term appear within close proximity (within 3 paragraphs)
- The post does not define its terminology early on

### Suggested Fix
- Choose one term and use it consistently throughout
- If multiple terms are technically accurate (e.g., "function" vs "method"), define the distinction early and stick to it
