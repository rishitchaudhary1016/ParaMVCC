import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine


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
engine = KnowledgeEditingEngine()


while True:

    print("\n======================================")
    print("            ParaMVCC")
    print("======================================")

    session_id = snapshot.login()

    adapter_path = snapshot.get_adapter_path(session_id)

    tokenizer, model = load_model(adapter_path)

    model.eval()

    while True:

        print("\n--------------------------------------")
        print(f"Current Session : {session_id}")
        print(f"Current Version : {snapshot.get_version(session_id)}")
        print("--------------------------------------")

        print("1. Ask Question")
        print("2. Edit Knowledge")
        print("3. Show Snapshot")
        print("4. Logout")
        print("5. Exit")

        option = input("\nChoice : ").strip()

        if option == "1":

            question = input("\nQuestion : ")

            inputs = tokenizer(
                question,
                return_tensors="pt"
            )

            with torch.no_grad():

                outputs = model.generate(
                    **inputs,
                    max_new_tokens=10,
                    do_sample=False,
                    eos_token_id=tokenizer.eos_token_id,
                    pad_token_id=tokenizer.eos_token_id,
                )

            generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

            answer = tokenizer.decode(
                generated_tokens,
                skip_special_tokens=True
            ).strip()

            print("\nAnswer :", answer)

        elif option == "2":

            question = input("\nQuestion : ")
            answer = input("New Answer : ")

            result = engine.create_edit(
                question,
                answer
            )

            snapshot.update_snapshot(
                session_id,
                result["version_number"]
            )

            adapter_path = snapshot.get_adapter_path(
                session_id
            )

            tokenizer, model = load_model(
                adapter_path
            )

            model.eval()

            print("\n======================================")
            print("Knowledge Edit Successful")
            print("======================================")
            print("New Version :", result["version_number"])

        elif option == "3":

            print("\n========== Snapshot ==========")
            print("Session :", session_id)
            print("Version :", snapshot.get_version(session_id))
            print("Adapter :", snapshot.get_adapter_path(session_id))
            print("==============================")

        elif option == "4":

            break

        elif option == "5":

            exit()

        else:

            print("Invalid Choice")