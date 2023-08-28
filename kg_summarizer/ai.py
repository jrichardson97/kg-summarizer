import warnings

import openai
import tiktoken
import kg_summarizer.config as CFG

openai.organization = CFG.ENV['OPENAI_ORGANIZATION_ID']
openai.api_key = CFG.ENV['OPENAI_API_KEY']

# https://openai.com/pricing   
# https://platform.openai.com/docs/models/gpt-3-5
OPENAI_MODEL_LIMITS = {
    'gpt-3.5-turbo': {
        'max_tokens': 4096,
        'input_price_per_1k_tokens': 0.0015,
        'output_price_per_1k_tokens': 0.002,
    },
    'gpt-3.5-turbo-16k': {
        'max_tokens': 16384,
        'input_price_per_1k_tokens': 0.003,
        'output_price_per_1k_tokens': 0.004,
    },
    'gpt-4': {
        'max_tokens': 8192,
        'input_price_per_1k_tokens': 0.03,
        'output_price_per_1k_tokens': 0.06,
    },
    'gpt-4-32k': {
        'max_tokens': 32768,
        'input_price_per_1k_tokens': 0.06,
        'output_price_per_1k_tokens': 0.12,
    },
}


def num_tokens_from_string(string, model_name):
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def check_token_count_and_price(string, model_name, verbose=True):
    price_per_1k_tokens = OPENAI_MODEL_LIMITS[model_name]['input_price_per_1k_tokens']
    max_tokens = OPENAI_MODEL_LIMITS[model_name]['max_tokens']

    num_tokens = num_tokens_from_string(string, model_name)
    if num_tokens > max_tokens:
        warnings.warn(f"Number of tokens ({num_tokens}) exceeds model max tokens ({max_tokens}).")

    cost = (num_tokens / 1000) * price_per_1k_tokens
    if verbose:
        print(f"Token Count: [{num_tokens}/{max_tokens}]\nPrice: ${cost:.6f}")

    return num_tokens, cost

def generate_response(system_prompt, user_prompt, model='gpt-3.5-turbo', temperature=0.0):
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt},
    ] 

    # Make a request to OpenAI
    completions = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    response = completions.choices[0].message.content

    return response

def general_summarize_abstracts(edge, statement):
    system_prompt = f"""
    You are a biomedical sciences researcher evaluating publication abstracts. You will be given a list of dictionaries with a PMID key and the associated abstract. Find evidence supporting the statement '{statement}' in the abstracts. Structure your response as bullet points starting with the PMID associated with the supporting evidence. List multiple PMIDs if you find related evidence from multiple publications.
    """

    text = generate_response(system_prompt, str(edge['publications']), model='gpt-3.5-turbo-16k')

    system_prompt = f"""
    Read the following list of abstract summaries. Group summaries that have similar conclusions. Structure your response as bullet points beginning with a comma separated list of grouped summaries followed the the main idea of the grouped summaries. 

    Abstract summary list: '{text}'
    """

    return generate_response(system_prompt, '', model='gpt-3.5-turbo-16k'), text