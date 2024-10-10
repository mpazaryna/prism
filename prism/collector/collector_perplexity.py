import json
import os

import requests

from prism.utils.logging import setup_logger

# Set up the logger
logger = setup_logger("collector_perplexity", "logs/collector_perplexity.log")


def get_perplexity_response(query, company_domain):
    api_key = os.environ.get("PERPLEXITY_API_KEY")

    if not api_key:
        logger.error("API key is not set in the environment variables.")
        raise ValueError(
            "API key is required but not set in the environment variables."
        )

    url = "https://api.perplexity.ai/chat/completions"

    payload = json.dumps(
        {
            "model": "llama-3.1-sonar-huge-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise. Return as much information as possible.",
                },
                {"role": "user", "content": f"{query}"},
            ],
            "max_tokens": "2000",
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": True,
            "search_domain_filter": ["perplexity.ai", f"{company_domain}"],
            "return_images": False,
            "return_related_questions": True,
            "search_recency_filter": "month",
            "top_k": 0,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1,
        }
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        response_json = response.json()

        # Extract the content from the response
        content = response_json["choices"][0]["message"]["content"]

        # Log the content
        logger.info(f"Perplexity response for query '{query}': {content}")

        return content
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to Perplexity API: {str(e)}")
        logger.error(f"Response content: {response.text}")
        raise
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing Perplexity API response: {str(e)}")
        logger.error(f"Response content: {response_json}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from Perplexity API: {str(e)}")
        logger.error(f"Response content: {response.text}")
        raise


if __name__ == "__main__":
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    query = "What do you know about Mount Vernon Mills?"
    company_domain = "mvmills.com"
    result = get_perplexity_response(query, company_domain)
    print(result)
