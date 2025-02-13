# ContentClassificator

## Project Status:
In development

---

### Entry point
Run `main.py`

---

### Features
- Custom UI library based on Pygame (core component of the project)
- Import graph generator script for project structure analysis (experimental)
- Custom font creation toolkit (work in progress)
  - Includes tools and instructions for font development

---

### PyCharm Changes
To prevent highlighting in PyCharm IDE, the `# noqa` comment is used in specific files (list below) 
to ignore PEP 8 warnings. This approach is preferred over disabling inspections globally, 
as it provides more granular control.

Used in files:
- `commands/element_interaction_commands.py`
- `commands/trivial_commands.py`

---

### Available documentation
- `docs/`: project documentation
  - `commint_convention.md`: a binding list of rules for commit text
  - `kerning_manual.txt`: instructions for working with font kerning
  - `issues.md`: known issues (almost empty, just initialized)
- `test_scripts/auto_analyze/README.md`: instructions for visualization imports across the project

---

### Refactoring Needed
   The following files require refactoring:
   - `main.py`
   - `UI_elements/simple_buttons.py`
   - `print` statement in `UI_elements/UI_abstracts.py`
   - `print` statements in `handlers/trivial_handlers.py`
