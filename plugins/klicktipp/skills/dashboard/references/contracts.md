# Die veröffentlichten Verträge — Statistik

Wort für Wort das, was der Server in `tools/list` für die 7 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wie die Zahlen zu lesen und zu rechnen
sind, steht in [../SKILL.md](../SKILL.md). Die Auswertung eines Splittests,
`get-newsletter-split-test-statistics`, steht beim Skill `splittest`.

## Inhalt

`get-account-statistics` · `get-campaign-statistics` · `get-tag-statistics` ·
`get-automation-statistics` · `get-automation-waiting-contact-counts` ·
`get-automation-email-statistics` · `get-automation-sms-statistics`

## `get-account-statistics` · RI

**Read account statistics**

Reads account dashboard statistics: total contacts counted against the contact limit (including pending and unsubscribed), the current contact limit, recent campaigns, top tags, daily list activity, email-provider shares and bounces. The days setting affects only daily activity. Activity counts subscriptions, unsubscriptions, SMS subscriptions, imports, bounces and complaints, not sends, opens or clicks; use get-campaign-statistics for one mailing. SMS open metrics are null.

Parameter:

- `days` — integer (minimum 1; maximum 90; Default `30`): How many days of daily activity to return, 1 through 90; the other blocks are unaffected
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-campaign-statistics` · RI

**Read campaign statistics**

Reads lifetime statistics for an email or SMS newsletter or follow-up: sends, opens, clicks, conversions, bounces and tracked links. openRate is per send, clickRate per open, and clickRateOfRecipients per send; use these rates rather than dividing the counters. SMS has no opens or browser views; those fields and clickRate are null. Use clickRateOfRecipients for SMS. An unsent campaign has zero counts. Automations use get-automation-statistics.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the campaign whose statistics are read
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-tag-statistics` · RI

**Read tag statistics over time**

Reads tag counts over time for up to ten manual or automatic tags, grouped by hour, day, month or year. The only statistics tool scoped to a period; the others report lifetime totals. Counts only current holders, dated by their latest tagging; removed tags do not appear. Empty periods are omitted. This is not a tagging history; use get-contact-history for one contact. Requests exceeding 2000 periods are refused.

Parameter:

- `tagIds`* — array<integer> (minItems 1; maxItems 10): IDs of the tags to count, one to ten; from search-tags or get-tag
- `granularity` — string (einer von `hour`, `day`, `month`, `year`; Default `day`): Period each count covers: hour, day, month or year
- `from` — null | integer (minimum 0): Unix timestamp the period begins at; omit for the first tagging there is
- `to` — null | integer (minimum 0): Unix timestamp the period ends at; omit for now
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-statistics` · RI

**Read automation statistics**

Reads one automation's lifetime contact totals (started, finished, active, ended on an open, waiting for a queue job, failed, not restricted to a period) and, when the account has conversion statistics, how many finished or reached a goal between from and to and how many reached each goal action. A newsletter or autoresponder ID is refused; read those with get-campaign-statistics.

Parameter:

- `automationId`* — integer (minimum 1): ID of the automation; a newsletter or autoresponder ID is refused
- `from` — null | integer (minimum 0): Unix timestamp where the conversion period begins; omit for the beginning of the automation
- `to` — null | integer (minimum 0): Unix timestamp where the conversion period ends; omit for now
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-waiting-contact-counts` · RI

**Read waiting contact counts**

Reads how many contacts wait at each action of one automation right now, with the action ID, type and name, most contacts first; actions nobody waits at are omitted. The counts are an observation, not a completion receipt for a queued move. A newsletter or autoresponder ID is refused.

Parameter:

- `automationId`* — integer (minimum 1): ID of the automation; a newsletter or autoresponder ID is refused
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-email-statistics` · RI

**Read automation email statistics**

Reads the lifetime statistics of one campaign (automation) or notification email: sent, opened, clicked, bounces, spam complaints and tracked links, most-clicked first, as on its statistics screen (statisticsUrl). Counters total every use of the email, with no period filter; a campaign email nothing was sent of answers zeroes. A notification email records no sends, opens or link clicks: sent, opened and clicked are null and links is empty; only bounces and complaints are counted. The ID comes from get-automation-email or get-notification-email. Automation SMS use get-automation-sms-statistics, newsletters get-campaign-statistics.

Parameter:

- `emailId`* — integer (minimum 1): ID of the campaign or notification email whose statistics are read; this is not an automation action ID
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-sms-statistics` · RI

**Read automation SMS statistics**

Reads lifetime statistics for an automation SMS: sends, recipient clicks, bounces and tracked-link clicks across all uses. SMS has no open rate; clickRateOfRecipients is clicks per recipient. Unsent messages have zero counts. Use the SMS ID, not an automation action ID.

Parameter:

- `smsId`* — integer (minimum 1): ID of the automation SMS whose statistics are read; this is not an automation action ID
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
