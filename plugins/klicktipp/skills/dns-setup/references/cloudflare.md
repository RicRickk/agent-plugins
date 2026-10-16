## Provider: Cloudflare

Prefer an already-connected official Cloudflare integration. If none is connected, offer to connect Cloudflare through the client's settings/plugins and have the user authorize access to the intended zone. Obtain approval before setting up the connection; obtain separate approval for the exact DNS changes after inspecting existing records.

Where the client supports adding a remote MCP server instead, Cloudflare's official API MCP server is at `https://mcp.cloudflare.com/mcp`. It uses Cloudflare OAuth and supports DNS record management. Use the API MCP server for record changes; the separate DNS Analytics server is for analysis, not DNS record management.

Set KlickTipp CNAME records to DNS-only (`proxied: false`). Follow the record inspection, approval, and verification workflow above. If the user cannot or does not want to connect Cloudflare, guide them through **Cloudflare dashboard > select zone > DNS > Records**.

Explain DNS-only through the observable DNS answer: a proxied CNAME may return Cloudflare IPs instead of the CNAME target KlickTipp expects for verification. Do not infer the current Cloudflare proxy toggle, live DKIM outcome or click-tracking path solely from KlickTipp's stored DNS result. Verify how the selected Cloudflare zone accepts record names before telling the user to enter full or relative hostnames.

Source: [Cloudflare's own MCP servers](https://developers.cloudflare.com/agents/model-context-protocol/cloudflare/servers-for-cloudflare/)
