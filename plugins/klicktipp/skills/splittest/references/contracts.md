# Die veröffentlichten Verträge — Splittests

Wort für Wort das, was der Server in `tools/list` für die 6 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## `get-newsletter-split-test` · RI

**Read split test**

Reads an email newsletter split test: audience share, duration, winner criterion, start state and variants with their email IDs, subjects and editor URLs. Identify it by campaignId or one variant emailId, not both. A fresh test has one variant; needsMoreVariants indicates whether it can be sent. A non-split-test campaign is refused.

Parameter:

- `campaignId` — null | integer (minimum 1): ID of the split test campaign -- the newsletterId of get-newsletter; pass this or emailId, not both
- `emailId` — null | integer (minimum 1): Email ID of one variant, as splitTestVariants or an editor URL carries it; the answer is the whole test that variant belongs to. Either this or campaignId, never both
- `accountId` — null | integer (minimum 1): User ID of the account the campaign belongs to; omit for the account the access token belongs to, or pass the user ID of a subaccount the token owner may act for

## `get-newsletter-split-test-statistics` · RI

**Read split test results**

Reads an email newsletter split test's results by variant: opens, clicks, conversions, revenue and the reported winner. While the test is running, isDecided is false and winnerLabel is null; a leading variant is not yet the winner. For the whole campaign's totals use get-campaign-statistics. Non-split-test campaigns are refused.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the split-test newsletter, as get-newsletter reports it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `add-newsletter-split-test-variant`

**Add split test variant**

Adds an email newsletter split-test variant, empty or copied from copyFromEmailId. Returns all variants and their editor URLs; audience shares are redistributed evenly. A test needs at least two variants to send. Refused after the test starts; sends nothing.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign (a newsletter ID)
- `copyFromEmailId` — null | integer (minimum 1): Email ID of the variant to copy, from splitTestVariants; omit for an empty variant
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `remove-newsletter-split-test-variant` · D

**Remove split test variant**

Removes an email newsletter split-test variant and deletes its email and content permanently. Returns the remaining variants with evenly redistributed shares. The last variant cannot be removed; a started test refuses the change. Sends nothing.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign the variant belongs to
- `emailId`* — integer (minimum 1): Email ID of the variant to remove, as get-newsletter returns it in splitTestVariants
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-newsletter-split-test-variant` · I

**Write split test variant**

Updates one email newsletter split-test variant's internal name, subject or preheader by emailId. This is where a variant's subject is set; its body uses the email editor. Omitted values stay unchanged. Changing subject or preheader invalidates earlier contentRevision values. Refused after the test starts; sends nothing.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign the variant belongs to
- `emailId`* — integer (minimum 1): Email ID of the variant to write, as get-newsletter returns it in splitTestVariants
- `name` — null | string (maxLength 250): New internal name of this variant, never sent to a recipient; omit to keep the current one
- `subject` — null | string (maxLength 998): New subject line of this variant, without HTML; ask the user, never invent one. Invalidates the variant's contentRevision
- `preheader` — null | string (maxLength 120): New inbox preview line of this variant, at most 120 characters, without HTML; empty string removes it, omit keeps it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `configure-newsletter-split-test` · I

**Configure split test**

Configures an email newsletter split test's audience share, measuring period and winner criterion. Omitted settings stay unchanged. Conversions and revenue require the conversion pixel; opens and clicks do not. Refused after the test starts; sends nothing.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign whose settings to write
- `testSizePercent` — null | integer (minimum 2; maximum 98): Share of the audience the variants go to, 2 to 98; omit to keep
- `testDurationHours` — null | integer (minimum 1; maximum 27777): Measuring period before the winner goes to the rest, 1 to 27777 hours; omit to keep
- `winnerBy` — null | string (einer von `opens`, `clicks`, `conversions`, `revenue`): "opens" (open rate), "clicks" (unique clicks), "conversions" or "revenue" (both need the conversion pixel); omit to keep
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
