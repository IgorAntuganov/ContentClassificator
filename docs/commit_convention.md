   # Agreement on Commits

> - translated with yandex and redacted with GPT Claude 3.5 
> - Версия на русском в отдельном файле (ru version in separate file)

   ## Commit format
 - `<type>`: `<short description>`
 - [empty string required]
 - `<commit body>`
 - [empty string required]
 - [`<optional footer>`] (Details)
 - [empty string required if footer exists]
 - PS:`<number>` CWF: `<brief description>`

  ### Types of commits
   - Feat: new functionality
   - Fix: error correction
   - Refactor: refactoring the code
   - Chore: updating routine tasks, etc.; without changing the production code
   - Style: formatting, indentation, etc.; without changing the code
   - Docs: changes in documentation
   - Test: adding tests, refactoring tests; without changing the production code

##### Optional
   - (minor): small commit
   - (major): enormous commit
   - (`<scope name>`): name of the module/component being changed (e.g., font, commands)
   - | WIP: Work In Progress - incomplete changes, project may be unstable
   - Start, Merge for special conditions

  ### Short description
   Description should contain 3-8 words  
   Optionally you can use up to 12 or even more words, especially if words are short, just look at readability

  ### Empty string #1
   Required for correct representation

  ### Commit Body
   List of changes in commit.
   Description should contain string of 3-8 words
   Optionally you can use up to 12 or even more words, especially if words are short, just look at readability

  ### Empty string #2
   Required for correct representation

  ### Optional footer (Details)

   List of details, required to understand changes   
   Also may contain 1-2 small todo ideas  
   For example:
> &#45; Right-click on an element to initiate dragging  
> &#45; Right-click again on the element to end dragging  

  ### Empty string #3
   Required for correct representation  
   Use only after optional footer (Details) if you need one

  ### Project Status (PS)
   - PS:0 - the project is in perfect condition
   - PS:1, PS:2, etc. - the number of known problems or unfinished tasks

  ### Current Workflow (CWF)
A brief description of the current main task or line of work, maybe scope name

---

## Examples

> Docs: Add todo_ideas.md
>
> &#45; Create new todo_ideas.md file with rules  
> &#45; Add 4 initial ideas to todo_ideas.md  
> &#45; Minor improvements to mandelbrot_test.py  
> &#45; Refine a little docs/commit_convention.md  
> 
> PS:3 | CWF: Enhance project documentation and organization

---

> Refactor(commands) | WIP: Restructure command package (part 2)
> 
> &#45; Rename files containing abstract classes:  
>   - command_classes.py -> abstract_commands.py  
>   - command_handlers.py -> abstract_handlers.py  
>
> &#45; Improve naming of command implementation files:  
>   - dragging_family.py -> dragging_commands.py  
>   - hover_family.py -> hover_commands.py  
> 
> &#45; Update imports across the project to reflect new file names
> 
> PS: 678 | CWF: lorem ipsum

---

> Feat: add cursor changing during dragging (part 1)
> 
> &#45; Add new class CursorManager  
> &#45; Add new command family and handler: CursorCommands  
> 
> Details:  
> &#45; now cursor change to "CHANGLE_ALL" during dragging  
> 
> PS: 678 | CWF: lorem ipsum

---

> Feat: rework adjusting with dragging logic (part 2)
>  
> &#45; Refactor handle_mouse method into two separate met hods  
> &#45; Make multiple methods in UI_abstracts.py private  
> &#45; Implement right-click to start/stop element dragging,  
> instead of holding the right mouse button
> 
> Details:
> &#45; Right-click on an element to initiate dragging
> &#45; Right-click again on the element to end dragging  
> 
> PS: 678 | CWF: lorem ipsum