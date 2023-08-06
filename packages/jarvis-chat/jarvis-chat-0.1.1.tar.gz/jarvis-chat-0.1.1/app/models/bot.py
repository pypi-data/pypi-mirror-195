import openai

from app.utils.print import print_error

MODEL_NAME = "gpt-3.5-turbo"

class Bot:
    def __init__(self, key):
        openai.api_key = key

    def request(self, chat):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=chat
            )

            return response.choices[0].message.content

        except openai.error.APIError as e:
            print_error(e)

        except openai.error.Timeout as e:
            print_error(e)

        except openai.error.RateLimitError as e:
            print_error(e)

        except openai.error.APIConnectionError as e:
            print_error(e)

        except openai.error.InvalidRequestError as e:
            print_error(e)

        except openai.error.AuthenticationError as e:
            print_error(e)

            