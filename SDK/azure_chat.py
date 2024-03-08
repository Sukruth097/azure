import os
import openai
openai.api_type = "azure"
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
# openai.api_key = os.getenv("AZURE_OPENAI_KEY")

openai.api_base ="****"
openai.api_key =  "***" 
openai.api_base ="*********"
openai.api_key =  "*******" 

# openai.api_version = "2023-03-15-preview"
openai.api_version = "2023-12-01-preview"

response = openai.ChatCompletion.create(
    engine="test-2", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "what is a bike?"}
    ]
)

print(response)
print(response['choices'][0]['message']['content'])
