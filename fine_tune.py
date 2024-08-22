import json

from transformers import (DataCollatorForLanguageModeling, GPT2LMHeadModel,
                          GPT2Tokenizer, TextDataset, Trainer,
                          TrainingArguments)

# Load the pre-trained model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Prepare the dataset
def load_dataset(file_path, tokenizer):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    texts = [f"Title: {item['title']}\n\nContent: {item['content']}" for item in data]
    
    # Tokenize and save as a temporary file
    with open('temp_dataset.txt', 'w') as f:
        for text in texts:
            f.write(text + tokenizer.eos_token + '\n')
    
    return TextDataset(
        tokenizer=tokenizer,
        file_path='temp_dataset.txt',
        block_size=128)

train_dataset = load_dataset('squat_university_data.json', tokenizer)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False,
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./gpt2-squat-university",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Train the model
trainer.train()

# Save the model
trainer.save_model()
