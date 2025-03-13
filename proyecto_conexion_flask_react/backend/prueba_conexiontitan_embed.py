# VERSION 2:

# from langchain.chat_models import ChatOpenAI
# from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,)
# from langchain.schema import HumanMessage, SystemMessagechat =
# ChatOpenAI(
#     openai_api_base="http://0.0.0.0:4000",
#     model = "bedrock/amazon.titan-embed-text-v2:0",
#     temperature=0.1 )
#
# messages = [
#     SystemMessage(content="You are a helpful assistant that im using to make a test request to."),
#     HumanMessage(content="test from litellm. tell me why it's amazing in 1 sentence"),
# ]
#
# response = chat(messages)
# print(response)

# VERSION 1:

# import openai
#
# client = openai.OpenAI(
#     api_key="sk-lqIaTaCA6djhkYLWFx5Gww",
#     base_url="https://litellm.dccp.pbu.dedalus.com" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
# )
# response = client.chat.completions.create(
#     model="bedrock/amazon.titan-embed-text-v2:0", # model to send to the proxy
#     messages = [
#         {"role": "user",
#          "content": "this is a test request, write a short poem"}
#     ]
# )
# print(response)

# primer intento V1: dice lo de los parametros no soportados de nuevo

# import openai
# import numpy as np
#
# # Configurar el cliente OpenAI con el proxy LiteLLM
# client = openai.OpenAI(
#     api_key="sk-lqIaTaCA6djhkYLWFx5Gww",
#     base_url="https://litellm.dccp.pbu.dedalus.com"
# )
#
# # Texto de ejemplo para generar embeddings
# text = "Este es un ejemplo de texto para generar embeddings."
#
# # Solicitud para obtener los embeddings
# response = client.embeddings.create(
#     model="bedrock/amazon.titan-embed-text-v2:0",
#     input=text
# )
#
# # Extraer los embeddings del resultado
# embeddings = response.data[0].embedding
#
# # Mostrar los embeddings
# print("Embeddings generados:", np.array(embeddings))

# from langchain.chat_models import ChatOpenAI
# from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,)
# from langchain.schema import HumanMessage, SystemMessage
#
# chat = ChatOpenAI(
#     api_key="sk-lqIaTaCA6djhkYLWFx5Gww",
#     openai_api_base="https://litellm.dccp.pbu.dedalus.com",
#     model = "bedrock/amazon.titan-embed-text-v2:0",
#     temperature=0.1 )
#
# messages = [
#     SystemMessage(content="You are a helpful assistant that im using to make a test request to."),
#     HumanMessage(content="test from litellm. tell me why it's amazing in 1 sentence"),
# ]
#
# response = chat(messages)
# print(response)

import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_aws import BedrockLLM
from langchain.chains import create_retrieval_chain
import json

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    endpoint_url="https://litellm.dccp.pbu.dedalus.com",
    aws_access_key_id="sk-lqIaTaCA6djhkYLWFx5Gww",
    aws_secret_access_key="sk-lqIaTaCA6djhkYLWFx5Gww",  # Repite la misma clave si solo tienes una
    region_name="us-east-1"
)

bedrock_embeddings = BedrockEmbeddings(model_id="bedrock/amazon.titan-embed-text-v2:0",
                                       client=bedrock_client)

response = bedrock_embeddings.embed_query("Hello world 4G")
print(response)
