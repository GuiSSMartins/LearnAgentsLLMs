# LearnAgents

This repository is 

From:
- "Claude Code in Action" course (by Anthropic - with Coursera) 

## How to setup for "Claude Code in Action" course

1) Install Claude on the system:
- MacOS (Homebrew): brew install --cask claude-code
- MacOS, Linux, WSL: curl -fsSL https://claude.ai/install.sh | bash
- Windows CMD (Windwos 10 or later): curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd 

2) Setup claide code to start (without subscription - with free tier API)

Suggestion: OpenRouter's free API

```bash
$env:OPENROUTER_API_KEY="sk-or-v1-xxxxxxxx"
$env:ANTHROPIC_BASE_URL="https://openrouter.ai/api"
$env:ANTHROPIC_AUTH_TOKEN=$env:OPENROUTER_API_KEY
$env:ANTHROPIC_API_KEY=""
```


```bash
# initate the claude code CLI
claude 
# for claude to analyzise the project repository (generates a summary file CLAUDE.md)
/init
# accept making changes on all files

/clear
```

But, it is also possible to craete differnet summary files depending on 
    1. Project memory (./CLAUDE.md)
    2. Project memory (local) (./CLAUDE.local.md)
    3. User memory (~/.claude/CLAUDE.md)

You can add custom instructions into CLAUDE.md (as comments in the messages affecting directly on the file)
in the form 
\# Enters memory mode to intelligently edit CLAUDE.md files with custom instructions (NOT custom commands!!!! - see above)
You make changes to the scripts you send in order for the Claude to memorize to not make certain actions in teh fuutre (e.g. too many comments)

Add context for better answers (@ character): @<path_to_file_or_folder>
It automatically includes a file's contents in your request to Claude

? for list of possible shortcuts

__TIP__: you can append IMAGES to your requests/prompts
__TIP 2__: you can also add "think" or "plan" words (depth vs breadth) to make Claude make better researches to fidn better solutions to your requests (with different degrees depending on how much tokens it can use to generate better solutions) 

- __Planning__ when we want Claude to understand many parts on the project code (particular tricky bit of the project).
- __Thinking__ is more when it has to research more to find a solution to a complex problem (like several steps to complete).

__WARNING__: using those words wastes more tokens than the ones it would usually use without those _words_!!!!!!!!!!!!!!!!!!!!!!!!

__Claude is also a Git ASSISTANT__ that cna make commits and review pull requests, etc.

```bash
/install-github-app
```

__TIP 3__: it's good for writing automated (unitary) tests.

_ESC_ to stop any Claude execution.
_ESC + ESC_ to return to the previous message.

nOMES DE FUNÇÕES EXPLICITAS NO PROMPTS DEVEM SER ESCRITAS CPOM '' (e.g. 'getSession')

.claudeignore para garantir que certos ficheiros nunca sejam observados/analizados pelo Claude Code

strategy for this sensitive code change:
- You'll use @ mentions only for files directly involved in user data and authentication logic.
- You'll explicitly exclude sensitive files like .env, configuration, and database files using CLAUDE.md and a .claudeignore file.
- For structural information about sensitive data, you'll provide schema details (like column names) within CLAUDE.md rather than the actual data.

/ to observe a bunch of commands you can use.

For more, search how to create __CUSTOM COMMANDS__ $ARGUMENTS

Adding MCP Servers to Cluade in order for it to, for example, access the web.

_WARNING_ NOT on claude !

```bash
claude mcp add <------->  @<-start_local_server_at_your_machine->
# Example
claude mcp add playwright npx @playwright/mcp@latest
```

.claude
|- commands (folder)
   |-
|settings.local.json

_Hooks_ PreToolUse and PostToolUse hooks

3) Install Node.JS (and its dependencies)

4) Prepare database for exercises

```bash
cd _e7efd33cfe0e406d8679082fce8f0ae5_uigen
# Setup SQLite Database
npm run setup
npm run dev
```