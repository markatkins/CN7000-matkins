# CN7000 Workflows

Each workflow operates in its own git worktree under `./worktrees/`.

## Workflows

| # | Workflow | Branch | Worktree Path |
|---|----------|--------|---------------|
| 1 | Main Repo | `main` | `./worktrees/main` |
| 2 | Packet Taxonomy | `packet-taxonomy` | `./worktrees/packet-taxonomy` |
| 3 | Requirements | `requirements` | `./worktrees/requirements` |
| 4 | Solutions | `solutions` | `./worktrees/solutions` |
| 5 | Doc Reviews | `doc-reviews` | `./worktrees/doc-reviews` |

## Setup

```bash
# Create worktree directory
mkdir -p worktrees

# Create worktrees (one per workflow)
git worktree add worktrees/main main
git worktree add -b packet-taxonomy worktrees/packet-taxonomy main
  * git branch --set-upstream-to=origin/main packet-taxonomy
git worktree add -b requirements worktrees/requirements main
git worktree add -b solutions worktrees/solutions main
git worktree add -b doc-reviews worktrees/doc-reviews main
```

## Usage

Work in the appropriate worktree for each workflow:

```bash
cd worktrees/packet-taxonomy   # Packet taxonomy work
cd worktrees/requirements      # Requirements analysis
cd worktrees/solutions         # Solutions documentation
cd worktrees/doc-reviews       # Document reviews
```

Each worktree is an independent checkout — commits, branches, and staging areas are isolated.
