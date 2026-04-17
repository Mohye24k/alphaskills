---
name: vehicle-recall-check
description: Checks US vehicle recalls from the official NHTSA database for any make, model, and model year. Returns recall campaign numbers, affected components, defect summaries, consequences, remedies, and over-the-air-fix flags. Use when the user asks about vehicle recalls, wants to check a specific car for defects, investigates class-action opportunities for a manufacturer, researches used-car inventory, or asks "any recalls on my Tesla / Honda / Ford". Covers recalls dating back decades for every US-sold vehicle. Uses the free official NHTSA public API (api.nhtsa.gov) with no key required. Replaces Carfax VIN reports ($40 each), AutoCheck, and NHTSA enterprise data services ($500-5,000/year).
---

# NHTSA Vehicle Recall Checker

## When to invoke

Trigger on any vehicle recall / auto-defect question:

- "Any recalls on 2023 Tesla Model 3?"
- "Ford F-150 2022 recalls"
- "Class-action lawsuit opportunities for Honda?"
- "Has my car been recalled?"
- "Tesla Autopilot recalls"
- "Toyota airbag recalls"

## Required input

- **Make** (manufacturer) — e.g. `Tesla`, `Ford`, `Honda`, `Toyota`
- **Model** — e.g. `Model 3`, `F-150`, `Civic`, `Camry`
- **Model year** — e.g. `2023`

## Optional filters

- **Component substring** — filter to recalls about airbags, brakes, engine, electrical, etc. (e.g. `"AIR BAG"`)
- **Since date** — only return recalls filed on or after this date (e.g. `"2024-01-01"`)

## Output format

### 1. Summary
`"{Year} {Make} {Model}: {N} total recalls found. {M} filed in last 12 months. Most common components: [list]."`

### 2. Recalls table

| Campaign # | Date Filed | Component | Severity | Remedy Type |
|------------|-----------|-----------|----------|-------------|

Severity flags:
- 🚨 `PARK_IT` — don't drive at all (extreme defect)
- ⚠️ `PARK_OUTSIDE` — fire risk, park outdoors only
- 🔧 Normal — scheduled service fix
- 📡 `OTA` — over-the-air software fix (Tesla-style)

### 3. Detailed breakdown per recall

For each recall, show:
- **Component**: e.g. `EXTERIOR LIGHTING:TAIL LIGHTS`
- **Defect summary**: the full text description
- **Consequence**: what happens (crash risk, injury, etc.)
- **Remedy**: how it's fixed
- **Link**: NHTSA recall page

## Data source + procedure

Query the NHTSA API:

```
GET https://api.nhtsa.gov/recalls/recallsByVehicle?make={Make}&model={Model}&modelYear={Year}
```

Returns a JSON object with:

- `Count` — total recalls returned
- `Message` — "Results returned successfully"
- `results[]` — array of recalls

Each recall row contains:

- `Manufacturer` — e.g. `"Tesla, Inc."`
- `NHTSACampaignNumber` — unique ID (e.g. `"22V844000"`)
- `parkIt` (boolean) — extreme defect, stop driving
- `parkOutSide` (boolean) — fire risk (note the typo in NHTSA's field name)
- `overTheAirUpdate` (boolean) — OTA software fix available
- `ReportReceivedDate` — **date in DD/MM/YYYY format** (yes, despite being a US agency)
- `Component` — affected subsystem (e.g. `"STEERING:AUTOMATED/ADAPTIVE STEERING"`)
- `Summary` — full defect description
- `Consequence` — what could happen
- `Remedy` — how it's fixed
- `Notes` — additional info
- `NHTSAActionNumber` — when there's a separate enforcement action

### Important date parsing

NHTSA returns `ReportReceivedDate` as `DD/MM/YYYY` (day first, month second). Parse carefully:

```js
const [day, month, year] = reportDate.split('/');
const iso = new Date(`${year}-${month.padStart(2,'0')}-${day.padStart(2,'0')}T00:00:00Z`);
```

### No component or date filter is supported server-side

NHTSA's API doesn't support component/date filters. Pull all recalls for the make/model/year and filter client-side.

## Example invocation

User: "Any recalls on 2023 Tesla Model 3?"

The skill should:
1. Query with `make=Tesla&model=Model 3&modelYear=2023`
2. Parse all recalls
3. Return:
   ```
   2023 Tesla Model 3: 10 total recalls.
   Most common components: airbags (2), software (3), electrical (3), lighting (1), steering (1).

   Notable recalls:
   🚨 23V085000 (2023-02-15) — FSD Beta unsafe at intersections. OTA fix.
   ⚠️ 23V434000 (2023-06-19) — Pyrotechnic battery disconnect defect. Physical service.
   🔧 21V834000 (2021-10-25) — Side curtain airbag improperly secured. Inspection + realignment.
   📡 24V935000 (2024-12-17) — TPMS warning light not persisting. OTA fix.
   📡 22V844000 (2022-11-15) — Tail lights fail intermittently. OTA fix.
   ...

   Class-action angle: the FSD Beta recall affects 2016-2023 Model S, Model X, 2017-2023 Model 3, 2020-2023 Model Y. Plaintiffs' firms could pursue consumer-fraud claims around marketing of FSD as "Full Self-Driving" when NHTSA determined it "may allow the vehicle to act unsafe around intersections."
   ```

## Who pays for this data (context for the user)

- **Class-action plaintiffs' firms** — build cases around defect campaigns
- **Auto journalists** — break stories on Park It! / Park Outside! recalls
- **Used car dealers** — check inventory for unrepaired open recalls
- **Fleet managers** — proactively schedule recall service
- **Insurance underwriters** — adjust risk models
- **Auto parts suppliers** — track which OEMs are recalling which components (replacement parts demand)
- **Investors** — bad recalls move stocks (Tesla -7% on FSD recall, GM -5% on Chevy Bolt fire recall)

## Relationship to AlphaStack portfolio

Corresponds to the `nhtsa-recalls-tracker` Apify actor (`0txCJmOv8HmFKlg87`).
