# Project Overview
This is for developing CN7000 architecture.

## Directory Layout
project-root/
|-- AGENTS/ # AI assistant resources
|-- analysis # contains analysis of the architecture by the AI assistants and humans
|-- earlysim # contains the artifacts that describe the architecture, datamodel and other collateral for CN7000

## Rules

1. **Worktrees**: Always create worktrees in './worktrees/'
2. **Commit Format**: For`  1.  'earlysim', follow the format in  '.AGENTS/kernel_commit_format.md'
3. **Scope**: All code work should be within this project direcory. DO not read/write to copies in other directories unless explicitly discussed.
4. **Base Branch**: All branches in 'earlysim' are relative to 'origin/main' unless otherwise stated.
5. **earlysim local git repository root**: The git repository local root for earlysim is at earlysim

