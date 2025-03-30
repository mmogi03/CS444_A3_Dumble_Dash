"""
This module is used to search for sounds in FreeSound using the FreeSound API.

Basic usage:
(1) Convert sound descriptions into query keywords using LLMs.
(2) Querying FreeSound, returning a list, each element is a dictionary with the freesound object and description.
(3) Based on search results, use LLM to select the best sound for the query, or decide to abandon the search.

Advanced usage:
(4) Based on search results, refine the query.
(5) Construct the pipeline for search-refine-search-refine...

"""

import os
import json5
from freesound import FreesoundClient, Sound
import requests
from bs4 import BeautifulSoup
from retrying import retry
import re

from prompts import PROMPTS

class SoundSearcher:
    client = None
    verbose: bool = False
    prompt_dir: str = "audios/sfx/soundSearch"

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.client = FreesoundClient()
        self.client.set_token(os.environ.get("FREESOUND_CLIENT_API_KEY"),"token")

    def log(self, message: str):
        if self.verbose:
            print(message)

    @retry(wait_fixed=2000, stop_max_attempt_number=10)
    def create_query(self, description: str) -> str:
        """
        Create a query from a description.
        """
        # read prompts
        sys_prompt = PROMPTS["create_query"]

        # split the sys_prompt into two parts by "{system_prompt_end}"
        sys_prompt, user_input = sys_prompt.split("{system_prompt_end}")

        # add the description and result_in_str to the user_input
        # by replacing "{description}" and "{results}" with the actual content
        user_input = user_input.replace("{description}", description)
        
        # chat with GPT with retrying
        response = chat_with_gpt(sys_prompt, user_input)

        # extract the content from triple ticks
        matches = re.findall(r'```([^`]*)```', response)
        if matches:
            response = matches[0].strip("\n ")
        else:
            response = response.strip()

        return response


    def search(self, query: str, duration: int = 5, max_results: int = 8) -> list[dict]:
        """
        Search for sounds in FreeSound using the query.
        """
        results = self.client.text_search(query=query, filter=f"duration:[{duration} TO *]")

        # fetch descriptions of the sounds
        item_counter = 0
        fetched_results = []
        for sound in results:
            if item_counter >= max_results:
                break

            sound_id = sound.id
            sound_user = sound.username
            sound_url = f"https://freesound.org/people/{sound_user}/sounds/{sound_id}/"

            # use requests to get the html of sound_url
            page = requests.get(sound_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # get the content in #soundDescriptionSection
            sound_description = soup.find(id="soundDescriptionSection")

            # clean the content by removing the html tags
            import re
            sound_description = re.sub(r'<.*?>', '', str(sound_description))

            # add the sound to fetched_results
            fetched_results.append({
                "sound": sound,
                "name": sound.name,
                "description": sound_description,
            })

            item_counter += 1

        return fetched_results
    
    def stringtify_fetched_results(self, fetched_results: list) -> str:
        """
        Stringtify the fetched results.
        """
        if len(fetched_results) == 0:
            return "No sound is found."
        
        result_in_str = ""
        for result_id, result in enumerate(fetched_results):
            result_in_str += "---------------------\n"
            result_in_str += f"Sound ID: {result_id}\n"
            result_in_str += f"Sound name: {result['name']}\n"
            result_in_str += f"Description: {result['description']}\n"
            result_in_str += "\n"
        return result_in_str
    
    @retry(wait_fixed=2000, stop_max_attempt_number=3)
    def choose_sound(self, description: str, fetched_results: list) -> dict:
        """
        Choose the best sound from the fetched results.
        """
        assert len(fetched_results) > 0
        result_in_str = self.stringtify_fetched_results(fetched_results)

        # read prompts from audios/soundSearch/choose_prompt.txt
        sys_prompt = PROMPTS["choose_sound"]
        sys_prompt, user_input = sys_prompt.split("{system_prompt_end}")

        # add the description and result_in_str to the user_input
        # by replacing "{description}" and "{results}" with the actual content
        user_input = user_input.replace("{description}", description)
        user_input = user_input.replace("{results}", result_in_str)
        
        # chat with GPT with retrying
        choice = chat_with_gpt(sys_prompt, user_input)

        if choice == "-1":
            return None
        # assert response is in the range of fetched_results
        assert (0 <= int(choice) < len(fetched_results))

        # return the chosen sound
        if choice == -1:
            return None
        else:
            return fetched_results[int(choice)]
        
    @retry(wait_fixed=2000, stop_max_attempt_number=3)
    def refine_query(self, description: str, query_list: list, result_list: list) -> dict:
        """
        Choose the best sound from the fetched results and refine the query.
        """
        result_in_str = self.stringtify_fetched_results(result_list[-1])

        # create a search history about queries and the number of results
        search_history = ""
        for i, query in enumerate(query_list):
            search_history += f"Search {i}: {query} -> {len(result_list[i])} results\n"

        # read prompts from audios/soundSearch/choose_prompt.txt
        sys_prompt = PROMPTS["refine_query"]
        # split the sys_prompt into two parts by "{system_prompt_end}"
        sys_prompt, user_input = sys_prompt.split("{system_prompt_end}")

        # update the user_input
        user_input = user_input.replace("{goal}", description)
        user_input = user_input.replace("{query}", query_list[-1])
        user_input = user_input.replace("{results}", result_in_str)
        user_input = user_input.replace("{history}", search_history)
        
        # chat with GPT with retrying
        response_json = chat_with_gpt(sys_prompt, user_input)
        json_string = extract_json_from_quotes(response_json)
        json_dict = json5.loads(json_string)
        json_dict["best_index"] = int(json_dict["best_index"])  # Convert to int
        assert "best_index" in json_dict and "query" in json_dict
        assert isinstance(json_dict["best_index"], int)
        return json_dict
        
    def save_sound(self, chosen_sound_dict: dict, output_path: str, duration: int):
        # get the chosen sound
        chosen_sound: Sound = chosen_sound_dict["sound"]

        # split the output_path into directory and filename
        directory, filename = os.path.split(output_path)
        # change the filename to .mp3 if it ends with .wav
        if filename.endswith(".wav"):
            filename = filename[:-4] + ".mp3"

        self.log(f"Retrieving the chosen sound to {output_path}")
        chosen_sound.retrieve_preview(directory, filename)

        
    def pipeline_basic(self, description: str, output_path: str, duration: int = 5, max_results: int = 8) -> dict:
        """
        The basic pipeline for searching sounds in FreeSound.
        if no sound is chosen, return None. 
        Otherwise, return a dictionary with the chosen sound name and its description.
        """
        self.log(f"Creating query for description: {description}")
        query = self.create_query(description)
        self.log(f"Searching FreeSound with query: {query}")
        fetched_results = self.search(query, duration, max_results)
        # if no sound is fetched, return
        if len(fetched_results) == 0:
            return None

        self.log(f"Choosing the best sound...")
        chosen_sound_dict = self.choose_sound(description, fetched_results)
        # if no sound is chosen, return
        if chosen_sound_dict is None:
            return None
        
        self.log(f"Saving the chosen sound to {output_path}")
        self.save_sound(chosen_sound_dict, output_path, duration)
        return {
            "name": chosen_sound_dict["name"],
            "description": chosen_sound_dict["description"],
        }
    
    def pipeline_self_reflection(self, description: str, output_path: str, duration: int = 5, max_results: int = 8) -> dict:
        """
        The refined pipeline for searching sounds in FreeSound.
        It refines the query based on the fetched results.
        If no sound is chosen, return None.
        Otherwise, return a dictionary such as {"name": chosen_sound_name, "description": chosen_sound_description}.
        """
        query_list = []
        results_list = []
        best_results_list = []

        self.log(f"Creating query for description: {description}")
        query = self.create_query(description)
        query_list.append(query)

        for _ in range(3):
            # search FreeSound with the lastest query
            self.log(f"Searching FreeSound with query: {query_list[-1]}")
            fetched_results = self.search(query_list[-1], duration, max_results)
            if len(fetched_results) == 0:
                self.log(f"No sound is found.")
            results_list.append(fetched_results)

            self.log(f"Refining the query...")
            response_json = self.refine_query(description, query_list, results_list)
            best_index, query = response_json["best_index"], response_json["query"]

            # add the best result to best_results_list
            try:
                if len(fetched_results) > 0:
                    best_result = fetched_results[int(best_index)]
                    self.log(f"Best result in this search: {self.stringtify_fetched_results([best_result])}")
                    best_results_list.append(best_result)
            except Exception as err:
                print(f"Failed to parse the best result index({best_index}): {err}")

            # add current query to query history
            query_list.append(query)

        self.log(f"Searching FreeSound with query: {query_list[-1]}")
        fetched_results = self.search(query_list[-1], duration, max_results)
        results_list.append(fetched_results)

        # backtrack the results_list to find the first non-empty fetched_results
        for fetched_results in reversed(results_list):
            if len(fetched_results) > 0:
                break

        # extend the fetched_results with the best_results_list
        fetched_results.extend(best_results_list)

        if len(fetched_results) == 0:
            return None

        # shuffle the fetched_results
        import random
        random.shuffle(fetched_results)

        self.log(f"Choosing the best sound...")
        self.log(f"results: {self.stringtify_fetched_results(fetched_results)}")
        chosen_sound_dict = self.choose_sound(description, fetched_results)
        if chosen_sound_dict is None:
            return None
        
        self.log(f"Saving the chosen sound to {output_path}")
        try:
            self.save_sound(chosen_sound_dict, output_path, duration)
            return {
                "name": chosen_sound_dict["name"],
                "description": chosen_sound_dict["description"],
            }
        except Exception as err:
            print(f"Failed to save the sound. Error: \n{err}")
            return None
        


def chat_with_gpt(sys_prompt, input_prompt):
    from openai import OpenAI
    try:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": sys_prompt
                },
                {
                    "role": "user",
                    "content": input_prompt
                }
            ],
        )
    except Exception as err:
        print(f'OPENAI ERROR: {err}')
        raise err
    
    return response.choices[0].message.content


def extract_json_from_quotes(content):
    import re
    # extract the content between "```json" and "```"
    match = re.search(r'```json(.*)```', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("cannot find the json content")