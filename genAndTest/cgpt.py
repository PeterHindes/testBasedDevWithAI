from openai import OpenAI
import os
api_key = os.getenv("OPENAI_API_KEY")
# remove quotes from the api key
api_key = api_key[1:-1]

client = OpenAI(api_key=api_key)

batch_input_file = client.files.create(
  file=open("./batchinput.jsonl", "rb"),
  purpose="batch"
)

batch_input_file_id = batch_input_file.id

batches = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "nightly eval job"
    }
)
batch_ids = [batch.id for batch in batches]

for batch_id in batch_ids:
    batch = client.batches.retrieve(batch_id)
    print(batch)

file_response = client.files.content(batch_input_file_id)
print(file_response.text)