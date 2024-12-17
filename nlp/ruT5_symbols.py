import pandas as pd
import torch
import os
import time
from transformers import EarlyStoppingCallback
from transformers import Trainer, TrainingArguments, AutoTokenizer, T5Tokenizer
from transformers import DataCollatorForSeq2Seq, AutoModelForSeq2SeqLM
from datasets import load_dataset
import evaluate
from metrics_symbols import get_metrics
from tqdm.auto import trange


os.environ['WANDB_DISABLED'] = 'true'

# cointegrated/rut5-small
# ai-forever/ruT5-large
# ai-forever/sage-fredt5-large
# ai-forever/FRED-T5-1.7B
# google/mt5-base

tokenizer = AutoTokenizer.from_pretrained('ai-forever/ruT5-large')
model = AutoModelForSeq2SeqLM.from_pretrained('ai-forever/ruT5-large')

directory_datasets = "datasets/symbols"


def preprocess(examples):
    model_inputs = tokenizer(examples['question'], truncation=True, padding=True)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples['answer'], truncation=True, padding=True)
    model_inputs['labels'] = labels['input_ids']
    return model_inputs


def answer(x, **kwargs):
    inputs = tokenizer(x, return_tensors='pt').to(model.device)
    with torch.no_grad():
        hypotheses = model.generate(**inputs, **kwargs, max_length=256)
    return tokenizer.decode(hypotheses[0], skip_special_tokens=True)


def merge_dicts(d1, d2):
    for i, v in d2.items():
        if i not in d1.keys():
            d1[i] = 0
        d1[i] += v
    return d1.copy()


def write_dict_to_file(d, path):
    with open(path, "w", encoding="utf-8") as file:
        for i, v in d.items():
            file.write(f"{i}:{v}\n")


def create_dict():
    new_d = dict()
    for i in dict_correct.keys():
        new_d[i] = dict_correct[i]/dict_all[i]
    return new_d


start = time.perf_counter()

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

data_files = {"train": f"{directory_datasets}/train.csv", "test": f"{directory_datasets}/valid.csv"}

dataset = load_dataset("csv", data_files=data_files, encoding="utf-8")

data_train = dataset["train"].map(preprocess, batched=False)
data_train = data_train.remove_columns(dataset["train"].column_names)

data_test = dataset["test"].map(preprocess, batched=True)
data_test = data_test.remove_columns(dataset["test"].column_names)

model.train()
losses = []

metric = evaluate.load("accuracy")
name = "rut5-large"
training_args = TrainingArguments(
    output_dir=f"./checkpoints/{name}_checkpoints",
    overwrite_output_dir=True,
    num_train_epochs=100,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    # gradient_accumulation_steps=4,
    # fp16=True,
    warmup_steps=0,
    weight_decay=0.01,
    logging_dir='./logs',
    remove_unused_columns=False,
    logging_strategy="epoch",
    metric_for_best_model='eval_loss',
    evaluation_strategy='epoch',
    save_strategy="epoch",
    load_best_model_at_end=True,
    # do_train=True,
    # do_eval=True,
    save_total_limit=3,
    # max_grad_norm=1.0,
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=data_test,
    eval_dataset=data_test,
    data_collator=data_collator,
    tokenizer=tokenizer,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)

trainer.train()
trainer.save_model(f"models_symbols/model_{name}")


print("\nВремя обучения: ", time.perf_counter() - start)


wrong_pairs = open(f"results_symbols/{name}/wrong_pairs.csv", "w", encoding="utf-8")
wrong_pairs.write("expected,result\n")
metrics = open(f"results_symbols/{name}/metrics.txt", "w", encoding="utf-8")

file = pd.read_csv(f"{directory_datasets}/test.csv")

count_all = 0
count_correct = 0

count_sentences_all = 0
count_sentences_correct = 0

dict_all = dict()
dict_correct = dict()

for i in trange(len(file.values)):
    struct = file.values[i]
    ans = answer(struct[0])

    if ans == struct[1]:
        count_sentences_correct += 1
    count_sentences_all += 1

    d_base, d_ans = get_metrics(struct[1], ans)
    for ind, v in d_base.items():
        count_all += v
        if ind in d_ans.keys():
            count_correct += d_ans[ind]
    dict_all = merge_dicts(dict_all, d_base)
    dict_correct = merge_dicts(dict_correct, d_ans & d_base)


result = f"""accuracy(предложения): {count_sentences_correct/count_sentences_all}({count_sentences_correct}/{count_sentences_all})\n
accuracy(слова): {count_correct/count_all}({count_correct}/{count_all})"""


write_dict_to_file(dict_all, f"results_symbols/{name}/dict_all.csv")
write_dict_to_file(dict_correct, f"results_symbols/{name}/dict_correct.csv")

print(result)
metrics.write(result)
write_dict_to_file(create_dict(), f"results_symbols/{name}/dict_res.csv")
wrong_pairs.close()
metrics.close()
