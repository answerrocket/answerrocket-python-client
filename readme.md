# AnswerRocket Skill API Client
This is a client library for interacting with an AnswerRocket instance.  Its purpose is to enable the development of skills (custom AnswerRocket extensions) without the need for AnswerRocket to be running locally.

## Installation

`pip install answerrocket-client`

## Use

```
import json
from answer_rocket import AnswerRocketClient
arc = AnswerRocketClient(url='https://your-answerrocket-instance.com', token='<your_api_token>')
# test that the config is valid
arc.can_connect()

# Gets a resource file.  When running in an AnswerRocket instance, this call will fetch a customized version of the resource if one has been created.
some_resource = json.loads(arc.config.get_artifact('path/to/my/file.json'))
```

Note that both the token and instance URL can be provided via the AR_TOKEN and AR_URL env vars instead, respectively. This is recommended to avoid accidentally committing a dev api token in your skill code.

# Working on the SDK
## Setup
This repository contains a .envrc file for use with direnv. With that installed you should have a separate python interpreter that direnv's hook will activate for you when you cd into this repository.

Once you have direnv set up and activating inside the repo, just `make` to install dev dependencies and get started.

## Finding things in the codebase
The main point of contact with users of this sdk is `AnswerRocketClient` in `answer_rocket/client.py`. That is, it is what users will import and initialize. Different categories of utilities can be grouped into modules in whatever way is most convenient, but they should be exposed via the client rather than through a separate import so that utilities for authentication, etc., can be reused.

The client hits an sdk-specific GraphQL API on its target AnswerRocket server. There is a `graphql/schema.py` with generated python types for what queries are available. When needed it can be regenerated with the `generate-gql-schema` makefile target. See the Makefile for details.