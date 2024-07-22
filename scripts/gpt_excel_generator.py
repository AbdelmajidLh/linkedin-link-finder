import pandas as pd
import openai
import logging
import os
import time

class GPTExcelGenerator:
    def __init__(self, prompt_template_path):
        with open(prompt_template_path, 'r') as file:
            self.prompt_template = file.read().strip()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def obtenir_reponse_chatgpt(self, prompt):
        retries = 10  # Augmenter le nombre de tentatives
        for i in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500
                )
                return response.choices[0].message['content'].strip()
            except openai.RateLimitError as e:
                wait_time = 2 ** i  # Délai exponentiel
                logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            except openai.APIError as e:
                logging.error(f"OpenAI API returned an API Error: {e}")
                raise e
            except openai.APIConnectionError as e:
                logging.error(f"Failed to connect to OpenAI API: {e}")
                raise e
            except openai.AuthenticationError as e:
                logging.error(f"Authentication error: {e}")
                raise e
            except openai.PermissionDeniedError as e:
                logging.error(f"Permission denied: {e}")
                raise e
            except openai.BadRequestError as e:
                logging.error(f"Bad request: {e}")
                raise e
            except openai.InternalServerError as e:
                logging.error(f"Internal server error: {e}")
                raise e
            except openai.NotFoundError as e:
                logging.error(f"Resource not found: {e}")
                raise e
            except openai.ConflictError as e:
                logging.error(f"Conflict error: {e}")
                raise e
            except openai.UnprocessableEntityError as e:
                logging.error(f"Unprocessable entity: {e}")
                raise e
            except openai.APITimeoutError as e:
                logging.error(f"API request timed out: {e}")
                raise e
        raise Exception("Exceeded maximum retries due to rate limit.")

    def sauvegarder_dans_excel(self, reponse, output_file_path):
        lines = reponse.split("\n")
        data = [line.split(",") for line in lines if line.strip() != '']
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_excel(output_file_path, index=False)
        logging.info(f"Excel file saved to {output_file_path}")

    def create_prompt_file(self, company_name, text):
        prompt = self.prompt_template + "\n\n" + text
        prompt_file_path = f"prompts/prompt_{company_name}.txt"
        with open(prompt_file_path, 'w') as file:
            file.write(prompt)
        logging.info(f"Prompt file created: {prompt_file_path}")
        return prompt
