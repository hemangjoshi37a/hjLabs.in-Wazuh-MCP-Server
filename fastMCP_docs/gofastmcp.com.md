Remote MCP that just works: [FastMCP Cloud is here!](https://fastmcp.link/IhmBxWn)

[FastMCP home page![light logo](https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/brand/logo-wordmark.svg?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=50f89aaf6046785dc41e9ee0880493e9)![dark logo](https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/brand/logo-wordmark-dark.svg?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=d648968cf938aa5fcab93a2f4d42ed78)](https://gofastmcp.com/)

Search the docs...

Ctrl K

Search...

Navigation

Get Started

Welcome to FastMCP 2.0!

[Documentation](https://gofastmcp.com/getting-started/welcome) [What's New](https://gofastmcp.com/updates) [SDK Reference](https://gofastmcp.com/python-sdk/fastmcp-exceptions)

On this page

- [Beyond the Protocol](https://gofastmcp.com/getting-started/welcome#beyond-the-protocol)
- [What is MCP?](https://gofastmcp.com/getting-started/welcome#what-is-mcp%3F)
- [Why FastMCP?](https://gofastmcp.com/getting-started/welcome#why-fastmcp%3F)
- [LLM-Friendly Docs](https://gofastmcp.com/getting-started/welcome#llm-friendly-docs)

The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is a new, standardized way to provide context and tools to your LLMs, and FastMCP makes building MCP servers and clients simple and intuitive. Create tools, expose resources, define prompts, and more with clean, Pythonic code:

Copy

```
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()

```

## [​](https://gofastmcp.com/getting-started/welcome\#beyond-the-protocol)  Beyond the Protocol

FastMCP is the standard framework for working with the Model Context Protocol. FastMCP 1.0 was incorporated into the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) in 2024.This is FastMCP 2.0, the **actively maintained version** that provides a complete toolkit for working with the MCP ecosystem.FastMCP 2.0 has a comprehensive set of features that go far beyond the core MCP specification, all in service of providing **the simplest path to production**. These include deployment, auth, clients, server proxying and composition, generating servers from REST APIs, dynamic tool rewriting, built-in testing tools, integrations, and more.Ready to upgrade or get started? Follow the [installation instructions](https://gofastmcp.com/getting-started/installation), which include steps for upgrading from the official MCP SDK.

## [​](https://gofastmcp.com/getting-started/welcome\#what-is-mcp%3F)  What is MCP?

The Model Context Protocol lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. It is often described as “the USB-C port for AI”, providing a uniform way to connect LLMs to resources they can use. It may be easier to think of it as an API, but specifically designed for LLM interactions. MCP servers can:

- Expose data through `Resources` (think of these sort of like GET endpoints; they are used to load information into the LLM’s context)
- Provide functionality through `Tools` (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- Define interaction patterns through `Prompts` (reusable templates for LLM interactions)
- And more!

FastMCP provides a high-level, Pythonic interface for building, managing, and interacting with these servers.

## [​](https://gofastmcp.com/getting-started/welcome\#why-fastmcp%3F)  Why FastMCP?

The MCP protocol is powerful but implementing it involves a lot of boilerplate - server setup, protocol handlers, content types, error management. FastMCP handles all the complex protocol details and server management, so you can focus on building great tools. It’s designed to be high-level and Pythonic; in most cases, decorating a function is all you need.FastMCP 2.0 has evolved into a comprehensive platform that goes far beyond basic protocol implementation. While 1.0 provided server-building capabilities (and is now part of the official MCP SDK), 2.0 offers a complete ecosystem including client libraries, authentication systems, deployment tools, integrations with major AI platforms, testing frameworks, and production-ready infrastructure patterns.FastMCP aims to be:🚀 **Fast**: High-level interface means less code and faster development🍀 **Simple**: Build MCP servers with minimal boilerplate🐍 **Pythonic**: Feels natural to Python developers🔍 **Complete**: A comprehensive platform for all MCP use cases, from dev to prodFastMCP is made with 💙 by [Prefect](https://www.prefect.io/).

## [​](https://gofastmcp.com/getting-started/welcome\#llm-friendly-docs)  LLM-Friendly Docs

This documentation is also available in [llms.txt format](https://llmstxt.org/), which is a simple markdown standard that LLMs can consume easily.There are two ways to access the LLM-friendly documentation:

- [llms.txt](https://gofastmcp.com/llms.txt) is essentially a sitemap, listing all the pages in the documentation.
- [llms-full.txt](https://gofastmcp.com/llms-full.txt) contains the entire documentation. Note this may exceed the context window of your LLM.

In addition, any page can be accessed as markdown by appending `.md` to the URL. For example, this page would become `https://gofastmcp.com/getting-started/welcome.md`, which you can view [here](https://gofastmcp.com/getting-started/welcome.md).Finally, you can copy the contents of any page as markdown by pressing “Cmd+C” (or “Ctrl+C” on Windows) on your keyboard.

[Installation](https://gofastmcp.com/getting-started/installation)

Assistant

Responses are generated using AI and may contain mistakes.