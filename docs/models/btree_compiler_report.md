# B+ Tree and Compiler Pipeline — Replacement & Status Report (§7.4)

**Specification:** `PRISMED_AGENT_FIX_BTREE_COMPILER.md` (§7.4)  
**Date:** 2026-10-29  
**Target:** Final Outcome for `database-b-tree` (DBT-01) and `compiler-pipeline` (CP-01)  

---

## 1. Summary of Actions Taken

In accordance with Section 0 and Section 1 of the brief:
1. **Deleted the two rejected models:**
   - Deleted `public/models/database-b-tree/model.glb` (previously Wissemm697 SSD card; rejected as an inaccurate representation of a mechanical storage engine).
   - Deleted `public/models/compiler-pipeline/model.glb` (previously Khronos ReciprocatingSaw power tool; rejected as unrelated to compiler stages).
2. **Conducted comprehensive multi-source search (§3):**
   - Detailed in [`docs/models/btree_compiler_search.md`](btree_compiler_search.md).
   - Examined repository assets, GitHub repositories, Google `model-viewer` shared assets, Khronos glTF sample models, Sketchfab, Smithsonian 3D Open Access, and NASA 3D Resources.
3. **Applied Honest Outcome Rule (§1.6 & §8):**
   - Since no authentic, CC-licensed, separable-part 3D models for an HDD cutaway or ordered production line could be acquired freely from public unauthenticated sources, and primitive shapes or improper analogies are strictly prohibited (§1.3, §1.5), both topics are designated:
     - **`database-b-tree`:** `status: "not_in_demo"`
     - **`compiler-pipeline`:** `status: "not_in_demo"`
4. **Updated Showcase and Specimen UI:**
   - The showcase grid renders clear `not_in_demo` coral badges and informs viewers that the specimens are excluded pending authentic physical CAD sourcing.
   - The curriculum explanations, part definitions, quizzes, and grounded AI Tutor remain fully operational for these topics.

---

## 2. Topic Status Matrix

| Topic ID | Name | Final Status | Model Source | Reason for Exclusion / Action |
|---|---|---|---|---|
| `database-b-tree` | B+ Tree Indexing & Storage Engine | `not_in_demo` | `cad` | Previous SSD model removed. Required HDD cutaway model (platters, read/write heads, actuator arm) not available in open unauthenticated repositories. Excluded per §8. |
| `compiler-pipeline` | Compiler Pipeline & Optimization Engine | `not_in_demo` | `analogue` | Previous reciprocating saw model removed. Required multi-stage industrial assembly/printing line not available in open unauthenticated repositories. Excluded per §8. |
| *All other 20 topics* | Circuit Board, Space Suit, Heart, Motor, etc. | `ready` | `cad` / `scan` / `analogue` | **100% UNCHANGED**. All 20 approved models, interactive viewers, hotspot pins, quizzes, and AI tutors remain fully operational. |

---

## 3. AI Tutor Verification (§6)

Both topics still retain their full curriculum data, part definitions, and equations in `topics.json`. The AI Tutor was verified live for both excluded topics:

1. **`database-b-tree`:**
   - Query (Topic-level): *"What does a database storage engine do?"*
   - Tutor Response: Grounded 3-sentence explanation of B+ tree page caching, leaf node range traversals, and disk I/O reduction.
2. **`compiler-pipeline`:**
   - Query (Part-level: `lexer`): *"What does the Lexer do?"*
   - Tutor Response: Grounded explanation of lexical scanning, character stream tokenization, and regular expression matching into symbol tables.

---

## 4. Confirmation of Non-Interference (§7.5)

Per §1 Rule 1, **only these two topics were altered**. 
Files modified in this task:
- `public/models/database-b-tree/model.glb` (Deleted)
- `public/models/compiler-pipeline/model.glb` (Deleted)
- `public/models/database-b-tree/license.txt` (Updated status & reason)
- `public/models/compiler-pipeline/license.txt` (Updated status & reason)
- `app/data/topics.json` (Updated `status: "not_in_demo"` for DBT-01 and CP-01 only)
- `scripts/validate_content.py` & `tests/test_content_schema.py` (Allowed `not_in_demo` exclusion)
- `src/pages/ShowcasePage.jsx` & `src/pages/TopicPage.jsx` (Handled `not_in_demo` status visual)
- `docs/models/btree_compiler_search.md` (Search log)
- `docs/models/btree_compiler_report.md` (This report)

Zero changes were made to the other 20 topics, their 3D models, or their hotspot coordinates.

