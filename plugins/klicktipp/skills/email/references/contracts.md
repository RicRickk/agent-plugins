# Die veröffentlichten Verträge — E-Mail-Inhalt, Bausteine, Gestaltung, Bilder

Wort für Wort das, was der Server in `tools/list` für die 60 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-email-editor-placeholders` · `get-email-editor-rich-text-content` ·
`replace-email-editor-rich-text-content` · `replace-email-editor-content-from-html` ·
`publish-newsletter-email-content` · `replace-email-editor-content-from-email` ·
`replace-email-editor-content-from-document` · `update-email-editor-spacer-style` ·
`update-email-editor-divider-style` · `update-email-editor-button-style` ·
`update-email-editor-text-style` · `get-email-editor-content` · `preview-email-editor` ·
`validate-email-editor-content` · `move-email-editor-block` · `remove-email-editor-block` ·
`update-email-editor-block-style` · `add-email-editor-button` · `update-email-editor-button` ·
`update-email-editor-column-style` · `add-email-editor-divider` · `add-email-editor-heading` ·
`add-email-editor-html` · `add-email-editor-icons` · `update-email-editor-icons` ·
`add-email-editor-image-block` · `update-email-editor-image-block` · `add-email-editor-list` ·
`add-email-editor-menu` · `update-email-editor-menu` · `update-email-editor-page-style` ·
`add-email-editor-paragraph` · `add-email-editor-row` · `update-email-editor-row-style` ·
`add-email-editor-social-links` · `list-email-editor-social-icons` ·
`update-email-editor-social-links` · `add-email-editor-spacer` · `add-email-editor-table` ·
`update-email-editor-table` · `add-email-editor-text` · `update-email-editor-text` ·
`add-email-editor-video` · `update-email-editor-video` · `list-email-editor-images` ·
`search-email-editor-stock-images` · `list-email-editor-image-folders` ·
`create-email-editor-image-folder` · `delete-email-editor-image-folder` ·
`open-email-editor-image-upload` · `upload-email-editor-image-file` ·
`upload-email-editor-image-from-url` · `preview-email-editor-image` ·
`search-email-editor-templates` · `preview-email-editor-template` ·
`replace-email-editor-content-from-template` · `get-email-editor-display-condition-capabilities` ·
`update-email-editor-display-condition` · `configure-email-editor-row-display-condition` ·
`list-email-editor-display-conditions`

## `search-email-editor-placeholders` · RI

**Search email placeholders**

Searches placeholders and system links available to one email by editor URL, returning labels and groups. The set varies by email, so a confirmation email offers other placeholders than a newsletter. Account-owned redirects, countdowns, fields and vCards carry numeric IDs that cannot be guessed: look them up here rather than writing a generic placeholder. Query matches placeholder and label. Reads only.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as get-email-editor-content returned it, or the editUrl of a double opt-in confirmation email
- `query` — null | string (maxLength 250): Text the placeholder or its label has to contain; omit for all of them
- `limit` — null | integer (minimum 1; maximum 200): How many to return at most, 1 to 200; 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-email-editor-rich-text-content` · RI

**Get rich-text email content**

Reads a rich-text email’s complete HTML and plain body, content type, subject and contentRevision, by email ID or editor URL; use it when get-email-editor-content reports emailEditor rich-text. New newsletters should use the drag-and-drop editor, which the block, template and publish tools require. Sent and scheduled bodies and automation and notification emails are readable; editable and blockers describe write access. Drag-and-drop emails are refused. editorUrl is a tool identifier, not an app link; use get-newsletter for contentUrl.

Parameter:

- `emailId` — null | integer (minimum 1): ID of the email; omit when the editor URL is given
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL of the email, as get-email-editor-content returned it; omit when the email ID is given
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `replace-email-editor-rich-text-content` · DI

**Replace rich-text email content**

Replaces a rich-text email’s entire body (newsletter, automation or notification; by email ID or editor URL) without undo or a publish step; the stored body is what dispatch sends. Requires a subject and the current contentRevision from get-email-editor-rich-text-content. HTML is stored only as KlickTipp normalises it: no html, head, body or script, self-closed <br />, closed <p> and <li>; a refusal names the place and the fix. Plain text is retained only when the account maintains it, otherwise generated with a warning. Subject, sender and audience stay. Like the app, an email an active automation uses is written too. Drag-and-drop emails are refused.

Parameter:

- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the preceding get-email-editor-rich-text-content; a stale one refuses the write
- `html`* — string (maxLength 100000): Complete HTML body, at most what a read hands back; pass an empty string only with contentType "plain-only"
- `plain` — null | string (maxLength 100000): Complete plain-text body, kept only if the account maintains plain text itself (else generated from the HTML, with a warning); omit to have KlickTipp generate it
- `contentType` — null | string (einer von `html-and-plain`, `plain-only`): "html-and-plain" or "plain-only"; omit to keep what the email uses
- `emailId` — null | integer (minimum 1): ID of the email; omit when the editor URL is given
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL of the email, as get-email-editor-content returned it; omit when the email ID is given
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `replace-email-editor-content-from-html` · DO

**Import email content from HTML**

Converts HTML into a newsletter email’s drag-and-drop draft, replacing its entire body without undo. Requires the current content revision; existing content triggers a first-call refusal listing what would be lost. Add-ons, decisions and AI blocks may be lost in conversion. The body must carry the %User:Signature% placeholder or postal details and an unsubscribe link. Later changes use the block tools. Does not publish or send; publishing is publish-newsletter-email-content. For an existing editor document use replace-email-editor-content-from-document, for another email replace-email-editor-content-from-email.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, exactly as returned by get-email-editor-content
- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the read this HTML is based on; a stale one refuses the import
- `contentHtml`* — string (minLength 1; maxLength 10000000): The complete HTML body; replaces the stored document entirely
- `replaceExistingContent` — null | boolean: true to replace content the email already has; omit on the first attempt, so the answer lists what would be lost
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `publish-newsletter-email-content` · DO

**Publish email content**

Publishes a newsletter email’s stored drag-and-drop draft as dispatch content, replacing the previous published body without undo. Requires the current content revision. Only editable drafts are accepted; unsupported editor features are refused. Sending is separate: prepare-newsletter-dispatch.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, exactly as returned by get-email-editor-content
- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the state to publish, from the read or the last write; a stale one refuses
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `replace-email-editor-content-from-email` · D

**Copy email content**

Copies one email’s drag-and-drop body into another email draft in the same account, including layout and special blocks. Replaces the target body without undo; the source may already have been sent and stays unchanged. Requires the target’s current revision; existing content triggers a first-call refusal listing what would be lost. Use it to build a newsletter on an existing one. Does not publish; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email to write, exactly as returned by get-email-editor-content
- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the read of that email; a stale one refuses the copy
- `sourceEditorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email to copy from; it is only read and stays untouched
- `replaceExistingContent` — null | boolean: true to replace content the target already has; omit on the first attempt, so the answer lists what would be lost
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `replace-email-editor-content-from-document` · D

**Import email content from a document**

Replaces an email draft’s entire drag-and-drop body with an editor JSON document, without conversion or undo. Accepts the page or page-rooted form from get-email-editor-content. Requires the current revision; existing content triggers a first-call refusal listing what would be lost. HTML uses replace-email-editor-content-from-html, another email replace-email-editor-content-from-email. Does not publish; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, exactly as returned by get-email-editor-content
- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the read this document is based on; a stale one refuses the write
- `contentDocument`* — string (minLength 1; maxLength 10000000): The complete editor document as JSON; replaces the stored one entirely
- `replaceExistingContent` — null | boolean: true to replace content the email already has; omit on the first attempt, so the answer lists what would be lost
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-spacer-style` · I

**Write email spacer height**

Updates email spacer heights in pixels, including mobile height, on selected blocks. Omitted values stay. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `height` — null | integer (minimum 0; maximum 400): Height of the gap in pixels
- `mobileHeight` — null | integer (minimum 0; maximum 400): Height of the gap on a phone, in pixels
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-divider-style` · I

**Write email divider line**

Updates email divider line, colour and percentage width on selected blocks. A line thickness of 0 makes an invisible spacer; omitted values stay. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `line` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): The line as "1px solid #000000"
- `width` — null | integer (minimum 10; maximum 100): How far the line reaches across the row, as a whole percentage
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-button-style` · I

**Write email button look**

Updates email button appearance: colours, hover state, typography, borders, corners and inner padding. For words or link use update-email-editor-button; for outer spacing use update-email-editor-block-style. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the label, "#RRGGBB" or "transparent"
- `textColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour of the label
- `borderRadius` — null | integer (minimum 0; maximum 400): How round the corners are, in pixels; 0 is a rectangle
- `borderTop` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border above, as "2px solid #000000"
- `borderRight` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border right, same shape
- `borderBottom` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border below, same shape
- `borderLeft` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border left, same shape
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the label, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the label
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the label
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the label
- `fontFamily` — null | string (einer von `inherit`, `Arial`, `Courier`, `Georgia`, `Helvetica Neue`, `Lucida Sans`, `Tahoma`, `Times New Roman`, `Trebuchet MS`, `Verdana`, `ヒラギノ角ゴ Pro W3`, `メイリオ`): Font of the label by name, or "inherit" for the email's font
- `fontSize` — null | integer (minimum 8; maximum 120): Size of the label in pixels
- `fontWeight` — null | string (einer von `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900`): Weight of the label, "400" regular to "700" bold
- `lineHeight` — null | string (Muster `^[0-9]{2,3}%$`): Line height of the label as a percentage, "200%"
- `hoverBackgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the label under the pointer
- `hoverTextColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour of the label under the pointer
- `mobileFontSize` — null | integer (minimum 8; maximum 120): Size of the label on a phone, in pixels
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-text-style` · I

**Write email text look**

Updates typography of email headings, paragraphs, text and lists, including colours, fonts and spacing. Set line height here; inline line-height is ignored. Text blocks keep size and weight in their markup; paragraph spacing and list markers apply only to those kinds. Omitted styles stay. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the text blocks to write; the same values land on each
- `textColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour of the text
- `linkColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour of the links in it
- `fontFamily` — null | string (einer von `inherit`, `Arial`, `Courier`, `Georgia`, `Helvetica Neue`, `Lucida Sans`, `Tahoma`, `Times New Roman`, `Trebuchet MS`, `Verdana`, `ヒラギノ角ゴ Pro W3`, `メイリオ`): Font by name, or "inherit" for the email's font
- `fontSize` — null | integer (minimum 8; maximum 120): Size in pixels; heading, paragraph and list only
- `fontWeight` — null | string (einer von `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900`): Weight, "400" regular to "700" bold; heading, paragraph and list only
- `letterSpacing` — null | integer (minimum -10; maximum 30): Space between letters in pixels, negative tightens
- `lineHeight` — null | string (Muster `^[0-9]{2,3}%$`): Line height as a percentage, "150%"
- `paragraphSpacing` — null | integer (minimum 0; maximum 100): Space between paragraphs in pixels; paragraph only
- `listStyleType` — null | string (einer von `disc`, `circle`, `square`, `decimal`, `lower-alpha`, `upper-alpha`, `lower-roman`, `upper-roman`, `none`): Marker of each item; list only
- `listItemSpacing` — null | integer (minimum 0; maximum 100): Space between items in pixels; list only
- `mobileFontSize` — null | integer (minimum 8; maximum 120): Size on a phone in pixels; heading, paragraph and list only
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-email-editor-content` · RI

**Get email**

Reads an email’s editor body by email ID or editor URL, with optional document, content outline, style outline or published HTML. The outlines include revision and block UUIDs for edits. Document projections require a drag-and-drop email; every projection is readable in any state, and writeBlockers names what keeps a write from running.

Parameter:

- `emailId` — null | integer (minimum 1): ID of the email; omit when the editor URL is given
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL of the email, as a previous read returned it; omit when the email ID is given
- `include` — array<string> (maxItems 4): Projections to add: "content" (the editable document), "contentOutline" (uuid, kind and value of every writable field -- for a content change), "styleOutline" (what the style tools set -- for a style change), "publishedContent" (the HTML a dispatch would send); omit for identity only
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `preview-email-editor` · ROI

**Preview email**

Renders the current drag-and-drop email draft, unpublished edits included, and displays its HTML in an MCP App; recipient placeholders stay unresolved. Takes the editor URL from get-email-editor-content or a content write. Does not save, publish or send. The result carries contentHtml for hosts without MCP Apps support.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as a previous read returned it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `validate-email-editor-content` · RI

**Check email content**

Validates a stored drag-and-drop email body for empty text, incomplete blocks, missing footer placeholders and known text/link contrast issues (WCAG 4.5:1). Findings identify blocks and fixes. Does not check signatures, rendered CSS, spam, live links or sending readiness; publication may still warn or fail. Previous-editor emails are refused. Reads only.

Parameter:

- `emailId` — null | integer (minimum 1): ID of the email; omit when the editor URL is given
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL of the email, as a previous read returned it; omit when the email ID is given
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `move-email-editor-block`

**Move email block**

Moves an email block within its column or into another column, preserving its UUID, style and add-on configuration. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the block to move
- `position` — null | integer (minimum 0): Where it goes, counted from zero; omit to append
- `toColumnUuid` — null | string: The uuid of the column to move it into; omit to move inside its own column
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `remove-email-editor-block` · D

**Remove email block**

Removes an email block by UUID, permanently discarding its content and style. There is no undo through these tools. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the block to remove
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-block-style` · I

**Write email block style**

Updates email block padding, alignment, device visibility and image corners, including mobile overrides. Applies to all selected blocks; omitted styles stay. Text typography uses update-email-editor-text-style; image display width is separate. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the block, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the block, in pixels
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the block, in pixels
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the block, in pixels
- `textAlign` — null | string (einer von `left`, `center`, `right`, `justify`): How its content sits: "left", "center", "right", or "justify" where the block is text
- `hideOnMobile` — null | boolean: Whether the block is hidden on a phone
- `hideOnDesktop` — null | boolean: Whether the block is hidden on a desktop
- `borderRadius` — null | integer (minimum 0; maximum 400): How round the corners of an image are, in pixels; image only
- `mobilePaddingTop` — null | integer (minimum 0; maximum 400): Space above the block on a phone, in pixels
- `mobilePaddingRight` — null | integer (minimum 0; maximum 400): Space right of the block on a phone
- `mobilePaddingBottom` — null | integer (minimum 0; maximum 400): Space below the block on a phone
- `mobilePaddingLeft` — null | integer (minimum 0; maximum 400): Space left of the block on a phone
- `mobileTextAlign` — null | string (einer von `left`, `center`, `right`, `justify`): How its content sits on a phone
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-button`

**Add email button**

Adds a button block with its label (markup) and link to an email column. Copies the nearest button’s style, not its label or inline markup, and returns the new UUID. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `label` — null | string (maxLength 2000): The visible text of the button, as markup
- `href` — null | string (maxLength 2000): Where the button leads
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-button` · I

**Write email button**

Updates an email button’s markup label and link. Preserve the read label’s formatting markup when changing its words, or its typography is lost. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the button block
- `label` — null | string: The visible text of the button, as markup
- `href` — null | string: The link target of the button
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-column-style` · I

**Write email column style**

Updates email column backgrounds, padding and borders, applying the same named values to every selected column. Omitted styles stay. Column widths cannot be changed here; uneven splits require the editor. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the columns to write; the same values land on each
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the column, "#RRGGBB" or "transparent"
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the content of the column, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the content of the column, in pixels
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the content of the column, in pixels
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the content of the column, in pixels
- `borderTop` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border above the column, as "1px solid #000000"
- `borderRight` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border right of the column, same shape
- `borderBottom` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border below the column, same shape
- `borderLeft` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border left of the column, same shape
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-divider`

**Add email divider**

Adds an email divider to a column and returns its UUID. Line and spacing are configured with update-email-editor-divider-style and update-email-editor-block-style. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-heading`

**Add email heading**

Adds a heading block to an email column with text and level (h1, h2 or h3). Copies the nearest heading’s style, not its inline markup; supply that with the text. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `text` — null | string (maxLength 100000): The words of the heading, as markup
- `level` — null | string (einer von `h1`, `h2`, `h3`): The heading level: "h1", "h2" or "h3"; omit for h1
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-html`

**Add email custom HTML**

Adds a custom HTML block to an email column, copying the nearest HTML block’s style but not its markup. Returns the new UUID. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The markup of the block
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-icons`

**Add email icons**

Adds an icon block with its pictures, captions and links to an email column. Required icon size and caption position come from an existing icon block. Returns the new UUID. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the picture, from list-email-editor-images or open-email-editor-image-upload.
  - `href` — string: Where it leads.
  - `text` — string: The words beside the icon.
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-icons` · I

**Write email icons**

Replaces every picture, caption and link in an email icon block, in order. Include all icons to retain; size and caption position are kept. Social links are a separate block. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the icon block
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the picture, from list-email-editor-images or open-email-editor-image-upload.
  - `href` — string: Where it leads.
  - `text` — string: The words beside the icon.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-image-block`

**Add email image**

Adds an image block with source, alt text and link to an email column. Copies the nearest image block’s style, not its content, and returns the new UUID. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `src` — null | string (maxLength 2000): URL of the image, from list-email-editor-images or open-email-editor-image-upload
- `alt` — null | string (maxLength 1000): Alternative text of the image
- `href` — null | string (maxLength 2000): Link target of the image
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-image-block` · I

**Write email image**

Updates email image blocks by UUID: account-library source, alternative text and link. Use an image URL from list-email-editor-images or an upload. Avoid external stock/provider URLs: recipients’ mail clients would load them from a third party. Display width stays unchanged. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `images`* — array<object> (minItems 1; maxItems 60): The image blocks to write, each by uuid; a field left out keeps its value, an empty href removes the link
  - `uuid`* — string: The uuid of the image block.
  - `src` — string: URL of the image, from list-email-editor-images or open-email-editor-image-upload.
  - `alt` — string: Alternative text of the image.
  - `href` — string: Link target; an empty string removes the link.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-list`

**Add email list**

Adds a list block with complete ul or ol markup to an email column. Copies the nearest list’s style or the email’s default text and link colours (set first with update-email-editor-page-style). Inline markup is not copied; supply it in html. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The list, as complete <ul> or <ol> markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-menu`

**Add email menu**

Adds a menu block with ordered entries to an email column. Copies link behavior, separators and spacing from an existing menu; returns the new UUID. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `items`* — array<object> (minItems 1; maxItems 30): The menu entries, left to right
  - `text`* — string: The words of the entry.
  - `href` — string: Where it leads.
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-menu` · I

**Write email menu**

Replaces all entries of an email menu block with ordered text and links. Include every entry to retain; link behavior, separators, spacing and typography stay. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the menu block
- `items`* — array<object> (minItems 1; maxItems 30): The menu entries, left to right
  - `text`* — string: The words of the entry.
  - `href` — string: Where it leads.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-page-style` · I

**Write email page style**

Updates an email’s page background (the colour around the message), default text and link colours, font, width and alignment. The colour behind the content uses update-email-editor-row-style. Text and link colours are copied into blocks when they are added, so set them before adding blocks. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour around the message, "#RRGGBB" or "transparent"
- `textColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Default text colour of the whole email
- `linkColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Default colour of every link of the email
- `contentWidth` — null | integer (minimum 320; maximum 1440): Width of the message in pixels
- `fontFamily` — null | string (einer von `Arial`, `Courier`, `Georgia`, `Helvetica Neue`, `Lucida Sans`, `Tahoma`, `Times New Roman`, `Trebuchet MS`, `Verdana`, `ヒラギノ角ゴ Pro W3`, `メイリオ`): Default font of the whole email, by name; see the schema for the names
- `contentAlign` — null | string (einer von `left`, `center`, `right`): Where the message sits when the window is wider than it is
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-paragraph`

**Add email paragraph**

Adds a paragraph block with HTML to an email column. Copies the nearest paragraph’s style or the email’s default text and link colours (set first with update-email-editor-page-style). Inline markup is not copied; supply it in html. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The words of the paragraph, as markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-row`

**Add email row**

Adds an email row of equally wide empty columns; this is the first write to an empty draft. Copies an existing row’s background and width. Returns column UUIDs and revision needed to add blocks. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columns` — null | integer (minimum 1; maximum 6): How many equally wide columns the row gets; 1, 2, 3, 4 or 6, one by default
- `position` — null | integer (minimum 0): Where the row goes among the rows, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-row-style` · I

**Write email row style**

Updates email row backgrounds, width, padding, borders and mobile column layout. A frame around the whole row belongs here, not on each column. Omitted styles stay. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the rows to write; the same values land on each
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the whole row, "#RRGGBB" or "transparent"
- `contentBackgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the content area inside the row
- `textColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Default text colour of the row
- `contentWidth` — null | integer (minimum 320; maximum 1440): Width of the content area in pixels
- `verticalAlign` — null | string (einer von `top`, `middle`, `bottom`): How the columns line up: "top", "middle" or "bottom"
- `stackOnMobile` — null | boolean: Whether the columns stack under each other on a phone
- `hideOnMobile` — null | boolean: Whether the row is hidden on a phone
- `hideOnDesktop` — null | boolean: Whether the row is hidden on a desktop
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the content of the row, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the content of the row, in pixels
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the content of the row, in pixels
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the content of the row, in pixels
- `borderTop` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border above the row, as "1px solid #000000"
- `borderRight` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border right of the row, same shape
- `borderBottom` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border below the row, same shape
- `borderLeft` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border left of the row, same shape
- `borderRadius` — null | integer (minimum 0; maximum 400): How round the corners of the content area are, in pixels
- `columnsSpacing` — null | integer (minimum 0; maximum 100): Gap between the columns, in pixels
- `columnsBorderRadius` — null | integer (minimum 0; maximum 400): How round the corners of each column are, in pixels
- `reverseStackOnMobile` — null | boolean: Whether stacked columns come in reverse order on a phone
- `mobilePaddingTop` — null | integer (minimum 0; maximum 400): Space above the content on a phone, in pixels
- `mobilePaddingRight` — null | integer (minimum 0; maximum 400): Space right of the content on a phone
- `mobilePaddingBottom` — null | integer (minimum 0; maximum 400): Space below the content on a phone
- `mobilePaddingLeft` — null | integer (minimum 0; maximum 400): Space left of the content on a phone
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-social-links`

**Add email social links**

Adds a social-links block with icons to an email column. Use icon URLs from list-email-editor-social-icons or the account’s image library; invented URLs will not render. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the icon picture. Take one from list-email-editor-social-icons, or any URL from the account's own image library -- an uploaded picture is a usable icon. Never invent one: an icon URL that resolves to nothing is a hole in the row, in every recipient's mail program.
  - `href`* — string: Where the icon leads.
  - `name` — string: The network, e.g. "facebook".
  - `alt` — string: Alternative text: what a reader gets instead of the picture when it does not load, and what a screen reader says.
  - `title` — string: Tooltip of the icon, shown on hover. Not a replacement for alt: a reader who never sees the picture never sees this either.
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `list-email-editor-social-icons` · RI

**Search email social icons**

Lists social icon images already used by an email, with network, alt text and tooltip, most used first. Reuse these URLs for social blocks; invented editor-icon URLs render as missing images. Account-library images from list-email-editor-images also work. An empty result means this email has no existing icon to reuse.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as a read returned it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-social-links` · I

**Write email social links**

Replaces all icons in an email social-links block, in order, including pictures and targets; each icon’s type (follow, share) and link behaviour are kept. Use icon URLs from list-email-editor-social-icons or the account’s image library. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the social block
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the icon picture. Take one from list-email-editor-social-icons, or any URL from the account's own image library -- an uploaded picture is a usable icon. Never invent one: an icon URL that resolves to nothing is a hole in the row, in every recipient's mail program.
  - `href`* — string: Where the icon leads.
  - `name` — string: The network, e.g. "facebook".
  - `alt` — string: Alternative text: what a reader gets instead of the picture when it does not load, and what a screen reader says.
  - `title` — string: Tooltip of the icon, shown on hover. Not a replacement for alt: a reader who never sees the picture never sees this either.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-spacer`

**Add email spacer**

Adds an email spacer to a column and returns its UUID. Set its height with update-email-editor-spacer-style. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-table`

**Add email table**

Adds a table block with markup rows to an email column. Every row needs the same cell count. Copies the nearest table’s style, or uses the email’s default text and link colours; inline cell markup is not copied. Returns the new UUID. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `rows`* — array<array> (minItems 1; maxItems 60): The rows, each a list of cells as markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-table` · I

**Write email table**

Replaces an email table’s body rows with markup cells. Every row and header must have the same cell count. Omit headers to keep them, or pass [] to remove them; borders and typography stay. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the table block
- `rows`* — array<array> (minItems 1; maxItems 60): Body rows, each a list of cell contents as markup, without enclosing td or th elements
- `headers` — null | array<string> (maxItems 12): Header cell contents; omit to keep the header, or use an empty list to remove it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-text`

**Add email text**

Adds a text block with HTML to an email column. Copies the nearest text block’s style, or the email’s default text and link colours (set first with update-email-editor-page-style). Inline markup is not copied; supply it in html. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The words of the block, as markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-text` · I

**Write email text**

Updates markup in heading, text, paragraph, list or custom HTML blocks by UUID. Preserve the read markup’s wrappers and attributes to retain inline formatting. Block typography uses update-email-editor-text-style. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `blocks`* — array<object> (minItems 1; maxItems 100): The blocks to write, each by uuid and its complete markup; a heading may add its level
  - `uuid`* — string: The uuid of the text block to write.
  - `html`* — string: Its complete markup, the read markup with the words replaced.
  - `level` — string (einer von `h1`, `h2`, `h3`): The heading level, for a heading block only. Refused on any other kind, which has none.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-email-editor-video`

**Add email video**

Adds a video block with URL and preview image to an email column. Copies the nearest video block’s style, not its content, and returns the new UUID. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `src` — null | string (maxLength 2000): URL of the video, which is where the click leads
- `thumbSrc` — null | string (maxLength 2000): URL of the preview image, which is what the recipient sees
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-video` · I

**Write email video**

Updates an email video block’s URL and preview image. Recipients see a linked preview with a play icon, not an inline video; without a preview image the block is empty. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the video block
- `src` — null | string (maxLength 2000): The video URL, for example a YouTube or Vimeo page
- `thumbSrc` — null | string (maxLength 2000): The preview image the block shows instead of the video
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `list-email-editor-images` · RI

**Search images**

Lists an account’s email-editor image library by path, paginated by cursor. Returns public URLs suitable for image blocks, file names, types and upload times. Has no text filter. New pictures come from open-email-editor-image-upload (local file) or upload-email-editor-image-from-url (public URL).

Parameter:

- `limit` — null | integer (minimum 1; maximum 100): Images per page, 1 to 100; default 20
- `cursor` — null | string (maxLength 1000): nextCursor of the previous page; omit for the first page
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `search-email-editor-stock-images` · ROI

**Search stock images**

Searches stock photos for the email editor and returns candidate previews, licences and sizes. A search without a match may return unrelated photos. Stock URLs are not ready for email blocks; upload the chosen photo with upload-email-editor-image-from-url. Check licence restrictions for identifiable people.

Parameter:

- `query`* — string (minLength 1; maxLength 100): What the picture shows, one or two words, in English (the archives are indexed in English)
- `limit` — null | integer (minimum 1; maximum 12): How many candidates, 1 to 12; default 3
- `orientation` — null | string (einer von `landscape`, `portrait`, `square`): Only photos of this shape: landscape, portrait or square; omit for any shape
- `minWidth` — null | integer (minimum 1; maximum 10000): Only photos at least this wide, in pixels; 1200 for a full-width image
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `list-email-editor-image-folders` · RI

**List image folders**

Lists paths of folders in an account’s email-editor image library. These paths can be used as the folder for image uploads; omitting folder uploads to the root. Does not list images.

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-email-editor-image-folder`

**Create image folder**

Creates an email-editor image-library folder, including parent folders in a path. Names are sanitized and changed reports the stored name; an existing folder is refused. Does not move or change images.

Parameter:

- `path`* — string (minLength 1; maxLength 250): Name of the new folder, or a path for one inside another ("Kampagnen/Herbst"); letters, digits, dots, dashes and underscores survive, everything else becomes a dash
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-email-editor-image-folder` · DI

**Remove empty image folder**

Deletes an empty email-editor image-library folder. Refuses folders containing images or subfolders; no image is deleted, because sent newsletters keep loading them. The user empties a folder in the KlickTipp file manager.

Parameter:

- `path`* — string (minLength 1; maxLength 250): Path of the folder to remove, as list-email-editor-image-folders lists it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `open-email-editor-image-upload` · I

**Upload image**

Opens an MCP App file picker for uploading a local image into the email-editor library. The user chooses the file; this call itself stores nothing. Public image URLs use upload-email-editor-image-from-url instead.

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `upload-email-editor-image-file`

**Store picked image file**

Stores a user-picked JPEG, PNG, GIF or WebP file in the email-editor image library and returns its public URL. Only for the MCP App upload form of open-email-editor-image-upload; maximum 5 MB and no overwrite.

Parameter:

- `fileName`* — string (minLength 1; maxLength 250): Name of the picked file, as the browser reports it; sanitised, extension set from the bytes, a taken name is numbered, never overwritten -- see storedAs
- `contentBase64`* — string (minLength 1; maxLength 6990508): The file's bytes as plain base64, no data: prefix
- `folder` — null | string (maxLength 250): Folder of the library to store it in, as list-email-editor-image-folders lists it; omit for the library's root
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `upload-email-editor-image-from-url` · O

**Add image from URL**

Uploads a public image URL into the email-editor library and returns a URL ready for an email image block. The source must be publicly reachable, not private or login-protected. Accepts JPEG, PNG, GIF or WebP up to 5 MB; never overwrites.

Parameter:

- `fileName`* — string (minLength 1; maxLength 250): Name for the file, extension optional; sanitised, extension set from the bytes, a taken name is numbered, never overwritten -- see storedAs
- `sourceUrl`* — string (minLength 12; maxLength 2000): Public http(s) URL the server fetches the image from; reachable from the internet, no login, no private host
- `folder` — null | string (maxLength 250): Folder of the library to store it in, as list-email-editor-image-folders lists it; omit for the library's root
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `preview-email-editor-image` · RI

**Preview image**

Previews an image URL in an MCP App window without changing an email. Accepts URLs from the account image library or stock archives; images hosted elsewhere are refused. For an external picture, upload-email-editor-image-from-url copies it into the library first. Requires MCP Apps support to display the image.

Parameter:

- `url`* — string (minLength 12; maxLength 2000): https URL of the image, as a previous image tool returned it

## `search-email-editor-templates` · ROI

**Search email templates**

Searches the email editor design catalogue by tag, category or collection. Returns template IDs, names and thumbnails, paginated with nextPage (12 per page by default). Use the ID, not the result number, to apply or preview a design. Tags are case-sensitive; unknown filters match nothing. Changes no email.

Parameter:

- `tag` — null | string (maxLength 250): Case-sensitive catalogue tag; use the exact spelling from the widget suggestions, e.g. "light", "white", "three-columns"; omit for all
- `category` — null | string (maxLength 250): Narrow by one category as this tool reports them, e.g. "events", "saas"; omit for all
- `collection` — null | string (maxLength 250): Narrow by one collection as this tool reports them, e.g. "welcome-series"; omit for all
- `page` — null | integer (minimum 1): Which page of the catalogue, from 1; default 1
- `pageSize` — null | integer (minimum 1; maximum 35): How many designs per page, 1-35; default 12
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `preview-email-editor-template` · ROI

**Preview email template**

Previews a full catalogue email design, rather than its thumbnail, in an MCP App. Use the template ID from search-email-editor-templates, not its result number. Returns contentHtml when MCP Apps are unavailable. Changes no email and sends nothing.

Parameter:

- `templateId`* — string (minLength 1; maxLength 250): id of the design, as search-email-editor-templates returned it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `replace-email-editor-content-from-template` · DO

**Apply design to email**

Replaces an email draft's entire body with a catalogue design, without undo or publication. Works for newsletter, automation and notification emails. Use the template ID from search-email-editor-templates, not its result number, and the current contentRevision. If the draft has content, the first call lists what would be lost; replaceExistingContent then permits the replacement. Publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email to write, exactly as get-email-editor-content returned it
- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the read of that email; a stale one refuses the write
- `templateId`* — string (minLength 1; maxLength 250): id of the design, as search-email-editor-templates returned it
- `replaceExistingContent` — null | boolean: true to replace content the email already has; omit on the first attempt, so the answer lists what would be lost
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-email-editor-display-condition-capabilities` · RI

**Read display condition capabilities**

Lists available email display-condition types. With conditionTypes, also returns their comparisons, account entities, actions and timeframes for update-email-editor-display-condition. Entities are capped at 200 per type; entityCount reports the full count. Reads only.

Parameter:

- `conditionTypes` — array<string> (maxItems 5): Kinds to read the field values of, as conditionType of the catalogue; omit for the catalogue alone
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-email-editor-display-condition` · D

**Write display condition**

Creates or replaces a named email display condition and returns its decisionId. Choices come from get-email-editor-display-condition-capabilities; foreign entities are refused. Replacing a decisionId overwrites its segments and changes who sees bound rows in the draft, without undo. Bind a row with configure-email-editor-row-display-condition; this write alone shows nothing. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as a read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `name`* — string (minLength 1; maxLength 250): What the editor shows for this condition; a person reads it
- `segments`* — array<object> (minItems 1; maxItems 10): Each {conditions: [{conditionType, condition, entity, action, timeframe}], conditionsOpAND}; a contact matches a segment when its conditions match
  - `conditionsOpAND` — boolean
  - `conditions`* — array<object> (maxItems 20)
    - `conditionType`* — string (minLength 1; maxLength 250)
    - `condition`* — string (minLength 1; maxLength 100)
    - `entity` — integer (minimum 1)
    - `action` — string (maxLength 100)
    - `timeframe` — string (maxLength 100)
- `segmentsOpAND` — null | boolean: true when every segment has to match, false when one is enough; defaults to true
- `decisionId` — null | string (maxLength 50): decisionId of an existing condition to replace whole; omit to create one
- `description` — null | string (maxLength 1000): A note for the person editing this email later
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `configure-email-editor-row-display-condition` · DI

**Bind row to display condition**

Binds an email row to an existing display condition, or clears its binding with null so everyone sees it. Nonmatching contacts cannot see a bound row; a condition matching nobody hides it entirely. The previous binding is lost; list-email-editor-display-conditions shows current bindings. Revision-bound, atomic edit; drafts only; publishing is publish-newsletter-email-content.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as a read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `rowUuid`* — string (minLength 1; maxLength 100): The uuid of the row, as get-email-editor-content answers it under contentOutline
- `decisionId` — null | string (maxLength 50): The condition this row follows; null frees the row, so it is shown to everybody
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `list-email-editor-display-conditions` · RI

**Read display conditions**

Lists an email’s display conditions, segments and bound row UUIDs with the contentRevision needed for writes. Row bindings appear only here; unbound conditions govern nothing and may be dropped on the next editor save. Reads only.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as a read returned it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
