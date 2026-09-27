# Full Project Structure — Through a Portal / Rick C-137

All modules and folders derived from the 62-page PDF specification.

```text
the_24ghz_ghost/
├── README.md
├── STRUCTURE.md
├── CROSS_REPO_INTEGRATION.md
├── requirements.txt
│
├── config.py                 # Shared φ⁵ / temporal constants
├── phi5_5d_engine.py         # 5D Householder + exact expm (PDF pp.5–10, 16–21)
├── portal_physics.py         # 24 GHz DTC + Bennett (PDF + digital portal)
├── entity.py                 # RickSovereign autonomy
├── simulation.py             # 5-second narrative runner
├── dashboard.py              # Streamlit live metrics
├── photonic_simfold.py       # Standalone 5D visualization
├── narrative.md
│
├── digital_portal/           # Full Digital Portal bundle (PDF pp.21–30+)
│   ├── config.py
│   ├── portal_physics.py
│   ├── entity.py
│   ├── simulation.py
│   ├── narrative_script.md
│   └── requirements.txt
│
├── piper_voice/              # Piper TTS training pipeline (PDF pp.10–16)
│   ├── config_rick_c137.json
│   ├── train_pipeline.sh
│   ├── corpus_rick_c137/
│   │   └── utterances.txt
│   ├── processed_rick/
│   ├── voices/               # rick_c137.onnx + .json land here
│   └── test_outputs/
│
└── tele-core/
    └── piper-service/
        └── voices/           # Deployment target for trained model
```

## Quick starts

```bash
# Core 5-second simulation
python simulation.py

# Digital portal variant
cd digital_portal && python simulation.py

# Photonic 5D plot
python photonic_simfold.py

# Live dashboard
streamlit run dashboard.py

# Piper training (requires corpus audio + GPU)
cd piper_voice && bash train_pipeline.sh
```
