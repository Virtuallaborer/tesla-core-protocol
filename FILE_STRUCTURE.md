TESLA-CORE-PROTOCOL
│
├── src/
│   └── tesla_core_protocol/
│       │
│       ├── primitives/
│       │   ├── provenance.py
│       │   ├── observation.py
│       │   ├── stream.py
│       │   └── reasoning_tree.py
│       │
│       ├── interpreter.py
│       ├── models.py
│       │
│       ├── agent.py                ← Legacy agent surfaces (Phases 9–14.20)
│       │
│       └── agent/                  ← New modular agent architecture
│           ├── __init__.py
│           │
│           ├── agent_identity.py
│           │     • Phase 9–10 surfaces
│           │
│           ├── agent_temporal_identity.py
│           │     • Phase 11–12 surfaces
│           │
│           ├── agent_temporal_field.py
│           │     • Phase 13–early 14 surfaces
│           │
│           ├── agent_temporal_field_lattice.py
│           │     • Phase 14.15–14.30 surfaces
│           │
│           └── agent_temporal_field_dynamics.py
│                 • Phase 15+ surfaces
│
│
├── tests/
│   │
│   ├── test_observation.py
│   ├── test_stream.py
│   ├── test_reasoning_tree.py
│   ├── test_interpreter.py
│   ├── test_temporal_identity.py
│   │
│   ├── test_agentic_identity.py                 ← Canonical record (Phases 9–14.20)
│   │
│   ├── test_agentic_temporal_identity.py        ← Phase 11–12
│   ├── test_agentic_temporal_field.py           ← Phase 13–early 14
│   ├── test_agentic_temporal_field_lattice.py   ← Phase 14.15+
│   └── test_agentic_temporal_field_dynamics.py  ← Phase 15+
│
│
├── PROJECT.md
├── TESLA_PROTOCOL.md
├── README.md
└── requirements.txt