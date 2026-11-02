"""Make a fresh run folder for one arm of the experiment, for any coding agent.

    python make_run.py none 1        # runs/none_s1: the bare task
    python make_run.py skill 1       # runs/skill_s1: the same task, plus skills/kick-physics

The run folder is a copy of workspace/. AGENTS.md is also copied to CLAUDE.md and GEMINI.md,
the names Claude Code and Gemini CLI read by default. The skill arm adds the skill folder where
the common agents look for skills (.agents/skills and .claude/skills). The grader and its hidden
data stay outside the run folder.

Env: any Python 3.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPT = "Read TASK.md and complete the task."
SKILL_DIRS = [".agents/skills", ".claude/skills"]


def main():
    """Create runs/<arm>_s<seed> and print how to run an agent in it."""
    arm = sys.argv[1]
    seed = sys.argv[2]
    if arm not in ("none", "skill"):
        raise SystemExit("arm must be none or skill")
    run_dir = HERE / "runs" / f"{arm}_s{seed}"
    if run_dir.exists():
        raise SystemExit(f"{run_dir} exists: use another seed")
    shutil.copytree(HERE / "workspace", run_dir)
    for name in ["CLAUDE.md", "GEMINI.md"]:
        shutil.copy(run_dir / "AGENTS.md", run_dir / name)
    if arm == "skill":
        for folder in SKILL_DIRS:
            shutil.copytree(HERE / "skills", run_dir / folder)
    relative = run_dir.relative_to(HERE)
    print(f"Made {relative}. Run ONE of these, then score it:\n")
    print(f"  cd {relative} && claude -p \"{PROMPT}\"      # Claude Code")
    print(f"  cd {relative} && codex exec \"{PROMPT}\"     # OpenAI Codex CLI")
    print(f"  cd {relative} && gemini -p \"{PROMPT}\"      # Gemini CLI")
    print(f"  python ask_llm.py {relative}                    # no agent: one call to any chat API\n")
    print(f"  python grader/score.py {relative}")


if __name__ == "__main__":
    main()
