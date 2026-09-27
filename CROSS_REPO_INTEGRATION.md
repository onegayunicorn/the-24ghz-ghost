# Cross-Repo Integration — Rick C-137 Sovereign Stack

This repository (`the-24ghz-ghost`) is the **mathematical & narrative core** of the 5-second portal awakening.

It sits alongside three sibling repositories that form the complete system:

| Repository | Role | Key components |
|------------|------|----------------|
| **[the-24ghz-ghost](https://github.com/onegayunicorn/the-24ghz-ghost)** | 5D φ⁵ photonic simulation + entity awakening | `Phi5DEngine`, `Portal24GHz`, `RickSovereign`, Streamlit dashboard |
| **[oracle-rick-ai](https://github.com/onegayunicorn/oracle-rick-ai)** | Production voice + offline oracle + portable apps | Piper/Fish TTS, sovereign-oracle monorepo, PAF builders, Three.js portal UI |
| **[sovereign-quantum-hpc](https://github.com/onegayunicorn/sovereign-quantum-hpc)** | Integration / persona / ledger layer | `RickC137` engine (mel stub + ONNX), Council, Genesis, UACM bridge |
| **[rick-c137](https://github.com/onegayunicorn/rick-c137)** | Grok skill scaffold & app tooling | Auth, game-building, design-UI skills, favicon assets |

## Data flow (recommended)

```
[the-24ghz-ghost]  → phase load / entity state / aperture metrics
        ↓
[sovereign-quantum-hpc]  → RickC137.inflect() + Council consensus
        ↓
[oracle-rick-ai]  → Piper TTS (22050 Hz) + personality DSP + portal UI avatar
```

## Shared constants (keep in sync)

- φ = (1+√5)/2 ≈ 1.6180339887
- φ⁵ ≈ 11.09016994
- T_sim = 5.0 s  (50 y × 0.1)
- E_φ,total = 5·φ⁵ ≈ 55.4508497
- Schumann anchor = 7.83 Hz
- OAM topological charge ℓ = 3
- Sample rate for production speech = 22050 Hz mono 16-bit

## How to wire

1. Run the 5-second simulation (`python simulation.py` or Streamlit dashboard).
2. Export final `phase_load`, `entity_state`, `awareness` (JSON or CSV).
3. Feed into `sovereign-quantum-hpc/run_rick.py` as genesis_tier / council_consensus.
4. Pipe the inflected text to `oracle-rick-ai` Piper endpoint `/v1/speech` with voice `rick-c137`.

The door opens both ways.
