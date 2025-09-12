Remote MCP that just works: [FastMCP Cloud is here!](https://fastmcp.link/IhmBxWn)

[FastMCP home page![light logo](https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/brand/logo-wordmark.svg?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=50f89aaf6046785dc41e9ee0880493e9)![dark logo](https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/brand/logo-wordmark-dark.svg?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=d648968cf938aa5fcab93a2f4d42ed78)](https://gofastmcp.com/)

Search the docs...

Ctrl K

Search...

Navigation

Authentication

OAuth Authentication

[Documentation](https://gofastmcp.com/getting-started/welcome) [What's New](https://gofastmcp.com/updates) [SDK Reference](https://gofastmcp.com/python-sdk/fastmcp-exceptions)

On this page

- [Client Usage](https://gofastmcp.com/clients/auth/oauth#client-usage)
- [Default Configuration](https://gofastmcp.com/clients/auth/oauth#default-configuration)
- [OAuth Helper](https://gofastmcp.com/clients/auth/oauth#oauth-helper)
- [OAuth Parameters](https://gofastmcp.com/clients/auth/oauth#oauth-parameters)
- [OAuth Flow](https://gofastmcp.com/clients/auth/oauth#oauth-flow)
- [Token Management](https://gofastmcp.com/clients/auth/oauth#token-management)
- [Token Storage](https://gofastmcp.com/clients/auth/oauth#token-storage)
- [Managing Cache](https://gofastmcp.com/clients/auth/oauth#managing-cache)

`New in version: 2.6.0`

OAuth authentication is only relevant for HTTP-based transports and requires user interaction via a web browser.

When your FastMCP client needs to access an MCP server protected by OAuth 2.1, and the process requires user interaction (like logging in and granting consent), you should use the Authorization Code Flow. FastMCP provides the `fastmcp.client.auth.OAuth` helper to simplify this entire process.This flow is common for user-facing applications where the application acts on behalf of the user.

## [​](https://gofastmcp.com/clients/auth/oauth\#client-usage)  Client Usage

### [​](https://gofastmcp.com/clients/auth/oauth\#default-configuration)  Default Configuration

The simplest way to use OAuth is to pass the string `"oauth"` to the `auth` parameter of the `Client` or transport instance. FastMCP will automatically configure the client to use OAuth with default settings:

Copy

```
from fastmcp import Client

# Uses default OAuth settings
async with Client("https://fastmcp.cloud/mcp", auth="oauth") as client:
    await client.ping()

```

### [​](https://gofastmcp.com/clients/auth/oauth\#oauth-helper)  `OAuth` Helper

To fully configure the OAuth flow, use the `OAuth` helper and pass it to the `auth` parameter of the `Client` or transport instance. `OAuth` manages the complexities of the OAuth 2.1 Authorization Code Grant with PKCE (Proof Key for Code Exchange) for enhanced security, and implements the full `httpx.Auth` interface.

Copy

```
from fastmcp import Client
from fastmcp.client.auth import OAuth

oauth = OAuth(mcp_url="https://fastmcp.cloud/mcp")

async with Client("https://fastmcp.cloud/mcp", auth=oauth) as client:
    await client.ping()

```

#### [​](https://gofastmcp.com/clients/auth/oauth\#oauth-parameters)  `OAuth` Parameters

- **`mcp_url`** ( `str`): The full URL of the target MCP server endpoint. Used to discover OAuth server metadata
- **`scopes`** ( `str | list[str]`, optional): OAuth scopes to request. Can be space-separated string or list of strings
- **`client_name`** ( `str`, optional): Client name for dynamic registration. Defaults to `"FastMCP Client"`
- **`token_storage_cache_dir`** ( `Path`, optional): Token cache directory. Defaults to `~/.fastmcp/oauth-mcp-client-cache/`
- **`additional_client_metadata`** ( `dict[str, Any]`, optional): Extra metadata for client registration
- **`callback_port`** ( `int`, optional): Fixed port for OAuth callback server. If not specified, uses a random available port

## [​](https://gofastmcp.com/clients/auth/oauth\#oauth-flow)  OAuth Flow

The OAuth flow is triggered when you use a FastMCP `Client` configured to use OAuth.

1

Token Check

The client first checks the `token_storage_cache_dir` for existing, valid tokens for the target server. If one is found, it will be used to authenticate the client.

2

OAuth Server Discovery

If no valid tokens exist, the client attempts to discover the OAuth server’s endpoints using a well-known URI (e.g., `/.well-known/oauth-authorization-server`) based on the `mcp_url`.

3

Dynamic Client Registration

If the OAuth server supports it and the client isn’t already registered (or credentials aren’t cached), the client performs dynamic client registration according to RFC 7591.

4

Local Callback Server

A temporary local HTTP server is started on an available port (or the port specified via `callback_port`). This server’s address (e.g., `http://127.0.0.1:<port>/callback`) acts as the `redirect_uri` for the OAuth flow.

5

Browser Interaction

The user’s default web browser is automatically opened, directing them to the OAuth server’s authorization endpoint. The user logs in and grants (or denies) the requested `scopes`.

6

Authorization Code & Token Exchange

Upon approval, the OAuth server redirects the user’s browser to the local callback server with an `authorization_code`. The client captures this code and exchanges it with the OAuth server’s token endpoint for an `access_token` (and often a `refresh_token`) using PKCE for security.

7

Token Caching

The obtained tokens are saved to the `token_storage_cache_dir` for future use, eliminating the need for repeated browser interactions.

8

Authenticated Requests

The access token is automatically included in the `Authorization` header for requests to the MCP server.

9

Refresh Token

If the access token expires, the client will automatically use the refresh token to get a new access token.

## [​](https://gofastmcp.com/clients/auth/oauth\#token-management)  Token Management

### [​](https://gofastmcp.com/clients/auth/oauth\#token-storage)  Token Storage

OAuth access tokens are automatically cached in `~/.fastmcp/oauth-mcp-client-cache/` and persist between application runs. Files are keyed by the OAuth server’s base URL.

### [​](https://gofastmcp.com/clients/auth/oauth\#managing-cache)  Managing Cache

To clear the tokens for a specific server, instantiate a `FileTokenStorage` instance and call the `clear` method:

Copy

```
from fastmcp.client.auth.oauth import FileTokenStorage

storage = FileTokenStorage(server_url="https://fastmcp.cloud/mcp")
await storage.clear()

```

To clear _all_ tokens for all servers, call the `clear_all` method on the `FileTokenStorage` class:

Copy

```
from fastmcp.client.auth.oauth import FileTokenStorage

FileTokenStorage.clear_all()

```

[Roots](https://gofastmcp.com/clients/roots) [Bearer Auth](https://gofastmcp.com/clients/auth/bearer)

Assistant

Responses are generated using AI and may contain mistakes.