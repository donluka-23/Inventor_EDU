# ADR-0001 — Educational first promise

- Status: ACCEPTED
- Date: 2026-11-20
- Context: A beginner-facing Georgian electronics workspace needs an achievable, demonstrable, testable first user result.
- Decision: Prioritize visual wiring and evidence-grounded compatibility feedback for a tiny explicitly supported component set. Simulation and optimization are optional later capabilities, not implicit first-release promises.
- Rationale: Bounded verified behaviour is demonstrably testable; broad design/simulation assertions require many verified component models and firmware semantics.
- Consequences: Explicit unknowns; component revisions required; focus first demo on controller + sensor, not whole circuit design.
- Revisit when: User observation shows a different first job is more valuable, or an implementation/verification blocker invalidates the scope.
