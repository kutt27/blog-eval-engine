Here is the extension file for your neuroscience and psychology writing. This is designed to plug directly into your evaluation engine as a specialized structural overlay.

***

# science-hierarchy-rules.md

**Purpose:** Establishes strict semantic rules for hierarchical knowledge transfer in neuroscience, computational neuroscience, cognitive psychology, and biopsychology. Used by the evaluation engine to enforce a "bottom-up" explanatory architecture, ensuring complex phenomena are built upon foundational mechanisms.

---

## 1. The Core Principle: The Reductionist Ladder
*In technical writing, you can often start with the "What" (a high-level overview). In neuro/cognitive science writing, starting at the top without establishing the bottom leads to "neuro-babble" or magical thinking. The reader must climb the ladder.*

### The Three Tiers
The engine will classify concepts into three distinct tiers. A high-quality post must explicitly connect these tiers in ascending order.

*   **Tier 1: Micro / Biological (The "How" at a cellular level)**
    *   *Keywords/Concepts:* Action potentials, ion channels, synapses, neurotransmitters (dopamine, serotonin, glutamate), receptors, gene expression, glial cells, molecular pathways.
*   **Tier 2: Meso / Systems (The "Where" and "Wiring")**
    *   *Keywords/Concepts:* Neural circuits, brain regions (e.g., Amygdala, Hippocampus, Prefrontal Cortex), functional connectivity, network models, pathways (e.g., mesolimbic pathway), local field potentials, fMRI/EEG correlates.
*   **Tier 3: Macro / Cognitive-Behavioral (The "What" and "Why")**
    *   *Keywords/Concepts:* Working memory, executive function, emotional regulation, learning, behavioral disorders, consciousness, perception, cognitive biases.

---

## 2. The "Hierarchical Bridge" Rule (Crucial)
*The most common failure in science writing is leaping from Tier 1 directly to Tier 3, or vice versa, without explaining the bridge (Tier 2).*

**Rule:** Whenever a Tier 1 mechanism and a Tier 3 behavior appear in the same paragraph or section, the engine *must* look for a Tier 2 bridge.

*   **Failure (Missing Bridge):** "Dopamine is responsible for the pleasure we feel when we achieve a goal." *(Jumps from Neurotransmitter [T1] directly to Subjective Experience [T3]).*
*   **Success (Bridged):** "Dopamine release [T1] within the mesolimbic pathway, specifically projecting to the nucleus accumbens [T2], creates a predictive reward signal that our conscious brain interprets as motivation or pleasure [T3]."

---

## 3. Structural Progression Standards
*How the bottom-up flow should physically look in the post.*

### Phase A: Grounding (Establishing Tier 1)
*   Define the biological substrate first.
*   Explain the *physical constraints* (e.g., "Because neurons have a refractory period, they cannot fire faster than 1000Hz..."). This grounds the reader in physical reality before abstracting it.

### Phase B: Network Integration (Building Tier 2)
*   Scale up from the single cell to the circuit.
*   Use spatial language ("projections to," "inhibits," "excites," "loops back to").
*   **Requirement for CompNeuro:** If the post is computational, this is where the mathematical model or algorithm is introduced. The math *is* the Tier 2 bridge between biological neurons (T1) and cognitive output (T3).

### Phase C: Emergence (Reaching Tier 3)
*   Explicitly use emergence language: "results in," "gives rise to," "manifests as," "can be observed behaviorally as."
*   This is the only phase where subjective experience (qualia) or complex psychological terms should be used.

---

## 4. Domain-Specific Nuances

### Computational Neuroscience Specifics
*   **The Abstraction Ladder:** In CompNeuro, the hierarchy is often: *Biological Neuron -> Integrate-and-Fire Model -> Hopfield Network -> Cognitive Simulation.*
*   **Rule:** The author must state *where* on the abstraction ladder their model sits. A post is penalized if it presents a highly abstracted neural network (e.g., a basic CNN) as a direct equivalent of human visual processing without defining the biological simplifications made.

### Cognitive Psychology Specifics
*   **The Reverse-Justification:** Sometimes, cognitive psych starts with the behavior (Tier 3) and works backward to hypothesize the mechanism.
*   **Rule:** If the post starts with a cognitive phenomenon (e.g., "The Stroop Effect"), it must immediately transition to the hypothesized neural basis (Tier 2/1). It cannot linger on Tier 3 descriptions without anchoring them in biology or computational models.

### Biopsychology Specifics
*   **The Gene-Environment Interaction:** Biopsychology requires a dual-ladder approach.
*   **Rule:** If discussing a disorder (e.g., depression), the engine must check for both the bottom-up biological explanation (e.g., HPA-axis dysregulation) AND the top-down environmental input (e.g., chronic stress), synthesizing them into a feedback loop.

---

## 5. Engine Evaluation Checks & Penalty Triggers

### Semantic Check: "Neuro-Fluff" Detection
*   **Trigger:** Using neuro-terminology as a buzzword to sound scientific without adding mechanistic value.
*   **Example:** "Your brain lights up when you see a sunset." (Vague, unscientific).
*   **Required Fix:** "Visual processing in the occipital lobe [T2] processes the high-contrast gradients of a sunset, sending signals to the limbic system [T2] which triggers an emotional response [T3]."

### Structural Check: "Top-Heavy" Post
*   **Trigger:** The post spends > 60% of its word count on cognitive/behavioral descriptions (Tier 3) and crams all the neurobiology into one paragraph at the very end as an "afterthought."
*   **Fix:** The engine should suggest restructuring to interleave the tiers, or moving the biological grounding to the introduction.

### Structural Check: "Lost in the Weeds"
*   **Trigger:** The post spends > 70% of its word count on Tier 1 molecular biology and never connects it to a cognitive function or behavior (Tier 3).
*   **Fix:** Flag as "Missing the Cognitive Payoff." Remind the author: *Why does this molecular mechanism matter to the reader's understanding of the mind?*

### Formatting Check: Ontology Mapping
*   **High-Score Signal:** The post includes a visual or text-based hierarchy map early on (e.g., "In this post, we will trace how a genetic mutation [T1] alters a receptor [T1], changes circuit dynamics in the prefrontal cortex [T2], and ultimately results in working memory deficits [T3].")
*   **Why this works:** It gives the reader the map before making them walk the path.
