# Enriching contacts with AI (SmartEnrichment)

The automation action `website_enrichment` lets AI fill custom fields of a contact from the website
of the email domain, a LinkedIn profile or a YouTube channel. Setup, prices and field settings for
customers: [Knowledge Base – Contact enrichment with AI](https://www.klicktipp.com/support/knowledge-base/contact-enrichment-with-ai/).
This file adds the steps for a controlled setup.

## Goal and success

The user gets the fields they asked for, filled for the contacts they chose, knows the price, and
has seen the result on a pilot contact before more contacts run. Success is **filled field values
on the pilot contact**.

## Order

1. **Availability and price.** `get-automation-editor-capabilities` (`actionType:
   website_enrichment`) says whether the add-on is active; if not, give the upgrade link it returns
   and stop there.
2. **Pick the source from what the user has.**

   | The user has | Source | Good for |
   |---|---|---|
   | business email addresses | `website` | company, website, industry, offer, target customers, city |
   | a LinkedIn profile URL in a field | `linkedin` with `post_scraping: true` | profile summary, communication style, personality (e.g. DISG), topics |
   | a YouTube channel URL in a field | `youtube` | channel topics, audience; `post_scraping` adds video transcripts |

   Reading posts or transcripts raises the price per contact; name it before building. The website
   source works with the company domain of business addresses.
3. **Fields.** The AI fills fields that have an AI description. Write it as an instruction: what to
   write, language, length, and "leave the field empty if the source does not say it; do not write a
   note that information is missing". For values the user relies on, use own fields rather than the
   standard Company and Website fields.
4. **Source field.** For LinkedIn and YouTube, a decision before the action: URL field `is not empty`
   and `contains` `linkedin.com/in/` or `youtube.com/`. Contacts without a URL get a tag.
5. **Overwrite.** `none` when the user maintains values by hand; `ai-only` when AI values may be
   refreshed later; `all` only on explicit request.
6. **Tags and result check.** Set the success and the error tag. Add a decision right after the
   action: the main target field `is empty` → tag "enrichment empty", so the user sees at a glance
   which contacts got no data.
7. **Pilot contact.** Activation stays with the user (`prepare-automation-activation` gives the
   dialog and the price per contact in euros). Then start **one** test contact, wait a few minutes,
   read its fields back with `get-contact` and report per field what arrived. A field holding only a
   statement that information is missing counts as empty.
8. **Then widen** the start condition or tag more contacts — with the price per contact times the
   number of contacts stated beforehand.

## Tell the user

- price per contact (from `prepare-automation-activation`);
- which fields will be filled and what a good result looks like (show the pilot values);
- how they check later: open a few contacts and read the fields, and watch the "enrichment empty" tag;
- AI reads public profiles and websites: the privacy notice should cover it.

## Abort

Stop and ask when the add-on is missing, when the balance does not cover the planned contacts, or
when the pilot contact comes back empty.
