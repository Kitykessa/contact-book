import pytest
import pandas as pd
import project
import csv

@pytest.fixture
def temp_csv(tmp_path):
    csv_path = tmp_path / "contacts.csv"
    df = pd.DataFrame(columns=["Name", "Email", "Number"])
    df.to_csv(csv_path, index=False)

    project.CSV_FILE = str(csv_path)
    return csv_path

def test_csv_init(temp_csv):
    df = pd.read_csv(temp_csv, dtype={"Number": str})
    assert list(df.columns) == ["Name", "Email", "Number"]
    assert df.empty

def test_add_contact(monkeypatch, tmp_path):
    inputs = iter([
        "",
        "test",
        "invalid_email",
        "valid@mail.com",
        "123",
        "+123456789"
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = project.add_contact()
    assert result is True

def test_add_contact_duplicate(monkeypatch, temp_csv):
    pd.DataFrame([["Test", "test@mail.com", "+1111111111"]], columns=["Name", "Email", "Number"])\
    .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter([
        "Test",
        "test@mail.com",
        "+1111111111"
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = project.add_contact()
    assert result is False

    df = pd.read_csv(temp_csv)
    assert len(df) == 1

def test_delete_contact_yes(monkeypatch, temp_csv):
    pd.DataFrame([["Test", "test@mail.com", "+1111111111"]], columns=["Name", "Email", "Number"])\
    .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter(["test", "yes"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = project.delete_contact()
    assert result is True

    df = pd.read_csv(temp_csv, dtype={"Number": str})
    assert df.empty

def test_delete_contact_no(monkeypatch, temp_csv):
    pd.DataFrame([["Test", "test@mail.com", "+1111111111"]], columns=["Name", "Email", "Number"])\
    .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter(["test", "no"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = project.delete_contact()
    assert result is False

    df = pd.read_csv(temp_csv, dtype={"Number": str})
    assert not df[df["Name"].str.lower() == "test"].empty

def test_search_contact(monkeypatch, capsys, temp_csv):
    pd.DataFrame([["Test", "test@mail.com", "+1111111111"]], columns=["Name", "Email", "Number"])\
      .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter(["test"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    project.search_contact()
    captured = capsys.readouterr()
    assert "Test" in captured.out
    assert "test@mail.com" in captured.out

def test_search_contact_by_number(monkeypatch, capsys, temp_csv):
    pd.DataFrame([["Test", "test@mail.com", "+1111111111"]], columns=["Name", "Email", "Number"])\
      .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter("+1111111111")
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    project.search_contact()
    captured = capsys.readouterr()
    assert "Test" in captured.out
    assert "+1111111111" in captured.out

def test_load_contacts_empty(capsys, temp_csv):
    project.load_contacts()
    captured = capsys.readouterr()
    assert "No contact found." in captured.out


def test_load_contacts_with_data(capsys, temp_csv):
    pd.DataFrame([
        ["Test", "test@mail.com", "+1111111111"]
    ], columns=["Name", "Email", "Number"]).to_csv(temp_csv, mode="a", index=False, header=False)

    project.load_contacts()
    captured = capsys.readouterr()
    assert "All contacts:" in captured.out
    assert "Test" in captured.out
    assert "test@mail.com" in captured.out
    assert "+1111111111" in captured.out


def test_update_contact(monkeypatch, temp_csv):
    pd.DataFrame([["Test", "test@mail.com", "+1111111111"]], columns=["Name", "Email", "Number"])\
      .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter([
        "test",
        "Update",
        "new@mail.com",
        "+777777777"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = project.update_contact()
    assert result is True

    df = pd.read_csv(temp_csv, dtype={"Number": str})
    assert df.iloc[0]["Name"] == "Update"
    assert df.iloc[0]["Email"] == "new@mail.com"
    assert df.iloc[0]["Number"] == "+777777777"

def test_update_contact_only_email(monkeypatch, temp_csv):
    pd.DataFrame([["Test", "test@mail.com", "+1111111111"]], columns=["Name", "Email", "Number"])\
      .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter([
        "test",
        "",
        "new@mail.com",
        ""
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = project.update_contact()
    assert result is True

    df = pd.read_csv(temp_csv, dtype={"Number": str})
    assert df.iloc[0]["Name"] == "Test"
    assert df.iloc[0]["Email"] == "new@mail.com"
    assert df.iloc[0]["Number"] == "+1111111111"

def test_update_contact_duplicate_number_or_email(monkeypatch, temp_csv):
    contacts = [
        ["Test", "test@mail.com", "+1111111111"],
        ["Tuk", "tuk@mail.com", "+2222222222"]
    ]
    pd.DataFrame(contacts, columns=["Name", "Email", "Number"])\
      .to_csv(temp_csv, mode="a", index=False, header=False)

    inputs = iter([
        "test",
        "",
        "tuk@mail.com",
        "+2222222222",
        "",
        ""
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = project.update_contact()
    assert result is True

    df = pd.read_csv(temp_csv, dtype={"Number": str})
    updated = df[df["Name"] == "Test"].iloc[0]
    assert updated["Email"] == "test@mail.com"
    assert updated["Number"] == "+1111111111"

