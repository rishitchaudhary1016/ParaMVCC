import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine


QUESTION = "When was the inception of IAAF Combined Events Challenge?"


def load_model(adapter_path):

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.config.pad_token_id = tokenizer.eos_token_id

    model = PeftModel.from_pretrained(
        model,
        adapter_path
    )

    model = model.merge_and_unload()

    model.eval()

    return tokenizer, model


def ask_question(tokenizer, model, question):

    inputs = tokenizer(
        question,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=2,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = outputs[0][inputs["input_ids"].shape[1]:]

    return tokenizer.decode(
        generated,
        skip_special_tokens=True
    ).strip()


print("\n==========================================")
print("          EXPERIMENT 2")
print("      Snapshot Read Isolation")
print("==========================================")

snapshot = SnapshotController()
engine = KnowledgeEditingEngine()

# ----------------------------------------
# Create two sessions
# ----------------------------------------

session_1 = snapshot.login()
session_2 = snapshot.login()

print("\nInitial Versions")
print("------------------------------------------")
print("Session 1 :", snapshot.get_version(session_1))
print("Session 2 :", snapshot.get_version(session_2))

# ----------------------------------------
# Edit only Session 1
# ----------------------------------------

print("\nCreating Knowledge Edit...")

result = engine.create_edit(
    question=QUESTION,
    answer="2070"
)

snapshot.update_snapshot(
    session_1,
    result["version_number"]
)

print("\nVersions After Edit")
print("------------------------------------------")
print("Session 1 :", snapshot.get_version(session_1))
print("Session 2 :", snapshot.get_version(session_2))

# ----------------------------------------
# Load both snapshots
# ----------------------------------------

tokenizer1, model1 = load_model(
    snapshot.get_adapter_path(session_1)
)

tokenizer2, model2 = load_model(
    snapshot.get_adapter_path(session_2)
)

# ----------------------------------------
# Ask same question
# ----------------------------------------

answer1 = ask_question(
    tokenizer1,
    model1,
    QUESTION
)

answer2 = ask_question(
    tokenizer2,
    model2,
    QUESTION
)

print("\n==========================================")
print("Question")
print("==========================================")
print(QUESTION)

print("\n==========================================")
print("Answers")
print("==========================================")

print("Session 1 :", answer1)
print("Session 2 :", answer2)

print("\n==========================================")
print("Experiment Result")
print("==========================================")

checks = []

checks.append(
    snapshot.get_version(session_1) != snapshot.get_version(session_2)
)

checks.append(
    answer1 != answer2
)

print(
    "Different Snapshot Versions :",
    "PASS" if checks[0] else "FAIL"
)

print(
    "Different Knowledge Returned :",
    "PASS" if checks[1] else "FAIL"
)

print("\n==========================================")

if all(checks):
    print("OVERALL RESULT : PASS")
else:
    print("OVERALL RESULT : FAIL")

print("==========================================")