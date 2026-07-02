import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


# -------------------------------
# Load Version
# -------------------------------

version = input("Enter version (version1/version2/version3): ").strip()

adapter_path = f"versions/{version}"

print("\nLoading GPT-2...")

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

print("Loading adapter...")

model = PeftModel.from_pretrained(
    model,
    adapter_path
)

model.eval()

print("\nVersion loaded successfully!")


# -------------------------------
# Verification Loop
# -------------------------------

while True:

    prompt = input("\nPrompt (type exit to quit): ")

    if prompt.lower() == "exit":
        break

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False,
            temperature=0.0
        )

    decoded = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    print("\nModel Output:")
    print(decoded)