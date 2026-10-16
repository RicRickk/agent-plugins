## Picking a template — show it, never describe it

**A template is a layout. Its name does not describe it**, and neither can you. "Modern, friendly,
with a large hero image" is a sentence about a design the user cannot see, and picking from it is
picking blind. So never answer a template request with prose.

1. **`search-email-editor-templates`** — the catalogue the editor's template browser shows. A host
   that renders MCP Apps **shows the designs as pictures**. Without such a host the grid is only a
   list of names — never describe them, go on to step 2 and show the designs yourself.

   **The first search is a probe, not the answer.** The catalogue is large (`category: "events"`
   alone returns around 300), so a first page is a sample, and paging through it is the wrong move.
   Read the `tags`, `categories` and `collections` the answer carries back and search again with the
   one that matches the intent — every value the tool **answered with** is one it accepts back, and
   an unknown value matches nothing rather than being refused.

   **Categories carry the occasion, tags carry the purpose.** `events` is full of dated and
   regional occasions — Halloween, Valentine's Day, Father's Day, Juneteenth, the Super Bowl — so a
   generic intent drowns in them. What a request like "a community event" actually means sits in the
   tags: `Community`, `RSVP`, `Invitation`, `Ticketing`, `Countdown`. Reach for `tag` when the user
   named a *purpose*, for `category` when they named an *occasion*.

   Keep the search proportional to the request. For a short internal test mail, try one broad probe
   and one or two focused searches using returned filters. Inspect promising thumbnails before
   opening full previews. Stop when up to three genuinely fitting designs are found, or explain
   that none fits instead of paging through the catalogue. A transient search error may be retried
   once; if later searches succeed, do not present the catalogue as unavailable.
2. **`preview-email-editor-template`** — **this is the deliverable, not the search result.** A
   search answer is a wall of thumbnails; a preview is the design at full height, the way the
   recipient will meet it. Never end a template request at the grid, and never end it at a
   paragraph about the grid: pick the two or three that fit and render each one. Judge fit from
   the full design, not its name or category. Compare the user's required sections and copy length
   with what is visible, including demo wording embedded in images. A design needing many removed
   rows, unrelated imagery or a replacement for an image with visible "Change image" is a poor
   match for a short message. Search for a simpler design; if none is available, say so instead
   of recommending extensive demolition as the best fit.

   Count logos, demo links, buttons and sections that would need changing. A template with multiple
   unrelated sections is not a text-only swap for a two-paragraph test mail. The empty design can
   be a clean starting point, but explain the work needed to add its content. Demo unsubscribe
   links do not satisfy the real footer requirement; when preparing actual content, follow the
   email skill's supported `%Link:Unsubscribe%` **or** `%User:Signature%` path.

   It takes the `id` that reads like `monthly-marketing-dispatch`; the number from the search
   answer is for pointing and is refused here by name. It renders the design itself, not the
   catalogue thumbnail, so what is approved here is what gets written. Reads only — no email is
   touched.

   **When no picture appears, showing it is still your job.** A host without MCP Apps (Claude
   Code, Codex) receives only `contentHtml` — the rendered design as a complete HTML page. That is
   not a dead end and not a reason to fall back to names:

   | Environment | Way |
   | --- | --- |
   | Claude Code | one page, published with the `Artifact` tool |
   | claude.ai | one artifact directly in the reply |
   | without artifacts (e.g. Codex) | write the `.html`, open it if a browser is at hand, name the path |

   - **One page for all candidates.** Each unmodified `contentHtml` goes into its own
     `<iframe srcdoc="…">` (escape for the enclosing attribute without changing the HTML value),
     full height, beside its name, its `id` and the sentence why it made the shortlist. The frame
     keeps each design's CSS to itself. Name the page as a gallery of original tool previews; if the
     wrapper changes how they render, give the original HTML separately.
   - **Do not pull `contentHtml` into the conversation.** It is 30–70 KB per design, and one alone
     can exceed what a tool answer may carry — the host then saves the answer to a file. Take it
     from there with `jq -r .contentHtml <file>` straight into the page.
   - The search answer's `previewUrl` is the catalogue picture, not the design. Use it only when
     `contentHtml` is missing, and say that it is the thumbnail.
3. **`replace-email-editor-content-from-template`** — writes it into the email, addressed by
   `editorUrl` and bound to the `contentRevision`. Full replacement without undo; over existing
   content the first call is refused with a list of what would be lost. It does not publish.
4. **`preview-email-editor`** — show the result. A newsletter built from a template is finished when
   the user has *seen* it, not when you have reported which blocks it has.

For a newsletter that is: `create-newsletter-draft`, then the template into it. The same tool works
for an automation email and a notification email — any email the editor opens.

**Show only candidates that actually fit, up to three, and give each its own preview.** Say in a
sentence why each made the shortlist and what visible sections would still need replacement. That
sentence is context for a picture, not a substitute for one. If the inspected designs do not fit,
say that plainly and continue a focused search when permitted. Choosing is the one decision in this
skill that is not yours: the design is what their audience sees.
