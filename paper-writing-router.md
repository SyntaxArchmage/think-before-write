# Paper Writing Skill Router

Quick reference for which skill handles what. When multiple could apply, follow this priority.

## Decision Tree

1. Is this about **paper structure** (contributions, sections, paragraph ordering)?
   → `paper-storyline`

2. Is Layer 3 **unconfirmed** for the target section?
   → `paper-storyline` (confirm L3 first, then hand off)

2.5. Is this about **figures, diagrams, or plots**?
   → `figure-generation.mdc` (not a skill, a rule)

3. Is this about **writing prose, QC, numbers, or de-AI**?
   → `academic-writing`

4. Is this a **simulated review, submission gate, or rebuttal**?
   → `paper-review`

5. Does the user want **strategic advice from multiple professors**?
   → `author-supervisor` (embedded within current skill, not standalone)

6. Is the request about **data auditing, numbers consistency, or claim checking**?
   → `academic-writing` (Numbers Triangle + scripts)

## Common Ambiguous Phrases

| User says | Route to | Why |
|---|---|---|
| "Help me improve this paragraph" | `academic-writing` (Track B) | Prose improvement = L4/L5 |
| "Review my intro" | `academic-writing` if QC; `paper-review` if user says "as a reviewer" | Default: academic-writing |
| "Is this compelling?" | `author-supervisor` (5 professors) | Strategic judgment |
| "Would reviewers accept this?" | `paper-review` | Simulated PC |
| "What should I lead with?" | `author-supervisor` (5 professors) | Emphasis/positioning |
| "Rewrite this section" | `paper-storyline` if L3 not confirmed; `academic-writing` if L3 confirmed | Check state first |
| "Rewrite this section" (L3 unconfirmed) | `paper-storyline` | Must confirm L3 before any rewrite |
| "Generate a figure for..." | `figure-generation.mdc` | Not a writing task |
| "Run preflight" / "check before submission" | `paper-review` (review_preflight.sh) | Submission gate |
| "Check my numbers" | `academic-writing` (check-numbers.py) | Numbers Triangle |
