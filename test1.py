
import os
from langchain.llms           import AzureOpenAI

# Create an instance of Azure OpenAI
# Replace the deployment name with your own

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT") 
os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

#import openai

# Import Azure OpenAI
from langchain.llms import AzureOpenAI

# Create an instance of Azure OpenAI
# Replace the deployment name with your own
llm = AzureOpenAI(
    deployment_name="unibot",
    #model_name="text-davinci-002", 
    model_name="gpt-35-turbo",
    max_tokens=512,
    temperature=0.1
)

# Run the LLM
print( llm("한국의 수도는 어디입니까"))

print(llm)