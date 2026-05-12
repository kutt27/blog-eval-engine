# platform-distribution-rules.md

**Purpose:** Defines platform-specific formatting, length, and structural optimization rules. Used by the evaluation engine to score Dimension 10 and flag content that is poorly formatted for its declared destination.

---

## 1. Medium (The "Digital Magazine")
**Platform Vibe:** Narrative-driven, polished, aesthetic. Readers expect a "story" even if the topic is technical.
**Optimal Length:** 5–8 minute read (~1,200 – 1,800 words).

### Structural Rules
*   **The Subtitle is King:** Medium often shares the subtitle (not the title) on social feeds. It must be a standalone hook. *Engine Check: Flag if subtitle is missing or is just a repeat of the title.*
*   **Pull Quotes:** Must use the Medium `>` blockquote formatting for 1-2 "tweetable" insights midway through the article to break up text and capture scrollers.
*   **Code Block Strategy:** Medium's code block styling is notoriously basic. *Rule:* If a post has > 3 code blocks, the author should be using GitHub Gists embedded via URL, rather than native markdown blocks.
*   **The "Clap" CTA:** A soft, contextual CTA at the end ("If you found this helpful, leave a clap...") is standard and expected. 

### Engine Penalty Triggers
*   Raw, unstyled JSON or wide tables that break out of the content container.
*   "Medium-optimal" keywords stuffed awkwardly into the first paragraph (hurts the narrative feel).

---

## 2. Dev.to (The "Developer Watercooler")
**Platform Vibe:** Community-driven, practical, code-first, highly skimmable.
**Optimal Length:** 3–5 minute read (~700 – 1,200 words).

### Structural Rules
*   **Tag Strategy:** Dev.to relies heavily on tags for reach. The top 4 tags must be highly relevant. *Engine Check: Ensure the primary tag matches the core technology discussed in the code blocks.*
*   **Liquid Tag Utilization:** Instead of standard markdown links, high-performing Dev.to posts use platform-specific "Liquid Tags" (e.g., `{% github repo_name %}`, `{% youtube video_id %}`).
*   **The "Discussion" Handoff:** Because comments drive the Dev.to algorithm, posts must end with an explicit, highly specific question to the community.
    *   *Good:* "What's your preferred state management pattern in 2024? Let me know in the comments."
    *   *Bad:* "Thanks for reading."

### Engine Penalty Triggers
*   Long, theoretical introductions without a code block in the first 20% of the text (violates community expectations of TTV).
*   Failing to mention an alternative approach (Dev.to readers love pointing out flaws; preempting this in the post improves its reception).

---

## 3. LinkedIn (The "Professional Network")
**Platform Vibe:** Business-oriented, personal branding, high-level takeaways.
**Optimal Length:** 500–1,000 words max (Shorter is almost always better).

### Structural Rules
*   **The "Broetry" Format:** LinkedIn's rendering requires single-sentence paragraphs. Large blocks of text are visually punishing on mobile. *Engine Check: Flag any paragraph > 3 sentences as a LinkedIn formatting error.*
*   **The "See More" Hook:** The first two lines must create an information gap so the user clicks "See more". Starting with a bold claim or contrarian statement is required.
*   **Zero Heavy Code:** Native LinkedIn does not support syntax-highlighted code blocks. *Rule:* Code snippets must be converted to screenshots of the IDE/Terminal, or the post must link out to a personal blog/Dev.to for the code.
*   **Whitespace as Punctuation:** Empty lines between almost every sentence to create breathing room.

### Engine Penalty Triggers
*   Deep, line-by-line code tutorials (wrong platform).
*   Preachy or overly casual tone that doesn't fit a professional network.
*   Missing a "I wrote a more detailed breakdown here: [Link]" CTA if the topic is highly technical.

---

## 4. Personal Blog / SEO Destination (The "Owned Real Estate")
**Platform Vibe:** Authoritative, comprehensive, search-optimized, evergreen.
**Optimal Length:** 1,500 – 3,000+ words (Deep dives).

### Structural Rules
*   **Strict H-Tag Hierarchy:** H1 (Title, only one), H2 (Main sections), H3 (Subsections). *Engine Check: Flag any skipping (e.g., H1 straight to H3).*
*   **Table of Contents (ToC):** Mandatory for posts > 1,500 words. Should be generated from H2s and link to anchors.
*   **Internal Linking:** Must contain a minimum of 2-3 internal links to other posts on the author's site to reduce bounce rate and build site authority.
*   **Alt-Text on Every Image:** Strict accessibility and SEO requirement.
*   **The Newsletter CTA:** Must have a contextual inline CTA (e.g., halfway through the post) and a footer CTA. "Subscribe" is not enough; must offer value ("Subscribe for weekly systems design deep-dives").

### Engine Penalty Triggers
*   Orphaned posts (no internal links pointing to the article, and no internal links pointing out).
*   Missing meta-description or SEO title optimization (if the user specifies SEO as a goal).

---

## 5. Hacker News (The "Academic Arena")
**Platform Vibe:** Highly critical, technical, anti-marketing, intellectual.
**Optimal Length:** No strict limit, but "fluff-per-word" ratio must be near zero.

### Structural Rules
*   **Factual, Dry Titles:** HN actively downvotes clickbait. Titles must be strictly declarative. *Engine Check: Flag adjectives like "Amazing," "Revolutionary," or "Why I Love..." in the title.*
*   **Text vs. Link:** If submitting a link to an external blog, the HN text post usually just contains a brief quote from the article. If writing a self-post (Ask HN, Show HN), it must lead with the core technical innovation or the exact problem being solved.
*   **Assume Expertise:** No introductory definitions of basic concepts (e.g., do not explain what an API is). 
*   **No Images/Diagrams:** HN text posts do not render images. If a post relies heavily on a diagram to make its point, it will fail on HN unless linked externally.

### Engine Penalty Triggers
*   Any perceived self-promotion or "hustle culture" language.
*   Submitting a listicle or superficial overview.

---

## Engine Logic: Platform Mismatch Detection (Dimension 10 Scoring)

The evaluation engine will apply a **Platform Alignment Multiplier** to the final score based on these checks:

*   **Code Block Distribution:** If the post contains > 40% code blocks and the target is `LinkedIn`, the alignment score drops to 0.
*   **Paragraph Length:** If the average paragraph is > 4 lines, and the target is `LinkedIn`, the formatting score drops by 50%.
*   **Hook Style:** If the first sentence is a question or bold claim (optimized for LinkedIn/Medium), but the target is `Personal Blog/SEO`, flag it as "Missing SEO-optimized introductory keywords."
*   **Link Density:** If the post contains no outbound links and the target is `Hacker News`, flag as "Lacks external citations expected by HN audience."