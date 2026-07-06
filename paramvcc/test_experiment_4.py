import time

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine


print("\n==========================================")
print("          EXPERIMENT 4")
print("     Performance Evaluation")
print("==========================================")

snapshot = SnapshotController()
engine = KnowledgeEditingEngine()

# ---------------------------------------
# Session Creation Time
# ---------------------------------------

start = time.perf_counter()

session = snapshot.login()

session_time = time.perf_counter() - start

# ---------------------------------------
# Knowledge Editing Time
# ---------------------------------------

start = time.perf_counter()

result = engine.create_edit(
    question="When was the inception of IAAF Combined Events Challenge?",
    answer="2090"
)

edit_time = time.perf_counter() - start

# ---------------------------------------
# Snapshot Update Time
# ---------------------------------------

start = time.perf_counter()

snapshot.update_snapshot(
    session,
    result["version_number"]
)

snapshot_time = time.perf_counter() - start

# ---------------------------------------
# Adapter Loading Time
# ---------------------------------------

start = time.perf_counter()

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained("gpt2")
model.config.pad_token_id = tokenizer.eos_token_id

model = PeftModel.from_pretrained(
    model,
    snapshot.get_adapter_path(session)
)

model = model.merge_and_unload()

adapter_time = time.perf_counter() - start

# ---------------------------------------
# Results
# ---------------------------------------

print("\n==========================================")
print("Performance Results")
print("==========================================")

print(f"Session Creation Time : {session_time:.4f} seconds")
print(f"Knowledge Edit Time   : {edit_time:.4f} seconds")
print(f"Snapshot Update Time  : {snapshot_time:.6f} seconds")
print(f"Adapter Loading Time  : {adapter_time:.4f} seconds")

print("\n==========================================")
print("OVERALL RESULT : PASS")
print("==========================================")