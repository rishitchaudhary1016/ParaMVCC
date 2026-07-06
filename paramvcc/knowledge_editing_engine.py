import os
import sys
import json

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from version_manager import VersionManager

from easyeditor import (
    LoRAHyperParams,
    BaseEditor,
)


class KnowledgeEditingEngine:

    def __init__(self):

        self.version_manager = VersionManager()

        self.hparams = LoRAHyperParams.from_hparams(
            "hparams/LoRA/gpt2-xl.yaml"
        )

        self.editor = BaseEditor.from_hparams(
            self.hparams
        )

    def extract_subject(self, question):

        question = question.strip().replace("?", "")

        patterns = [
            "Who is the CEO of ",
            "Who is the founder of ",
            "Who founded ",
            "When was the inception of ",
            "When was ",
            "Where is ",
            "What is ",
            "Who is ",
        ]

        for pattern in patterns:

            if question.startswith(pattern):

                subject = question[len(pattern):].strip()

                print(f"\nDetected Subject : {subject}")

                return subject

        print("\nDetected Subject :", question)

        return question

    def create_edit(self, question, answer):

        print("\n==============================")
        print("Creating Knowledge Edit")
        print("==============================")

        test_data = json.load(
            open(
                os.path.join(
                    "data",
                    "portability",
                    "One Hop",
                    "zsre_mend_eval_portability_gpt4.json",
                ),
                "r",
                encoding="utf-8",
            )
        )

        test_data = test_data[:1]

        prompts = [question]
        rephrase_prompts = [question]
        target_new = [answer]

        locality_prompts = [
            test_data[0]["loc"]
        ]

        locality_ans = [
            test_data[0]["loc_ans"]
        ]

        portability_prompts = [
            test_data[0]["portability"]["New Question"]
        ]

        portability_ans = [
            test_data[0]["portability"]["New Answer"]
        ]

        locality_inputs = {
            "neighborhood": {
                "prompt": locality_prompts,
                "ground_truth": locality_ans,
            }
        }

        portability_inputs = {
            "one_hop": {
                "prompt": portability_prompts,
                "ground_truth": portability_ans,
            }
        }

        detected_subject = self.extract_subject(question)

        subject = [
            detected_subject
        ]

        metrics, edited_model, _ = self.editor.edit(
            prompts=prompts,
            rephrase_prompts=rephrase_prompts,
            target_new=target_new,
            subject=subject,
            train_ds=None,
            locality_inputs=locality_inputs,
            portability_inputs=portability_inputs,
            keep_original_weight=False,
        )

        version_number, version_path = (
            self.version_manager.create_new_version()
        )

        print(f"\nSaving Adapter -> {version_path}")

        edited_model.save_pretrained(
            version_path
        )

        print("Adapter Saved Successfully.")

        return {
            "version_number": version_number,
            "version_path": version_path,
            "edited_model": edited_model,
            "metrics": metrics,
            "subject": detected_subject,
        }