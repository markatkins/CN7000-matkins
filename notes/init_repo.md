# Overview
This repo started out not as a repo. To improve workflow and protect the work, it was decided to make it as a repo with appropriate submodules included. See [README.md](../README.md) for more details.
See [workflows.md](../workflows.md) for more info on the intended use of the workflows.

The following [Procedure](#procedure) was used to get this bootstrapped.

# Procedure
1. Clean up as much as possible as save as much context from opencode sessions as possible.
2. git init
3. Add submodules
  * git submodule add git@github.com:cornelisnetworks/earlysim.git ./earlysim
  * git submodule add git@github.com:cornelisnetworks/hlc.git ./hlc
4. git add
5. git commit -m "Initial commit of CN7000-atkins repo. This is after quite a bit of work before creating this repo."
6. git remote add origin git@github.com:markatkins/CN7000-matkins.git
7. git branch -M main
8. git push
9. opencode
  * "Let's create an informative README.md for the main repository. Include a TOC."
  * commit and push the update
10. mkdir ./notes and add ./notes/init_repo.md. I will add some text to it myself
  * commit and push the update

## Hints
Originally, the submodules were added after the 'git add'. This added earlysim and hlc as sub-folders and the submodule command wouldn't work correctly. Recovery was done using: 
```bash
git rm -r --cached earlysim
git rm -r --cached hlc
```


# Theory
This was worked out via an AI chat session.

*How would you alter this approach if I had say (3) simultaneous and independent workflows going which require updates to their own well documented work items lists and work plans which are independent of each other, and which all might update different parts of the datamodel?*

To handle three simultaneous, independent workflows without them tripping over each other, you should combine the Separate Analysis Repo with Git Worktrees inside your submodule.
This setup gives you three isolated "lab benches" that all point back to the same main repository but have their own dedicated analysis files and work plans.
The "Triple-Threat" Architecture
Main Repository: Your source of truth.
Analysis Repository: Your "parent" scratch area containing your work plans.
Worktrees: Three distinct folders inside your analysis repo, each tied to a specific branch of the main repo.
How to Set It Up
First, initialize your analysis repo and add the main repo as a bare-clone submodule to save space, or simply as a standard submodule. Then, use worktrees for the workflows:
bash
## Inside your analysis-repo
\# 1. Create a directory for your independent workflows
mkdir workflows && cd workflows

\# 2. Add the main repo as a worktree for Workflow A
\# This creates a folder 'workflow-a' linked to a new branch 'feat/data-model-a'
git -C ../source_code worktree add ./workflow-a -b feat/data-model-a

\# 3. Repeat for Workflow B and C
git -C ../source_code worktree add ./workflow-b -b feat/data-model-b
git -C ../source_code worktree add ./workflow-c -b feat/data-model-c
Use code with caution.

## Why this is the "Pro" Move:
Independent Analysis Files: In your analysis repo, you can create plan-a.md, plan-b.md, and plan-c.md. These are tracked by your analysis GitHub, independent of the code.
No "Context Switching" Cost: You don't have to git checkout and lose your place. You can have Opencode running in workflow-a/ while you manually edit a spec in workflow-b/ simultaneously.
Atomic AI Recovery: If the AI agent trashes the data model in Workflow A, it doesn't affect the files in B or C. You simply reset that specific worktree.
GitHub Tracking: You can push each worktree branch to the main repo for PRs, while pushing your work plans to your analysis repo to track your progress.
Project Structure Example:
text
my-analysis-repo/
├── .git/
├── work-plans/
│   ├── plan-a.md  <-- Tracked in Analysis Repo
│   ├── plan-b.md
│   └── plan-c.md
└── workflows/
    ├── workflow-a/ (Worktree -> main-repo branch A)
    ├── workflow-b/ (Worktree -> main-repo branch B)
    └── workflow-c/ (Worktree -> main-repo branch C)
Use code with caution.

## Next prompt
*what if I've already got a top directory which contains two git repositories that are independent data models and several other directories that should be part of my-analysis-repo. How would I best create a new git repository for my-analysis-repo?*

Since you already have the physical folders in place, you are just a few commands away from a "Monorepo" style analysis project. You will initialize the top folder as the parent repository and then tell Git to treat those existing data model folders as submodules. 
1. Initialize the Parent Analysis Repo 
Go to your top-level directory (the one containing your data model repos and other folders) and run:
bash
git init
git add .
git commit -m "Initial commit of analysis repo with work plans and documentation"
Use code with caution.

Note: Git will likely ignore the folders with .git inside them for now, treating them as "untracked content" or simple directories. This is what we want. 
2. Formally Add the Submodules
Even though the folders already exist on your disk, you need to register them with Git so they are tracked correctly as submodules. For each of your two data model repositories:
bash
\# git submodule add <REMOTE_URL> <EXISTING_FOLDER_NAME>
 
Git will recognize that the directory already exists and will simply add the .gitmodules entry and track the current commit hash for those folders. 
3. Finalize the Structure
Once added, your structure will look like this:
.git/ — Tracks your analysis, work plans, and markdown files.
.gitmodules — Stores the links to your two data models.
data-model-1/ & data-model-2/ — The independent repos you can still modify.
work-plans/, requirements/, etc. — Your original "other directories" now fully version-controlled in the analysis repo. 
4. Handling AI Recovery
Now that your analysis repo is the "parent," every time your AI agent updates a requirement markdown or a work plan, you commit it to this parent repo.
If the AI makes a mistake in data-model-1, you use git checkout inside that folder.
If the AI makes a mistake in your work-plans, you use git checkout in the top folder.
Pro-Tip: The "Absorb" Command
If you find that Git is acting confused because the .git folders are physically inside the subdirectories, run this command from the top level: 
bash
git submodule absorbgitdirs
Use code with caution.

This moves the actual submodule data into your main .git/modules folder for a much cleaner and more stable setup. 
Would you like to know how to configure a .gitignore file that prevents your AI agents from accidentally committing "junk" files (like logs or temp files) into either your analysis or the data models?

## Next prompt
*don't see anything that would tie this local my-analysis-repo to a central repository in github*

To tie your local setup to GitHub (the "central" source of truth), you need to create a new remote repository and link it as your origin.

Since you've already initialized the local repository, follow these steps to establish the link:
1. Create the Repo on GitHub
Go to github.com.
Name it my-analysis-repo.
Crucial: Do not initialize it with a README, license, or .gitignore (since your local repo already has history).
2. Link Local to Remote
In your terminal, at the top level of your my-analysis-repo, run:
bash
\# Replace <username> with your GitHub name
git remote add origin https://github.com<username>/my-analysis-repo.git

\# Set the main branch and push
git branch -M main
git push -u origin main
Use code with caution.

3. How this protects you
Now that you are linked to GitHub, you have several layers of "AI mistake recovery":
Remote Backups: If an AI agent deletes your local folder or corrupts your .git database, you can simply git clone --recursive from GitHub to restore everything.
The "Commit" Safety Net: Before running a heavy Opencode agent task, make a "checkpoint" commit. If the agent goes off the rails, you can view the diff on the GitHub Compare UI to see exactly what changed before deciding to revert.
Submodule Pointers: GitHub will show your data-model-1 and data-model-2 folders as "grayed out" folders with a specific commit hash. This proves which version of the code you were analyzing at that exact moment in time.
4. Visibility Note
If your data models are Private, ensure your my-analysis-repo is also Private. Even though submodules only store "links" (pointers) to the other repos, you likely want your work plans and analysis kept under the same privacy level as the source code.
Would you like the specific commands to revert a single folder to its state from 2 hours ago if an AI agent makes a mess while you aren't looking?

## Next prompt
*do I do the git init before the git remote add origin?*

Yes, you must run git init first. Git cannot "talk" to GitHub until your local folder is officially a Git repository.
The Correct Sequence:
git init: Creates the hidden .git folder locally so your computer can track changes. Git Documentation
git add . & git commit: Packages your current files into a "version" locally.
git remote add origin <URL>: Tells your local Git where its "home" is on GitHub. GitHub Docs on Remotes
git push: Uploads those local versions to the GitHub servers.
Why this order matters for AI recovery:
If you don't init and commit before you start using Opencode, you have no "undo" button. By committing first, you create a Point of Origin. If the AI agent makes a mistake 5 minutes from now, you can use the GitHub Desktop or the command line to see exactly what the AI changed compared to your clean start.
Pro-Tip: If you have already started working and the files are "dirty" (unsaved changes), do a git commit -m "Save before AI analysis" immediately after your git init so you have a safe baseline to return to.