# seo-meta-rubrics.md

**Purpose:** Defines SEO optimization standards for blog content, including keyword strategy, meta descriptions, heading placement, internal linking, and content structure for search visibility.

---

## 1. Keyword Strategy & Density

### Primary Keyword Placement
*   **Rule:** The primary keyword or phrase must appear in the first 100 words of the content (ideally within the first paragraph).
*   **Engine Check:** Detect if the primary keyword (inferred from title/H1) appears in the opening section. If not, flag as "Late keyword introduction — hurts search snippet relevance."

### Keyword Density Targets
*   **General SEO Best Practice:** 1–3% keyword density (primary keyword appears 1–3 times per 100 words).
*   **Over-Optimization Threshold:** > 5% keyword density triggers a "Keyword stuffing" warning.
*   **Under-Optimization Threshold:** < 0.5% keyword density triggers a "Missing keyword focus" flag.

### Secondary & LSI Keywords
*   **Rule:** Content should include 2–4 semantically related terms (LSI keywords) naturally in subheadings and body.
*   **Example:** If the primary keyword is "React performance," LSI keywords might include "virtual DOM," "re-rendering," "memoization," "React.memo."
*   **Engine Check:** If the content only repeats the exact primary keyword without any semantic variation, flag as "Narrow keyword scope — lacks topical depth."

---

## 2. Meta Data Optimization

### Title Tag (H1) Quality
*   **Length Target:** 50–60 characters to avoid truncation in SERPs.
*   **Formula:** Primary Keyword + Value Proposition or Hook (e.g., "React Performance: 7 Proven Strategies to Cut Load Time by 60%").
*   **Engine Penalty:** Titles under 20 characters or over 70 characters. Titles that do not contain the primary keyword.

### Meta Description Readiness
*   **Length Target:** 120–158 characters.
*   **Required Elements:**
    *   Contains primary keyword (preferably near the beginning).
    *   Includes a call-to-action or value statement ("Learn how," "Discover," "Step-by-step guide").
    *   Unique to the page (not a generic tagline).
*   **Engine Check:** The first 1–2 sentences of the blog post serve as the *de facto* meta description on many platforms. If the opening is generic (e.g., "In this article, we will discuss..."), flag as "Weak meta description — rewrite opening paragraph."

### URL Slug Quality
*   **Rule:** The slug should be a hyphenated, lowercase version of the primary keyword. Remove stop words (the, a, an, of, in).
*   **Good:** `/react-performance-optimization-tips`
*   **Bad:** `/blog/post123` or `/how-to-optimize-react-performance-in-2024-a-comprehensive-guide`

---

## 3. Heading Hierarchy for SEO

### H1 Usage
*   **Rule:** Exactly one H1 per page. Must match or closely relate to the title tag.
*   **Engine Check:** Multiple H1s or missing H1.

### H2 Subheadings
*   **Rule:** H2s should contain primary keywords or close variants. Each H2 should represent a distinct topical section.
*   **Keyword-per-H2 Ratio:** Aim for at least 50% of H2s to include a keyword variant.
*   **Engine Check:** If no H2 contains the primary keyword or a close variant, flag as "Missing keyword in subheadings — weak topical structure."

### H3+ Subsections
*   **Rule:** H3s should only appear under an H2 (never directly under H1).
*   **Engine Check:** H3 appearing without a preceding H2 → "Broken heading hierarchy."

---

## 4. Content Structure for Featured Snippets

### "People Also Ask" Optimization
*   **Rule:** Include 1–2 direct question-answer pairs in the content (e.g., "What is X?" followed by a concise 2–3 sentence answer).
*   **Format:** Use H2 or H3 for the question; answer immediately in plain text (not in a list or code block).
*   **Benefit:** Increases chances of being pulled into a "People Also Ask" box.

### List & Table Detection
*   **Rule:** Bullet lists and numbered steps are favored for "List" featured snippets. Comparison tables are favored for "Table" snippets.
*   **Engine Check:** If the content is a "How-to" or "Comparison" type but lacks any bullet/numbered list or table, flag as "Missing list format — missed snippet opportunity."

---

## 5. Internal & External Linking

### Internal Link Density
*   **Target:** 2–5 internal links per 1,000 words.
*   **Rule:** Links should point to relevant, topically related content on the same domain. Avoid linking to the same page twice.
*   **Engine Check:** Content with zero internal links → "Orphaned content — no internal linking."

### Outbound Link Quality
*   **Rule:** Link to authoritative, high-DA sources for claims, statistics, and citations. Link directly to official documentation, not third-party summaries.
*   **Rule:** Use descriptive anchor text (not "click here" or "read more").
*   **Engine Check:** More than 30% of outbound links using generic anchor text → "Weak link context — improve anchor text."

---

## 6. Readability & SEO

### Flesch-Kincaid for SEO
*   **Target Grade Level by Topic:**
    *   General audience: 7–9
    *   Technical/B2B: 10–13
    *   Academic: 14+
*   **Note:** Readability does not directly affect rankings but impacts bounce rate and dwell time, which are correlated with SEO performance.

### Paragraph Length
*   **Target:** Max 3–4 sentences or 80 words per paragraph. Shorter paragraphs improve mobile readability and reduce bounce rate.

---

## 7. Image & Media SEO

### Alt Text Requirements
*   **Rule:** Every image must have a descriptive alt text containing the primary keyword where relevant.
*   **Engine Check:** Missing alt text on any image → "Accessibility & SEO gap — missing image alt text."

### File Naming
*   **Rule:** Image filenames should be descriptive and hyphenated (e.g., `react-performance-chart.png` not `IMG_0421.jpg`).
