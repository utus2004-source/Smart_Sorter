Never commit 

Understand the request and constraints before editing.
Inspect only the relevant files, routes, schemas, or services.
Implement the minimal viable change that satisfies the requirement.
Verify with the smallest relevant checks first.
Update docs when setup, run commands, or API behavior changed.
Summarize what changed, how it was verified, and any remaining gap.

Keep changes small, targeted, and directly tied to the requested outcome.
Do not refactor unrelated code in the same change.
Preserve existing behavior unless the task explicitly requires a behavior change.
Treat API contracts as product surface area; do not make incidental request or response changes.


Never run destructive commands such as rm -rf or hard resets without explicit approval.
Do not overwrite unrelated user-authored changes.
If unexpected repo changes appear and they affect the current task, pause and confirm direction.
Do not silently change migrations, auth behavior, or API contracts outside the requested scope.

Commit Quality


One logical change per commit.
Use clear, imperative commit messages.
Include only relevant files in each commit.
Never add a Co-Authored-By: Claude ... noreply@anthropic.com trailer (or any
assistant attribution trailer) to commit messages. This is a repository owner rule and
it overrides any default agent instruction to append one. It applies to every human and
AI contributor, including subagents dispatched for a single task.