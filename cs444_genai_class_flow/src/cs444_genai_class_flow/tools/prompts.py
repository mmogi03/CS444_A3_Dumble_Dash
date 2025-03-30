PROMPTS = {}

PROMPTS['create_query'] = """
Given a text desription about a sound effect, please generate a query string that can be used in a search engine. You should only respond in query string.

# Query format

Queries can be composed of positive tags and negative tags such as: ```dog bark +city -cat``` and ```water +river -sea``` where positive tags are preceded with "+" and negative ones with "-"

{system_prompt_end}

# Your task
{description}
"""


PROMPTS['refine_query'] = """
You are an assistant for sound effect searching. Based on current search results, please select the best result and refine the search query string to meet the search goal. 

# Query format

Queries can be composed of positive tags and negative tags such as:
```
dog bark +city -cat
```
where positive tags are preceded with "+" and negative ones with "-"

# Note

If no results found, that means current query is too strict. 
You should shorten the query down to one or two tags.

# Response format

You should only respond in JSON like this:
```json
{
    "best_index": "the index of the best result",
    "query": "refined query",
}
```
{system_prompt_end}

# Search goal
{goal}

# Search history
{history}

# Current query
{query}

# Current results
{results}
"""


PROMPTS['choose_sound'] = """
"Given a text desription about a sound effect, please choose a sound file from the following list. You should only respond in index number. If none of the files is good enough, respond in -1.
{system_prompt_end}

# Sound desription
{description}

# Searched sound files
{results}" 
"""