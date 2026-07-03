# AI Agents Project Instructions

Skill discovery policy
----------------------

Before executing any implementation task, first check [`.agents/skills/SKILLS_INDEX.md`](.agents/skills/SKILLS_INDEX.md) and use it to route to the best matching skill.

Skill loading workflow (performance + token cost)
-------------------------------------------------

1. Read [`.agents/skills/SKILLS_INDEX.md`](.agents/skills/SKILLS_INDEX.md) first.
2. Match the request against the index triggers.
3. Load only the selected skill file under `.agents/skills/**/SKILL.md`.
4. If no strong match exists, ask one short clarifying question.
5. Follow the selected skill exactly and do not add extra steps unless requested by the user.

### Priority order

1. User request
2. This file
3. Skill selection and routing rules in [`.agents/skills/SKILLS_INDEX.md`](.agents/skills/SKILLS_INDEX.md)
4. Matching skill instructions in `.agents/skills/**/SKILL.md`
5. Existing repository patterns/templates

Unit and Integration testing policy
-----------------------------------

...