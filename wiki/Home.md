# AnswerRocket Python Client

Welcome to the AnswerRocket Python Client documentation! This library provides programmatic access to AnswerRocket's generative AI analytics platform.

## What is AnswerRocket?

AnswerRocket is a generative AI analytics platform for enterprise data exploration. It provides:
- Natural language interface for business intelligence queries
- AI agents for instant data insights and visualizations
- Automated reporting and analytics workflows

## Quick Start

### Installation

```bash
pip install answerrocket-client
```

### Basic Usage

```python
from answer_rocket import AnswerRocketClient

# Initialize the client
arc = AnswerRocketClient(
    url='https://your-answerrocket-instance.com',
    token='<your_api_token>'
)

# Test connection
arc.can_connect()
```

### Authentication

You can authenticate using either direct parameters or environment variables (recommended):

```bash
export AR_URL="https://your-instance.com"
export AR_TOKEN="your_api_token"
```

```python
# Client will automatically use environment variables
arc = AnswerRocketClient()
```

API tokens are available through the AnswerRocket UI for authenticated users.

## Key Components

The AnswerRocket client provides access to several key modules:

- **[client](API-Client)** - Main client class for initialization and connection
- **[data](API-Data)** - SQL/RQL execution, dataset operations, AI-powered SQL generation
- **[chat](API-Chat)** - Natural language questions to AI copilots
- **[config](API-Config)** - Configuration and artifact management
- **[output](API-Output)** - Output and visualization building
- **[skill](API-Skill)** - Skill management
- **[llm](API-Llm)** - Language model operations

## Common Use Cases

### Execute SQL Queries

```python
database_id = "my_database_id"
sql = "SELECT sum(revenue) FROM sales WHERE year = 2024"

result = arc.data.execute_sql_query(database_id, sql, limit=100)

if result.success:
    print(result.df)  # pandas DataFrame
else:
    print(f"Error: {result.error}")
```

### Ask Natural Language Questions

```python
copilot_id = "your_copilot_id"
question = "What were our top selling products last quarter?"

entry = arc.chat.ask_question(copilot_id, question)
print(entry)
```

### AI-Powered SQL Generation

```python
database_id = "my_database_id"
question = "Show me revenue by region for Q4"

result = arc.data.run_sql_ai(database_id, question)

if result.success:
    print(f"Generated SQL: {result.sql}")
    print(result.df)
```

### Language Model Interactions

```python
messages = [
    {"role": "system", "content": "You are a data analyst assistant."},
    {"role": "user", "content": "What is the average of 150, 12, 200, 54, 24, and 32?"}
]

success, reply = arc.llm.completion(messages=messages)

if success:
    content = reply["choices"][0]["message"]["content"]
    print(content)
```

### Streaming Responses

```python
def display_streaming_result(chunk):
    print(chunk, end="", flush=True)

success, reply = arc.llm.completion(
    messages=messages,
    stream_callback=display_streaming_result
)
```

## API Reference

For detailed documentation of all classes, methods, and parameters, see the [API Reference](API-Reference).

## Requirements

- Python >= 3.10.7
- Dependencies: `sgqlc`, `pandas>=1.5.1`, `typing-extensions`

## Support

For issues and questions:
- GitHub Issues: [answerrocket/answerrocket-python-client](https://github.com/answerrocket/answerrocket-python-client/issues)
- Documentation: This wiki

## Notes

- When running outside of an AnswerRocket installation (e.g., during development), make sure to set the OpenAI API key:
  ```python
  import os
  os.environ['OPENAI_API_KEY'] = 'your_openai_key'
  ```
