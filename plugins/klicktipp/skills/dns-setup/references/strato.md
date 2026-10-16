## Provider: STRATO

STRATO has no supported general DNS CRUD API or CLI. Guide the user through **Domains -> Domain management -> gear -> DNS**.

- TXT: open TXT management and enter a relative prefix such as `_dmarc`.
- CNAME: create/select the required subdomain, then open its CNAME management.

STRATO appends the zone automatically. Its DynDNS endpoint cannot create KlickTipp TXT or CNAME records. Do not use tools that scrape the portal with account credentials.

Source: [STRATO DNS records](https://www.strato.de/faq/domains/wie-kann-ich-bei-strato-meine-dns-eintraege-verwalten/)

