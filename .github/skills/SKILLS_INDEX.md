# SKILLS_INDEX

Purpose: fast skill routing with minimal token usage.

## Usage Rules (cost-optimized)
- Do not preload all skill files.
- First, match request text against `triggers`.
- Load only the selected skill's `SKILL.md`.
- If no strong match, ask 1 short clarifying question.
- Prefer exact instruction compliance over adding extra steps.

## Available Skills

### 1) setup-mcp-server-project
- path: `.agents/skills/setup-mcp-server-project/SKILL.md`
- use_when: user asks to create/scaffold/setup a new MCP server project.
- triggers: `mcp server`, `new server`, `scaffold`, `setup project`, `create project`

## Maintenance
- Keep each skill entry under 8 lines.
- Keep triggers short, lowercase, comma-separated.
- Update this file whenever skills are added/removed.
