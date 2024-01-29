from transformers import GPT2Tokenizer
from transformers import GPT2LMHeadModel
from transformers import TrainingArguments
from transformers import Trainer, EarlyStoppingCallback
from datasets import Dataset
import pandas as pd

df = pd.read_csv('data/horoscopes.csv', sep = '|', header = None)
df = df.dropna()
df[1].str.lower()

# load the dataset into the Dataset object
dataset = Dataset.from_pandas(df)

# split dataset into train and test using class method
dataset_split = dataset.train_test_split(test_size=0.1, seed=58008)

# Use the tokenizer from the same model as the weights are being used from.
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  

# add a special token for padding
tokenizer.add_special_tokens({'pad_token': '<pad>'})

# a tokenization function to apply on every text in the dataset
def horoscope_tokenizer(horoscope):
    return tokenizer(horoscope['1'], padding='max_length', max_length=100, truncation=True)


tokenized_datasets = dataset_split.map(horoscope_tokenizer)

# lets make sure the size of the first input is set to 100, so the padding worked.
assert (len(tokenized_datasets['train'][0]['input_ids'])) == 100

# add label function for the mapping
def add_labels(example):
    example['labels'] = example["input_ids"].copy()
    return example

# map every example in the dataset, apply add label function
cleaned_datasets = tokenized_datasets.remove_columns(['0', '2', '3'])
cleaned_datasets = tokenized_datasets.map(add_labels)

model = GPT2LMHeadModel.from_pretrained("gpt2")

# resize embedding also for the model
model.resize_token_embeddings(len(tokenizer))

assert model.transformer.wte.weight.shape[0] == len(tokenizer)

training_args = TrainingArguments(
    output_dir="./model/",
    num_train_epochs=5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    logging_dir='./logs',
    logging_steps=25,
    evaluation_strategy="steps",
    eval_steps = 25,
    load_best_model_at_end = True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=cleaned_datasets['train'],
    eval_dataset=cleaned_datasets['test'],
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)

trainer.train()