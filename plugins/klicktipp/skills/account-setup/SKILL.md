---
name: account-setup
description: Guide initial KlickTipp account setup, sending readiness and first safe newsletter test; explain a product-confirmed upgrade path when the selected account lacks MCP access. Use for onboarding or "KlickTipp einrichten". DNS records, DOI details, email content and dispatch belong to their specialist skills.
---

# KlickTipp account setup

Bring the customer's **selected account** from its current state to the smallest usable setup for their stated goal. Start with what already exists. Carry forward confirmed answers; ask only for missing decisions that affect the next step. A homepage may suggest audience and offer, but present those as assumptions until the customer confirms them.

## Establish scope and access

- Identify the selected account and whether the customer wants MCP access, sending readiness, or both. A successful sign-in is not proof that this account may use AI/MCP. A skill cannot itself make a chat open automatically after plugin installation; treat any proposed onboarding gate as a separate client capability to verify.
- Read the current account/capability response and its live tool contract. Treat product-provided eligibility, available plan, required plan, upgrade destination, and retry guidance as the source of truth. Do not infer entitlements from a plan name or from `validate-account-sending-readiness`.
- If the product explicitly says this account may upgrade to enable MCP, say so plainly and give its returned upgrade link in text. Explain that the customer must complete the account change; do not book or purchase on their behalf.
- If the refusal concerns authentication, account selection, permissions, a blocked account, a limit, or a temporary error, explain that actual issue and its supplied remedy. Do not present an upgrade as the fix unless the product response confirms it.
- After the customer reports an upgrade, retry a suitable read-only access check. If access is not yet available, use the current response to explain whether to reconnect, wait, or contact support. Never ask for a password, API key, billing data, or a screenshot of secrets in chat.

When account capability details are unavailable, state what can be verified and what is missing. Do not invent current prices, tariff rules, or a generic checkout URL. Keep the guidance usable in clients without widgets.

## Build on the existing setup

1. Capture the customer's immediate goal and business context. Ask for a public website URL or, if there is none, a short description of the business; reuse one already supplied. From the site, identify likely offer, audience and brand tone, then confirm the details that matter for the intended setup. Ask for the intended sending address and Du/Sie preference when relevant. In a first-login flow that begins with the sending address, accept that answer first. Carry a concise summary of confirmed facts into the relevant specialist work in this conversation. Do not claim that chat context or an email-builder prompt is stored as account-wide AI memory.
2. Read available account settings and, for an email-sending goal, `validate-account-sending-readiness`. Inspect the specific sender domain, sender address, signatures, opt-in processes and contact situation needed for the goal. Inventory relevant User Settings across account identity, sending and consent; distinguish what the MCP actually exposes from sections visible only in the app. A clean sending-readiness result does not establish a complete new-customer setup. Sending readiness and MCP entitlement are separate checks.
3. Show a short status: usable now, missing, and which action is next. Prefer reusing a verified domain, usable sender address, suitable signature and opt-in process over creating duplicates. If the proposed sender is a freemail address such as Gmail, GMX or web.de, ask for the customer's own sending domain or homepage; do not register or select a domain by assumption.
4. For domain records, use current values from KlickTipp and the `dns-setup` skill. DNS provider work may be handled by a connected provider or guided in its portal. Show the exact proposed changes and obtain approval for the external DNS write. A recorded DNS check and a usable sending domain are separate facts.
5. Registering a sender address sends a real confirmation email. Explain that effect before creating it; the recipient confirms the address personally. Reuse or select a suitable signature and inspect the default opt-in process before a new sign-up route uses it: sender, confirmation email, redirect and intended consent scope. Adjust it or create a separate process only when the confirmed customer goal requires that. Do not assert that a placeholder proves the recipient-specific footer is correct.
6. Ask whether the customer already has contacts, and where they are. Reuse contacts already in KlickTipp. For an external CSV or Excel list, ask about its source, columns and consent/status markers without requesting the whole file merely to plan setup. When the customer wants the list checked or imported, use `contacts` and its `references/contact-import.md` for classification, mapping and the supported import path; use `opt-in` for DOI process details. A one-contact upsert is not a bulk import. If no contacts exist, offer an opt-in form or landing page for new sign-ups. Both paths may be needed.
7. For a first one-time newsletter, hand audience, sender, test and dispatch to `newsletter`, body and preview to `email`. For an ongoing or repeatable campaign, hand the flow to `automation` and each message's content to `email`. Use an isolated permitted test recipient. Creating a contact or sending a test can trigger real email, tags, or automations; agree on that effect before execution. Report draft, published, test-sent, scheduled, active and sent as distinct states.

Check current tool schemas before mutations and read back the resulting state. If a tool or account does not expose the required operation, offer a concrete app step or mark the part unverified. Do not claim setup complete from a clean body validator or from a schema description alone.

## Completion report

Summarize the selected account, confirmed goal, MCP access state, sending prerequisites, actions completed, remaining blocks, and the next customer action. Include the evidence for each completed item and explicitly mark anything that still requires a real recipient, domain verification, personalization, publication, or dispatch test.
