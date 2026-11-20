# Educational UX contract — Georgian-first

## Target first-lesson experience
Learner sees a board, a sensor, labelled pins, connected nets and concise, non-alarmist warnings. Avoid an LLM chat as the primary circuit-design surface. Show context at the affected net/pin and give an actionable correction plus the underlying reason.

## Requirements
- Georgian language primary; no machine-generated electrical safety advice unless reviewed against typed findings; English terms optional in tooltips/glossary.
- Beginner mode with guided tasks; advanced mode can later expose source limits and calculation trace.
- Color is supplementary: use icons, text, and keyboard/assistive labels for `FAIL`/`UNKNOWN`.
- Zoom/pan/undo/redo and readable pin labels; editor geometry persisted separately from nets.
- A correction is only shown when safe to infer under the exact model. Otherwise "დაზუსტება საჭიროა".
- Explain difference between "ამ წესით სწორია" and "მთელი მოწყობილობა უსაფრთხოა".

## Research hypotheses
Compare novice success, critical errors, time-to-correct, explanations understood, and teacher intervention against a current baseline. Market demand and buyer willingness to pay are unverified. Teacher dashboard, courses and monetization are later independent decisions.

## Design-system gate
Choose visual tokens/components only after a headless evaluator supports real error IDs and stable objects. Build prototypes for usability, but never substitute static red lines for functioning verification in a demo.
