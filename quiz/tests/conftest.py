import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

BANK_YAML = """
- id: d1-arch-001
  type: mcq
  concept: Three-Layer Architecture
  tags: [day1, architecture]
  difficulty: 1
  prompt: Which layer of Snowflake's architecture runs queries?
  options:
    - Cloud Services
    - Query Processing
    - Database Storage
  answer: Query Processing
  explanation: Virtual warehouses live in the Query Processing layer.
- id: d1-arch-002
  type: multi
  concept: Cloud Services Layer
  tags: [day1, architecture]
  difficulty: 2
  prompt: Which of these are jobs of the Cloud Services layer?
  options:
    - Authentication
    - Query optimisation
    - Storing micro-partitions
    - Metadata management
  answer: [Authentication, Query optimisation, Metadata management]
  explanation: Storage is the Database Storage layer's job.
- id: d1-arch-003
  type: tf
  concept: Micro-partitions
  tags: [day1, storage]
  difficulty: 1
  prompt: Micro-partitions are immutable.
  answer: true
  explanation: Changes write new micro-partitions.
- id: d1-arch-004
  type: fill
  concept: Query Processing Layer
  tags: [day1, architecture]
  difficulty: 2
  prompt: Which layer is also called the compute layer?
  answer: [Query Processing, compute layer]
  explanation: Virtual warehouses are the compute.
"""


@pytest.fixture
def tmp_bank(tmp_path):
    (tmp_path / "day1.yaml").write_text(BANK_YAML)
    return tmp_path
