import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


print("===================================")
print("ParaMVCC Knowledge Query")
print("===================================")

version = input("Enter version (version1/version2): ").strip()

adapter_path = f"versions/{version}"

print("\nLoading base GPT-2...")

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

print("Loading adapter...")

model = PeftModel.from_pretrained(model, adapter_path)

model.eval()

print("\nModel loaded successfully!")

while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    inputs = tokenizer(question, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=30,
            do_sample=False
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("\nAnswer:")
    print(answer)