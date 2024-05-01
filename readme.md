# AnswerRocket Skill API Client
This is a client library for interacting with an AnswerRocket instance.

## Installation

`pip install answerrocket-client`

## Use

```
from answer_rocket import AnswerRocketClient
arc = AnswerRocketClient(url='https://your-answerrocket-instance.com', token='<your_api_token>')

# test that the config is valid
arc.can_connect()

# Get a resource file.  When running in an AnswerRocket instance, this call will fetch a customized version of the resource if one has been created.
import json
some_resource = json.loads(arc.config.get_artifact('path/to/my/file.json'))

# to run SQL, get the database ID from an AnswerRocket environment
table_name = "my_table"
sql = "SELECT sum(my_measure) from "+table_name
database_id = "my_database_id"

execute_sql_query_result = arc.data.execute_sql_query(database_id, sql, 100)

if execute_sql_query_result.success:
    print(execute_sql_query_result.df)    
else:
    print(execute_sql_query_result.error)
    print(execute_sql_query_result.code)

# language model calls use the configured settings from the connected Max instance (except for the secret key)
success, model_reply = arc.chat.completion(messages = "hakuna")

if success:
    # the reply is the full value of the LLM's return object
    reply = model_reply["choices"][0]["message"]["content"]
    print(f"** {reply} **")
else:
    # error reply is a description of the exception
    print("Error: "+model_reply)

# chat conversations and streaming replies are supported
messages = [
    { "role":"system",
      "content":"You are an efficient assistant helping a business user answer questions about data."},
    { "role":"user",
      "content":"Can you tell me the average of 150,12,200,54,24 and 32?  are any of these outliers?  Explain why."}
]

def display_streaming_result(str):
    print(str,end="", flush=True)

success, reply = arc.chat.completion(messages = messages, stream_callback=display_streaming_result)

```

Notes: 
- both the token and instance URL can be provided via the AR_TOKEN and AR_URL env vars instead, respectively. This is recommended to avoid accidentally committing a dev api token in your skill code.   API token is available through the AnswerRocket UI for authenticated users.
- when running outside of an AnswerRocket installation such as during development, make sure the openai key is set before importing answer_rocket, like os.environ['OPENAI_API_KEY'] = openai_completion_key.  Get this key from OpenAI.

# Working on the SDK
## Setup
This repository contains a .envrc file for use with direnv. With that installed you should have a separate python interpreter that direnv's hook will activate for you when you cd into this repository.

Once you have direnv set up and activating inside the repo, just `make` to install dev dependencies and get started.

## Finding things in the codebase
The main point of contact with users of this sdk is `AnswerRocketClient` in `answer_rocket/client.py`. That is, it is what users will import and initialize. Different categories of utilities can be grouped into modules in whatever way is most convenient, but they should be exposed via the client rather than through a separate import so that utilities for authentication, etc., can be reused.

The client hits an sdk-specific GraphQL API on its target AnswerRocket server. There is a `graphql/schema.py` with generated python types for what queries are available. When needed it can be regenerated with the `generate-gql-schema` makefile target. See the Makefile for details.
