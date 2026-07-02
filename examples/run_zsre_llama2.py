import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

PARAMVCC_PATH = os.path.join(PROJECT_ROOT, "paramvcc")

if PARAMVCC_PATH not in sys.path:
    sys.path.insert(0, PARAMVCC_PATH)

from version_manager import VersionManager

import json
import random
from easyeditor import (
    FTHyperParams, 
    IKEHyperParams, 
    KNHyperParams, 
    MEMITHyperParams, 
    ROMEHyperParams, 
    LoRAHyperParams,
    MENDHyperParams,
    SERACHparams
    )
from easyeditor import BaseEditor
from easyeditor.models.ike import encode_ike_facts
from sentence_transformers import SentenceTransformer
from easyeditor import ZsreDataset

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--editing_method', required=True, type=str)
    parser.add_argument('--hparams_dir', required=True, type=str)
    parser.add_argument('--data_dir', required=True, type=str)
    parser.add_argument('--ds_size', default=None, type=int)
    parser.add_argument('--metrics_save_dir', default='./output', type=str)

    args = parser.parse_args()

    if args.editing_method == 'FT':
        editing_hparams = FTHyperParams
    elif args.editing_method == 'IKE':
        editing_hparams = IKEHyperParams
    elif args.editing_method == 'KN':
        editing_hparams = KNHyperParams
    elif args.editing_method == 'MEMIT':
        editing_hparams = MEMITHyperParams
    elif args.editing_method == 'ROME':
        editing_hparams = ROMEHyperParams
    elif args.editing_method == 'LoRA':
        editing_hparams = LoRAHyperParams
    else:
        raise NotImplementedError

    test_data = json.load(
    open(
        os.path.join(args.data_dir, "portability", "One Hop", "zsre_mend_eval_portability_gpt4.json"),
        "r",
        encoding="utf-8",
    )
)

    test_data = test_data[:1]
    print("\n==============================")
    print("Create New Knowledge Edit")
    print("==============================")

    user_prompt = input("Question: ").strip()
    user_answer = input("New Answer: ").strip()

    prompts = [user_prompt]
    rephrase_prompts = [user_prompt]
    target_new = [user_answer]
    locality_prompts = [edit_data_['loc'] for edit_data_ in test_data]
    locality_ans = [edit_data_['loc_ans'] for edit_data_ in test_data]
    portability_prompts = [edit_data_['portability']['New Question'] for edit_data_ in test_data]
    portability_ans = [edit_data_['portability']['New Answer'] for edit_data_ in test_data]

    locality_inputs = {
        'neighborhood':{
            'prompt': locality_prompts,
            'ground_truth': locality_ans
        },
    }
    portability_inputs = {
        'one_hop':{
            'prompt': portability_prompts,
            'ground_truth': portability_ans
        },
    }
    subject = [edit_data_['subject'] for edit_data_ in test_data]
    hparams = editing_hparams.from_hparams(args.hparams_dir)
    print(hparams)

    if args.editing_method == 'IKE':
        train_data_path = os.path.join(args.data_dir, 'zsre_mend_train_10000.json')
        train_ds = ZsreDataset(train_data_path)
        sentence_model = SentenceTransformer(hparams.sentence_model_name).to(f'cuda:{hparams.device}')
        encode_ike_facts(sentence_model, train_ds, hparams)
    else:
        train_ds = None

    editor = BaseEditor.from_hparams(hparams)

    metrics, edited_model, _ = editor.edit(
        prompts=prompts,
        rephrase_prompts=rephrase_prompts,
        target_new=target_new,
        subject=subject,
        train_ds=train_ds,
        locality_inputs=locality_inputs,
        portability_inputs=portability_inputs,
        keep_original_weight=False
    )

    print(edited_model)
    print(type(edited_model))
    print(hasattr(edited_model, "active_adapters"))
    if hasattr(edited_model, "active_adapters"):
        print("Active adapters after editor.edit():", edited_model.active_adapters)

print("\nTrainable parameters:")
edited_model.print_trainable_parameters()

print("\nNamed parameters containing 'lora':")
for name, param in edited_model.named_parameters():
    if "lora" in name.lower():
        print(name, param.shape, param.requires_grad)

print("\nAdapter config:")
print(edited_model.peft_config)

print("\nAdapter state dict keys:")
print(type(edited_model))
print(hasattr(edited_model, "active_adapters"))
if hasattr(edited_model, "active_adapters"):
    print(edited_model.active_adapters)


vm = VersionManager()

version_number, version_path = vm.create_new_version()

print(f"\nCreating Version {version_number}")
print(f"Saving adapter to: {version_path}")

edited_model.save_pretrained(version_path)

print(f"Version {version_number} saved successfully.")

json.dump(
    metrics,
    open(
        os.path.join(args.metrics_save_dir, f'{args.editing_method}_results.json'),
        'w'
    ),
    indent=4
)
