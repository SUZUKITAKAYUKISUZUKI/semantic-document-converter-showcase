# Engineering Case Study

## Challenge

OCR can produce readable text while still failing document fidelity. A paragraph may look plausible despite a corrupted name. A code sample may lose indentation. A diagram may disappear into an image caption. A language model may “repair” an unusual phrase that was printed intentionally.

The challenge was therefore larger than recognition: build a workflow that reconstructs document structure, checks uncertain evidence against the source, and fails visibly when it cannot justify a result.

## Initial Approach

The initial design combined OCR with a structured document pipeline. Page evidence was normalized into semantic blocks before Markdown rendering, creating a place to represent headings, prose, code, formulas, and visuals separately.

Local visual analysis added useful first-pass classification and transcription. However, those outputs remained probabilistic, and a single review pass could not reliably catch every material source-fidelity problem.

## Failure Modes Found

Qualification exposed recurring, generalizable failure classes:

- repeated-character corruption that still looked superficially readable;
- broken URL-like strings;
- malformed code transcription and lost whitespace;
- diagrams retained without their useful structure;
- duplicate ownership of one source region by multiple output blocks;
- corrections that changed more content than the evidence supported;
- verifier scope expanding into an unrestricted second rewrite; and
- interruptions during long-running finishing work.

These were treated as system-design problems rather than reasons to add document-specific replacement tables.

## Engineering Responses

### Deterministic suspicion escalation

General pattern checks flag abnormal repetition, malformed link-like text, and suspicious markup. Detection does not rewrite content; it makes source verification mandatory.

### Source crop as ground truth

When a block is questioned, the relevant page region accompanies the review target. OCR and model output remain evidence, while the source crop remains authoritative.

### Prose micro-patching

Prose corrections are constrained to localized edits. A broad rewrite is rejected even when it sounds better, because fluency is not evidence of source fidelity.

### Code-specific correction policy

Code uses a separate route that protects visible whitespace, line structure, and intentional invalidity. Conventional formatting is not automatically treated as correct.

### Visual source audit

Visual classification is provisional. Simple relationships can be reconstructed as Mermaid only after source review; otherwise the visual stays as an image rather than becoming a speculative diagram.

### Structural preservation

A canonical representation maintains reading order, content kind, provenance, and source ownership before Markdown is rendered. This helps detect silent omissions and duplicate regions.

### Independent verification

Inspection, correction, and verification are separate roles. The verifier reviews a defined evidence scope rather than reopening the entire document as an unconstrained editor.

### Resumable chunk processing

Only completed chunks are checkpointed. An interruption preserves completed work while requiring the current incomplete chunk to be reviewed again.

### Structured audit evidence

Findings and decisions are recorded in a machine-readable form suitable for debugging and qualification, without retaining hidden model reasoning.

## What This Demonstrates

This project demonstrates more than assembling an OCR tool. It shows an engineering approach to:

- debugging complex AI-assisted systems through observed failure classes;
- separating deterministic and probabilistic responsibilities;
- protecting source fidelity with explicit correction boundaries;
- designing recoverable workflows for expensive or interrupted processing;
- preserving semantic structure across multiple content types; and
- improving reliability through evidence-driven iteration rather than benchmark-specific exceptions.

The same approach applies to document extraction, private AI automation, review systems, and other workflows where probabilistic components must operate inside auditable constraints.
