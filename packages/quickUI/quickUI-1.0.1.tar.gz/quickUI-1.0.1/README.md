# Quick View

<p align="center">
    <a href="https://www.codefactor.io/repository/github/oscarvsp/quickui"><img src="https://www.codefactor.io/repository/github/oscarvsp/quickui/badge" alt="CodeFactor" /></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-v3.8%20%7C%20v3.9%20%7C%20v3.10%20%7C%20v3.11-blue" alt="Python v3.8 | v3.9 | v3.10 | v3.11" /></a>
    <a href="https://github.com/DisnakeDev/disnake"><img src="https://img.shields.io/badge/disnake-v2.8-blue" alt="disnake == 2.8" /></a>
</p>

An extension for the [disnake library](https://github.com/DisnakeDev/disnake) that aims to extend the current set of item and view to facilitate the creation of UI for `ApplicationCommand`.

## Installation

```
pip install quickUI
```

## Documentation

Here is a list of the new items and views.

You can find the complet documentation [here](https://oscarvsp.github.io/quickUI/)

### Items

- CycleButton
    >This is a button that automatically cycle between a given set of state when clicked. See [example](examples/cycle_button.py)
- ModalButton
    >This is a button that automatically send a modal when clicked. See [example](examples/modal_button.py)
- ModalSelect
    >This is a select that automatically a modal depending of the option selected. See [example](examples/modal_select.py)
- UserHybridModal
    >This is a select that allow you to extract only `User` and `Member` from a selection of mentionable (`User`, `Member` and `Role`). See [example](examples/user_hybrid_select.py)

### Views

- QView
    >This is a subclass of `disnake.ui.View` that is required to used most of the above item while still being completely compatible with other items and view usage.

- ConfirmationView
    >This is a view that already contains 2 buttons: one to confirm the interaction and one to cancel it. The confirm button can be easily disable/enable with condition. This is usefull for interaction where the user has to provide some information or make some choice before going to the next step. See [example](examples/code_locked_view.py)

## Example

You can find example for each new item and view in [/examples](examples)
