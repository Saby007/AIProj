
# Import libraries
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from azure.identity import get_bearer_token_provider
from azure.core.paging import ItemPaged


def getOpenAIClient(token_provider):
    print("token_provider", token_provider)
    return AzureOpenAI(
        api_version="2024-05-01-preview",
        azure_endpoint="<Your Azure OpenAI endpoint>",
        azure_ad_token_provider=token_provider
    )

def getSearchClient(credential):
    return SearchClient(
        endpoint="<Your Azure Search endpoint>",
        index_name="<Your index name>",
        credential=credential
    )

def ragCall(user_query, openai_client, search_client, deployment_name):
    # Provide instructions to the model
    GROUNDED_PROMPT="""
        You are an AI assistant that helps users learn from the information found in the source material.
        Answer the query using only the sources provided below.
        Use bullets if the answer has multiple points.
        If the answer is longer than 3 sentences, provide a summary.
        Answer ONLY with the facts listed in the list of sources below. Cite your source when you answer the question
        Query: {query}
        Sources:\n{sources}
    """
    #vector_query = VectorizableTextQuery(text=user_query, k_nearest_neighbors=50, fields="text_vector")
    print("Initiated Search!!")
    search_results = search_client.search(
        search_text=user_query,
        #vector_queries= [vector_query],
        select=["chunk"],
        top=5      
    )
    
    sources_formatted = "=================\n".join([f'CONTENT: {document["chunk"]}' for document in search_results])
    #sources_formatted = "\n=================\n".join('concur is good')

    print("coming here!!")

    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": GROUNDED_PROMPT.format(query=user_query, sources=sources_formatted)
            }
        ],
        model=deployment_name
    )

    return response.choices[0].message.content


# main rag function
def ragApp(user_query, credential):
    print("token provider")
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    print("token provider:", token_provider)
    openai_client = getOpenAIClient(token_provider)
    print("openai_client:", openai_client)
    deployment_name = "gpt-4o"
    search_client = getSearchClient(credential)
    print("search_client:", search_client)
    return ragCall(user_query, openai_client, search_client, deployment_name)

    
