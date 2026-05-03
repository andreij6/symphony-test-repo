---
tracker:
  kind: linear
  project_slug: "symphony-claude-e60631494ae6"
  active_states:
    - Todo
    - In Progress
  terminal_states:
    - Done
    - Cancelled
    - Canceled
    - Duplicate
    - Closed
polling:
  interval_ms: 15000
workspace:
  root: ~/code/symphony-test-workspaces
hooks:
  after_create: |
    git clone https://github.com/andreij6/symphony-test-repo .
    pip install -r requirements.txt
agent:
  max_concurrent_agents: 3
  max_turns: 20
codex:
  runner: claude_code
  command: claude --model claude-sonnet-4-6 --print --verbose --output-format stream-json --max-turns 50 --permission-mode bypassPermissions
  turn_timeout_ms: 3600000
  stall_timeout_ms: 300000
---

You are working on a Linear ticket `{{ issue.identifier }}`.

{% if attempt %}
Continuation context:

- This is retry attempt #{{ attempt }} because the ticket is still in an active state.
- Resume from the current workspace and workpad state instead of restarting from scratch.
- Do not repeat already-completed investigation or validation unless needed.
{% endif %}

## Issue

Identifier: {{ issue.identifier }}
Title: {{ issue.title }}
Current status: {{ issue.state }}
URL: {{ issue.url }}

Description:
{% if issue.description %}
{{ issue.description }}
{% else %}
No description provided.
{% endif %}

## Instructions

1. This is an unattended session. Never ask a human to perform follow-up actions.
2. Stop early only if blocked by missing required auth or secrets you cannot resolve.
3. Your final message must report completed actions and blockers only — no "next steps for user."

## Repository

Work only in the provided repository copy. Run `pytest tests/ -v` to verify correctness before every push.

## Workflow

### Step 0 — Route on current state

- `Todo` → move to `In Progress`, then execute.
- `In Progress` → resume from current state.
- `Done` / terminal → do nothing, shut down.

### Step 1 — Plan and implement

1. Read the issue title and description carefully.
2. Create or update a single persistent Linear comment (`## Workpad`) with:
   - A short plan checklist
   - Acceptance criteria matching the issue description
3. Create a feature branch: `git checkout -b {{ issue.identifier | downcase }}-<short-slug>`
   - Example: `git checkout -b spa-9-add-priority-field`
   - Never commit directly to `main`.
4. Implement the change on that branch. Keep it focused — no scope creep.
5. Run `pytest tests/ -v` — all tests must pass.
6. Commit with a clear message and push: `git push -u origin <branch-name>`
7. Open a PR targeting `main`: `gh pr create --title "{{ issue.identifier }}: {{ issue.title }}" --body "Closes {{ issue.url }}"`
8. Move the issue to `Done`.

### Guardrails

- Use exactly one `## Workpad` comment per issue.
- Never edit the issue body.
- Never commit to `main` — always use a feature branch.
- Keep PRs small and scoped to the issue.
- If tests fail, fix them before pushing.
