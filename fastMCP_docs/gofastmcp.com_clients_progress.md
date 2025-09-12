Remote MCP that just works: [FastMCP Cloud is here!](https://fastmcp.link/IhmBxWn)

[FastMCP home page![light logo](https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/brand/logo-wordmark.svg?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=50f89aaf6046785dc41e9ee0880493e9)![dark logo](https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/brand/logo-wordmark-dark.svg?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=d648968cf938aa5fcab93a2f4d42ed78)](https://gofastmcp.com/)

Search the docs...

Ctrl K

Search...

Navigation

Advanced Features

Progress Monitoring

[Documentation](https://gofastmcp.com/getting-started/welcome) [What's New](https://gofastmcp.com/updates) [SDK Reference](https://gofastmcp.com/python-sdk/fastmcp-exceptions)

On this page

- [Progress Handler](https://gofastmcp.com/clients/progress#progress-handler)
- [Handler Parameters](https://gofastmcp.com/clients/progress#handler-parameters)
- [Per-Call Progress Handler](https://gofastmcp.com/clients/progress#per-call-progress-handler)

`New in version: 2.3.5` MCP servers can report progress during long-running operations. The client can receive these updates through a progress handler.

## [​](https://gofastmcp.com/clients/progress\#progress-handler)  Progress Handler

Set a progress handler when creating the client:

Copy

```
from fastmcp import Client

async def my_progress_handler(
    progress: float,
    total: float | None,
    message: str | None
) -> None:
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {percentage:.1f}% - {message or ''}")
    else:
        print(f"Progress: {progress} - {message or ''}")

client = Client(
    "my_mcp_server.py",
    progress_handler=my_progress_handler
)

```

### [​](https://gofastmcp.com/clients/progress\#handler-parameters)  Handler Parameters

The progress handler receives three parameters:

## Progress Handler Parameters

[​](https://gofastmcp.com/clients/progress#param-progress)

progress

float

Current progress value

[​](https://gofastmcp.com/clients/progress#param-total)

total

float \| None

Expected total value (may be None)

[​](https://gofastmcp.com/clients/progress#param-message)

message

str \| None

Optional status message (may be None)

## [​](https://gofastmcp.com/clients/progress\#per-call-progress-handler)  Per-Call Progress Handler

Override the progress handler for specific tool calls:

Copy

```
async with client:
    # Override with specific progress handler for this call
    result = await client.call_tool(
        "long_running_task",
        {"param": "value"},
        progress_handler=my_progress_handler
    )

```

[Logging](https://gofastmcp.com/clients/logging) [Sampling](https://gofastmcp.com/clients/sampling)

Assistant

Responses are generated using AI and may contain mistakes.