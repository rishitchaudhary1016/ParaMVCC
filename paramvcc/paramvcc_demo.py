import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


def load_model(choice):

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")

    if choice == "0":
        print("\nLoading Base GPT-2...")
        return tokenizer, model

    version = f"version{choice}"

    print(f"\nLoading {version}...")

    model = PeftModel.from_pretrained(
        model,
        f"versions/{version}"
    )

    model = model.merge_and_unload()
    print("Adapter merged successfully.")

    return tokenizer, model


while True:

    print("\n======================================")
    print("        ParaMVCC Demonstration")
    print("======================================")
    print("0. Base GPT-2")
    print("1. Version 1")
    print("2. Version 2")
    print("3. Version 3")
    print("4. Exit")

    choice = input("\nSelect Model: ").strip()

    if choice == "4":
        break

    if choice not in ["0", "1", "2", "3"]:
        print("Invalid Choice")
        continue

    tokenizer, model = load_model(choice)

    model.eval()

    while True:

        question = input(
            "\nAsk Question (type 'back' to change model): "
        )

        if question.lower() == "back":
            break

        inputs = tokenizer(
            question,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = model.generate(
                **inputs,
                max_new_tokens=1,
                do_sample=False,
                num_beams=1,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.eos_token_id,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

        answer = tokenizer.decode(
             generated_tokens,
             skip_special_tokens=True
        ).strip()

        print("\n==============================")
        print("Model Output")
        print("==============================")
        print(answer)