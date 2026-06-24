# Skill Creator

A meta-skill for creating new Claude Code skills. Use this when a user asks to create, scaffold, or generate a new skill.

## What is a Skill

A Claude Code skill is a markdown file (`SKILL.md`) placed inside a directory under `skills/`. The file contains instructions that teach Claude how to perform a specific task. Skills are invoked with `/skill-name` and appear in the available skills list automatically.

## Directory Structure

Each skill lives in its own directory:

```
skills/
  <skill-name>/
    SKILL.md          # Required: skill definition
    templates/        # Optional: template files
    examples/         # Optional: example files
```

## SKILL.md Format

A well-structured SKILL.md includes:

1. **Title** (`# Skill Name`) — clear, concise name
2. **Description** — one-paragraph summary of what the skill does and when to use it
3. **Trigger conditions** — when this skill should be invoked (keywords, patterns, contexts)
4. **Inputs** — what the user provides (arguments, files, context)
5. **Workflow** — step-by-step instructions Claude follows to execute the skill
6. **Output** — what gets produced (files created, modifications made, information returned)
7. **Examples** — concrete usage examples showing input and expected output
8. **Error handling** — how to handle common failure cases

## Workflow

When the user asks to create a new skill:

1. **Gather requirements**: Ask the user what the skill should do, when it should trigger, and what it should produce. If the user already provided enough detail, skip to step 2.
2. **Choose a name**: Pick a short, kebab-case name (e.g., `db-migration`, `api-scaffold`, `test-generator`).
3. **Create the directory**: `skills/<skill-name>/`
4. **Write the SKILL.md**: Follow the format above. Be specific in the workflow section — Claude executes these instructions literally.
5. **Add templates** (if needed): Create template files the skill references.
6. **Test the skill**: Verify the SKILL.md is valid markdown and the instructions are unambiguous.
7. **Report back**: Show the user the created skill and how to invoke it.

## Writing Good Skill Instructions

- Be imperative and specific: "Read the file at X" not "You might want to read X"
- Include exact tool calls when possible: "Use Glob to find all `*.test.ts` files"
- Specify output format: "Create a file named `<name>.migration.sql`"
- Handle edge cases: "If no tests exist, create the test directory first"
- Keep instructions atomic: one clear action per step
- Avoid vague language: "appropriately", "as needed", "if necessary" — specify the condition

## Examples

### Creating a simple skill

User: "Create a skill that generates a changelog from git commits"

Result:

```
skills/changelog/SKILL.md
```

With content covering:
- Reading git log between two refs
- Grouping commits by type (feat, fix, chore, etc.)
- Generating formatted markdown changelog
- Writing to CHANGELOG.md

### Creating a skill with templates

User: "Create a skill that scaffolds a new API endpoint"

Result:

```
skills/api-endpoint/
  SKILL.md
  templates/
    route.ts.template
    handler.ts.template
    test.ts.template
```

## Notes

- Skill names must be unique across the project
- Keep SKILL.md files focused — one skill per task
- Complex workflows should be broken into multiple skills
- Always include at least one usage example in the SKILL.md
