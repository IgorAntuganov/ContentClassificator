# ContentClassificator

## Project Status:
🚧Temporarily paused🚧  
Development is currently on hold and will resume in approximately two weeks (~20.01.25) or more

---

### PyCharm changes
To prevent highlighting in PyCharm IDE:
1) somewhere in code was used this comment  
 `# noinspection PyPep8Naming`
2) The following PEP 8 warnings have been disabled in the project settings:
   - E301: Expected 1 blank line, found 0
   - E302: Expected 2 blank lines, found 0
   - E701: Multiple statements on one line (colon)
   - Potentially some more

#### How to Apply These Settings
- Go to Settings/Preferences → Editor → Inspections
- Find "PEP 8 coding style violation"
- Add the mentioned error codes (E301, E302, E701) to the ignored list

---

### Entry point
Run `main.py`

---

### Available documentation

- `docs/`: project documentation
  - `commint_convention.md`: a binding list of rules for commit text
  - `kerning_manual.txt`: instructions for working with font kerning
  - `issues.md`: known issues (almost empty, just initialized)

---

### Refactoring Needed
   The following files require refactoring:
   - `main.py`
   - `UI_scene.py`
   - `cursor_manager.py`
