"""Tests for SelectionList handling of out-of-range highlighted indices."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import SelectionList


class SelectionListApp(App[None]):
    """Test selection list application."""

    def compose(self) -> ComposeResult:
        yield SelectionList[int](*[(str(n), n) for n in range(10)])


async def test_highlight_after_remove_does_not_raise() -> None:
    """Removing an option should not cause OptionDoesNotExist when highlighted index is stale.

    Regression test for https://github.com/Textualize/textual/issues/6726.
    """
    async with SelectionListApp().run_test() as pilot:
        assert isinstance(pilot.app, SelectionListApp)
        await pilot.pause()
        selections = pilot.app.query_one(SelectionList)
        # Highlight an option near the end
        selections.highlighted = 8
        await pilot.pause()
        # Remove options so that index 8 no longer exists
        selections.remove_option_at_index(0)
        selections.remove_option_at_index(0)
        selections.remove_option_at_index(0)
        await pilot.pause()
        # Now trigger a re-highlight by setting highlighted to the same value
        # This should not raise OptionDoesNotExist
        selections.highlighted = 8
        await pilot.pause()


async def test_clear_options_does_not_raise() -> None:
    """Clearing options should not cause OptionDoesNotExist when highlighted index is stale."""
    async with SelectionListApp().run_test() as pilot:
        assert isinstance(pilot.app, SelectionListApp)
        await pilot.pause()
        selections = pilot.app.query_one(SelectionList)
        # Highlight an option
        selections.highlighted = 5
        await pilot.pause()
        # Clear all options
        selections.clear_options()
        await pilot.pause()
        # Setting highlighted should not raise
        selections.highlighted = 0
        await pilot.pause()
