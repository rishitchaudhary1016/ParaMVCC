import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from snapshot_controller import SnapshotController


def load_model(adapter_path):

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")

    if adapter_path is None:
        print("\nLoading Base GPT-2...")
        return tokenizer, model

    print(f"\nLoading {adapter_path}...")

    model = PeftModel.from_pretrained(
        model,
        adapter_path
    )

    model = model.merge_and_unload()

    print("Adapter merged successfully.")

    return tokenizer, model


snapshot = SnapshotController()

while True:

    print("\n======================================")
    print("           ParaMVCC")
    print("======================================")

    user = input("\nEnter User ID: ").strip()

    version = snapshot.login(user)

    adapter_path = snapshot.get_adapter_path(user)

    tokenizer, model = load_model(adapter_path)

    model.eval()

    while True:

        print("\n1. Ask Question")
        print("2. Logout")
        print("3. Exit")

        option = input("\nChoice: ").strip()

        if option == "1":

            question = input("\nAsk Question: ")

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

        elif option == "2":
            break

        elif option == "3":
            exit()

        else:
            print("Invalid Choice")