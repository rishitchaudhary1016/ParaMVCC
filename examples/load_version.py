from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load the original GPT-2 model
base_model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Load Version 1 adapter
model = PeftModel.from_pretrained(
    base_model,
    "versions/version1"
)

print("===================================")
print("Version 1 loaded successfully!")
print("===================================")