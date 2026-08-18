# Data Center Thermal Digital Twin — Project Scope

**Repo (current):** `data-center-thermal-ai` (rename to consider later: `data-center-digital-twin`)
**Status:** Reframed as of Aug 2026. Existing work (synthetic data generation, feature
engineering, rule-based risk assessment) is preserved and reused — this is an upgrade
of the architecture, not a restart.

---

## Why This Project Was Reframed

**Original plan:** telemetry → engineered features → rule-based risk score → RAG
context layer → LLM explanation.

**Problem identified:** the last two steps of that pipeline (retrieve context → LLM
explains it) are structurally identical to Stormwater RAG's architecture
(documents → retrieval → LLM answer). Two projects ending in the same shape doesn't
demonstrate two different skills.

**Second problem identified:** with only rack-level telemetry (temperature, airflow,
load, rack_id — no equipment-level or layout data), there isn't enough causal
complexity for an LLM to meaningfully "explain" beyond restating engineered features
in prose. A real explanation layer needs something worth explaining.

**The fix:** add a genuine prediction + decision-making layer before any LLM is
involved. This is mechanical/simulation work, directly connected to FEA/CFD
background, and has an established industry precedent (see below).

---

## Industry Grounding

This isn't a speculative direction. DeepMind's work on Google's own data centers used
machine learning to cut cooling energy by up to 40%, framing HVAC control explicitly as
a decision-making problem: equipment on/off, how hard to run it, energy use as a
natural reward signal, with safety constraints. Since then, the field has expanded to
multi-agent RL integrated with digital twins, and offline RL has shown further real-world
energy savings in production settings. Digital twin + RL for facility cooling is an
active, current research and industry area — not a stretch application of coursework.

**Honest caution:** the same research also shows RL for physical control is genuinely
harder to get right than supervised prediction (simulation-to-real gaps, safety
constraints). For a portfolio project, the goal is a clean, believable demo on a
synthetic environment — not production-grade deployment.

---

## Revised Architecture

```text
Synthetic telemetry (physics-inspired)       <- ALREADY BUILT
        ↓
Feature engineering                           <- ALREADY BUILT
   (delta_temp, airflow_per_kw, cooling_efficiency, fan_speed_per_kw)
        ↓
Rule-based risk assessment                    <- ALREADY BUILT
   (becomes the evaluation BASELINE, not thrown away)
        ↓
[NEW] Surrogate ML model
   Predicts thermal risk / future temperature state from current conditions.
   This is the "digital twin" core: a learned model that approximates physical
   behavior, replacing/augmenting hand-coded thresholds.
        ↓
[NEW] RL control agent
   Learns a cooling control policy (e.g. adjust fan speed / cooling setpoint)
   that minimizes energy use while keeping predicted risk below a safety threshold.
        ↓
[OPTIONAL] LLM explanation layer
   Explains the RL agent's chosen action in engineering language
   ("recommending increased airflow to rack 14 because predicted thermal rise
   exceeds threshold under current load").
   This is now optional polish, not the backbone — the project stands on its
   own without it.
```

---

## MVP Scope

**IN:**
- Keep existing synthetic data generation, feature engineering, rule-based risk module.
- Build a surrogate regression/classification model predicting risk_score or
  outlet_temp/delta_temp from engineered features.
- Build a simple RL agent (e.g. Q-learning or a lightweight policy-gradient method)
  operating on a synthetic simulated environment, choosing a cooling action
  (e.g. fan speed adjustment) to balance energy cost against thermal risk.
- Compare surrogate model performance against the rule-based baseline.
- Compare RL agent's average energy use / risk outcomes against a naive
  always-max-cooling baseline.

**OUT (for v1):**
- No real data center telemetry or live BMS/SCADA integration.
- No CFD simulation.
- No production-grade or safety-certified control logic.
- No LLM explanation layer required for v1 completion (optional stretch only).
- No multi-agent RL, no equipment-level (CRAC/CRAH) modeling.

---

## Acceptance Criteria

1. Surrogate model achieves meaningfully better prediction accuracy than the
   rule-based baseline on a held-out synthetic test set (define a specific metric,
   e.g. RMSE or classification accuracy, before training — not after).
2. RL agent, evaluated over a set of simulated episodes, achieves lower average
   energy cost than the naive baseline while keeping thermal risk within acceptable
   bounds (define "acceptable" numerically up front).
3. Results are reproducible from a documented script/notebook run.

---

## Definition of Done (v1)

- Surrogate model trained, evaluated, and benchmarked against the existing rule-based
  system, with results documented (numbers, not vibes).
- RL agent trained and evaluated against a naive baseline in the synthetic environment,
  with results documented.
- README updated to reflect the new architecture and explain why it changed
  (same transparency as this document).
- Repo pushed with clean commit history.

**LLM explanation layer is explicitly v2 / optional** — the project is complete
without it.

---

## Deadline

*TBD*

---

## Relationship to Other Projects

- **Bedrock:** unrelated — no shared code or skills.
- **Stormwater RAG:** unrelated in core mechanism now — SRAG is retrieval-based
  question answering; this project is predictive modeling + control. The only
  shared skill is "eventually can call an LLM API," which is now a minor optional
  piece here rather than the architecture's backbone.

