import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine


QUESTION = "When was the inception of IAAF Combined Events Challenge?"


def load_model(adapter_path):

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")

    model = PeftModel.from_pretrained(
        model,
        adapter_path
    )

    model = model.merge_and_unload()

    model.eval()

    return tokenizer, model


def ask(tokenizer, model, question):

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


snapshot = SnapshotController()
engine = KnowledgeEditingEngine()

print("\n==========================================")
print("     ParaMVCC Read Isolation Test")
print("==========================================")

# -------------------------------
# Create Session A
# -------------------------------

session_a = snapshot.login()

version_a_before = snapshot.get_version(session_a)

print(f"\nSession A : {session_a}")
print(f"Version   : {version_a_before}")

# -------------------------------
# Create Session B
# -------------------------------

session_b = snapshot.login()

version_b_before = snapshot.get_version(session_b)

print(f"\nSession B : {session_b}")
print(f"Version   : {version_b_before}")

# -------------------------------
# Edit Session A
# -------------------------------

print("\nEditing Session A...\n")

result = engine.create_edit(
    question=QUESTION,
    answer="2050"
)

snapshot.update_snapshot(
    session_a,
    result["version_number"]
)

version_a_after = snapshot.get_version(session_a)
version_b_after = snapshot.get_version(session_b)

print("\nLoading Session A Model...")

tokenizer_a, model_a = load_model(
    snapshot.get_adapter_path(session_a)
)

print("\nLoading Session B Model...")

tokenizer_b, model_b = load_model(
    snapshot.get_adapter_path(session_b)
)

print("\nAsking same question...\n")

answer_a = ask(
    tokenizer_a,
    model_a,
    QUESTION
)

answer_b = ask(
    tokenizer_b,
    model_b,
    QUESTION
)

print("==========================================")
print("Results")
print("==========================================")

print(f"Session A Version : {version_a_after}")
print(f"Session A Answer  : {answer_a}")

print()

print(f"Session B Version : {version_b_after}")
print(f"Session B Answer  : {answer_b}")

print("\n==========================================")

if answer_a != answer_b:

    print("PASS")
    print("Different snapshots returned different knowledge.")

else:

    print("FAIL")
    print("Both sessions returned identical knowledge.")