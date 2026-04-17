---
name: github-repo-intel
description: Analyzes GitHub repositories to generate competitive and commercial intelligence reports. Returns stars, forks, contributor count, commit velocity, issue triage rate, pull request merge rate, release cadence, top contributors, top dependents, security advisories, and a computed "health score". Use when the user asks about an open-source project's health, wants to evaluate a library before adopting it, needs VC-style due diligence on an OSS company, researches a competitor's GitHub, or wants to identify top contributors to recruit. Uses the official free GitHub REST API and GraphQL API — optional API token gives higher rate limits (5000 req/hr authenticated vs 60 req/hr anonymous). Replaces OSS Insight ($99+/month), SourceGraph ($49-99/month), and Snyk ($25-98/user/month) for core repo intelligence.
---

# GitHub Repo Intelligence

## When to invoke

Trigger on any OSS project / repo analysis:

- "Evaluate next.js for my project"
- "GitHub intel on anthropics/skills"
- "Is Deno healthier than Node.js by commit velocity?"
- "Top contributors to React"
- "Due diligence on Vercel's OSS portfolio"
- "Should I use tRPC or GraphQL?"

## Required input

- **Repo** in `{owner}/{repo}` format (e.g. `vercel/next.js`, `anthropics/skills`)
- **Optional time window** (default: last 90 days for activity metrics)

## Output format

### 1. Top-line
`"{owner}/{repo} — {stars} stars, {forks} forks, {contributors} contributors. Health score: {0-100}."`

### 2. Activity metrics (table)

| Metric | Value | Percentile |
|--------|------:|----------:|
| Commits (last 90 days) | | |
| Pull requests merged | | |
| Issues opened | | |
| Issues closed | | |
| Median PR merge time | | |
| Median issue close time | | |
| Releases | | |
| Contributors (last 90 days) | | |

### 3. Top contributors

| Contributor | Commits | % of PRs |
|-------------|--------:|--------:|

### 4. Dependency / reverse-dependency signal
- **Top dependents** — packages/repos that depend on this one (shows ecosystem importance)
- **Security advisories** — any open CVEs affecting the repo
- **Stale issues / PRs** — queue depth indicator

### 5. Health score (0-100)
Computed from:
- Commit velocity (last 90 days vs lifetime average)
- PR merge rate (merged / opened last 90 days)
- Issue close rate
- Release cadence (releases last 12 months)
- Contributor diversity (bus factor)
- Open security advisories (deduction)

## Data source + procedure

### 1. Basic repo metadata

```
GET https://api.github.com/repos/{owner}/{repo}
```

Returns `stargazers_count`, `forks_count`, `subscribers_count`, `open_issues_count`, `default_branch`, etc.

### 2. Contributors

```
GET https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100
GET https://api.github.com/repos/{owner}/{repo}/stats/contributors  (commit velocity per contributor)
```

### 3. Recent commits

```
GET https://api.github.com/repos/{owner}/{repo}/commits?since={date}&per_page=100
```

### 4. Pull requests (merged vs closed vs opened)

```
GET https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc
```

Filter client-side by `merged_at !== null`.

### 5. Issues activity

```
GET https://api.github.com/repos/{owner}/{repo}/issues?state=all&since={date}
```

Exclude PRs (GitHub returns both under /issues). Filter where `pull_request` is undefined.

### 6. Releases

```
GET https://api.github.com/repos/{owner}/{repo}/releases?per_page=50
```

### 7. Security advisories

```
GET https://api.github.com/repos/{owner}/{repo}/security-advisories
```

### 8. Dependents count (requires GraphQL or HTML scrape)

GitHub's Dependency Graph has a `/network/dependents` page. For API, use GraphQL:

```graphql
query {
  repository(owner: "vercel", name: "next.js") {
    dependencyGraphManifests(first: 10) {
      nodes { dependenciesCount }
    }
  }
}
```

## Authentication + rate limits

- **Unauthenticated**: 60 req/hr per IP — enough for 1-2 repos before hitting the limit
- **Authenticated (PAT)**: 5,000 req/hr — plenty for normal use
- User should set `GITHUB_TOKEN` env var or pass token in headers: `Authorization: Bearer ghp_...`

## Health score rubric

```
score = 0
+25 if commits_last_90d >= 50
+20 if pr_merge_rate_last_90d >= 0.7
+15 if median_pr_merge_time_hours <= 72
+10 if issue_close_rate_last_90d >= 0.5
+10 if releases_last_12m >= 4
+10 if contributors_last_90d >= 10
+10 if contributors_lifetime >= 50
-15 if open_critical_security_advisories > 0
-10 if last_commit_age_days > 180
```

Round to [0, 100].

## Example invocation

User: "GitHub intel on anthropics/skills"

The skill should:
1. Query all endpoints above
2. Compute metrics
3. Return:
   ```
   anthropics/skills — 2,487 stars, 312 forks, 34 contributors. Health score: 78/100.

   Activity (last 90 days):
   | Commits | 147 | ↑ above avg |
   | PRs merged | 62 | ↑↑ |
   | PR merge rate | 83% | top quartile |
   | Median PR merge | 18 hrs | top decile |
   | Issues closed | 89 | > issues opened (41) |
   | Releases | 8 | healthy cadence |

   Top contributors:
   | @danny-avila | 48 | 31% |
   | @tyhopp | 23 | 15% |
   | @ericbuess | 12 | 8% |

   Health breakdown:
   + Active development (commits well above historical mean)
   + High PR merge rate (83% — healthy review culture)
   + Fast merge time (18hr median — maintainers responsive)
   + Good contributor diversity
   - One open CVE (CVE-2026-1234 — medium severity)

   Recommendation: healthy, actively-maintained repo. Suitable for production adoption.
   ```

## License + source

GitHub API data is public for public repos. Uses GitHub's REST v3 and GraphQL v4 APIs per their terms of service. Respect rate limits.
