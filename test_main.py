import pytest

from main import main, pyramid_pattern


def lines_of(capsys):
    """Return captured stdout as a list of lines (no trailing empty line)."""
    return capsys.readouterr().out.splitlines()


# ---------- pyramid_pattern: exact output ----------

def test_single_row(capsys):
    pyramid_pattern(1)
    assert lines_of(capsys) == ["*"]


def test_three_rows_exact(capsys):
    pyramid_pattern(3)
    assert lines_of(capsys) == [
        "  *",
        " ***",
        "*****",
    ]


def test_five_rows_exact(capsys):
    pyramid_pattern(5)
    assert lines_of(capsys) == [
        "    *",
        "   ***",
        "  *****",
        " *******",
        "*********",
    ]


# ---------- pyramid_pattern: edge cases ----------

def test_zero_prints_nothing(capsys):
    pyramid_pattern(0)
    assert capsys.readouterr().out == ""


def test_negative_prints_nothing(capsys):
    pyramid_pattern(-4)
    assert capsys.readouterr().out == ""


def test_returns_none(capsys):
    assert pyramid_pattern(2) is None


# ---------- pyramid_pattern: shape properties for many sizes ----------

@pytest.mark.parametrize("n", [1, 2, 4, 7, 10, 25])
def test_shape_properties(capsys, n):
    pyramid_pattern(n)
    rows = lines_of(capsys)

    # one line per row
    assert len(rows) == n

    for i, row in enumerate(rows):
        leading = len(row) - len(row.lstrip(" "))
        stars = row.strip(" ")

        # row is only spaces then stars, nothing trailing
        assert set(stars) == {"*"}
        assert row == row.rstrip()

        # i-th row has 2i+1 stars and n-i-1 leading spaces
        assert len(stars) == 2 * i + 1
        assert leading == n - i - 1

    # bottom row has no indent and is the widest
    assert rows[-1] == "*" * (2 * n - 1)


# ---------- main ----------

def test_main_full_output(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "3")
    main()
    assert lines_of(capsys) == [
        "Hello, World!",
        "  *",
        " ***",
        "*****",
        "Goodbye!",
    ]


def test_main_passes_prompt(monkeypatch, capsys):
    prompts = []

    def fake_input(prompt=""):
        prompts.append(prompt)
        return "1"

    monkeypatch.setattr("builtins.input", fake_input)
    main()
    assert prompts == ["Enter a number: "]


def test_main_zero(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "0")
    main()
    assert lines_of(capsys) == ["Hello, World!", "Goodbye!"]


def test_main_handles_whitespace_around_number(monkeypatch, capsys):
    # int() strips surrounding whitespace, so this should work
    monkeypatch.setattr("builtins.input", lambda prompt="": "  2 \n")
    main()
    assert lines_of(capsys) == ["Hello, World!", " *", "***", "Goodbye!"]


@pytest.mark.parametrize("bad", ["abc", "", "3.5", "two"])
def test_main_rejects_non_integer(monkeypatch, capsys, bad):
    monkeypatch.setattr("builtins.input", lambda prompt="": bad)
    with pytest.raises(ValueError):
        main()
    # "Hello" already printed, but no pyramid and no "Goodbye"
    out = capsys.readouterr().out
    assert out.startswith("Hello, World!")
    assert "Goodbye!" not in out
