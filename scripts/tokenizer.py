from tokenizers import Tokenizer, models, pre_tokenizers, processors, trainers, decoders
from pandas import *
import csv

# Read the column from the CSV file
with open("../2008-01/train.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    column = [row[5] for row in reader]
# Initialize a tokenizer
tokenizer = Tokenizer(models.BPE())

# Define the pre-tokenizer
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False, trim_offsets=True)
tokenizer.post_processor = processors.ByteLevel(add_prefix_space=True, trim_offsets=False)
tokenizer.decoder = decoders.ByteLevel(add_prefix_space=True, trim_offsets=True)
# Define the trainer
trainer = trainers.BpeTrainer(vocab_size=30000, min_frequency=2)

# Train the tokenizer
# tokenizer.train(files=["train.csv"], trainer=trainer)
tokenizer.train_from_iterator(column, trainer=trainer)
# Save the tokenizer
tokenizer.save("bytebpe_combined_30k")
