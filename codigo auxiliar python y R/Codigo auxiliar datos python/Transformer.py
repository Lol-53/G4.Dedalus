from datasets import load_dataset
from transformers import AutoTokenizer

# Cargar el dataset
dataset = load_dataset("json", data_files={"train": "dataset_squad.json"})

# Usar un tokenizer en español
tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-cased")

# Tokenizar datos
def preprocess_function(examples):
    return tokenizer(
        examples["question"],
        examples["context"],
        truncation=True,
        padding="max_length",
        max_length=384
    )

tokenized_datasets = dataset.map(preprocess_function, batched=True)
