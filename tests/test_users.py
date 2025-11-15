from constants import users_url
from users_data import valid_user_data, generate_invalid_user_data
import pytest


def find_user_by_email(page, user):
    grid = page.locator('div[role="grid"]')
    grid.wait_for()

    headers = grid.locator('div[role="columnheader"]')
    header_count = headers.count()
    print(f"Found {header_count} header columns")

    email_index = None
    for i in range(header_count):
        text = headers.nth(i).inner_text().strip()
        print(f"Header {i}: '{text}'")
        if text == "Email":
            email_index = i
            break

    if email_index is None:
        raise AssertionError("Email column not found")

    print(f"Email column found at index {email_index}")

    rows = grid.locator('div[role="row"]')
    print(rows)
    row_count = rows.count()
    print(f"Found {row_count} rows")

    for i in range(row_count):
        row = rows[i]
        print("row", row)
        cells = row.locator('div[role="cell"]')

        cell_text = cells.nth(email_index).inner_text().strip()
        print(f"Row {i}, Email cell: '{cell_text}'")
        if cell_text == user["email"]:
            print(f"User found in row {i}")
            return row

    raise AssertionError(f'User with email {user["email"]} not found')


def find_row_by_email(page, email_to_find: str):
    grid = page.locator('div[role="grid"]')
    grid.wait_for()

    rows = grid.locator('div[role="row"]')
    total_rows = rows.count()
    print(f"Total rows found (including header): {total_rows}")

    for i in range(total_rows):
        row = rows.nth(i)

        # Force evaluation of the row
        row_text = row.inner_text()  # this actually queries the DOM
        print(f"Row {i} full text: '{row_text}'")

        # locate the email cell
        email_cell = row.locator('div[data-field="email"]')
        if email_cell.count() == 0:
            print(f"Skipping row {i}, no email cell")
            continue

        cell_text = email_cell.inner_text().strip()
        print(f"Row {i} email cell: '{cell_text}'")

        if cell_text == email_to_find:
            print(f"Found matching row at index {i}")
            return row

    print(f"No matching row found for email '{email_to_find}'")
    return None


def fill_user_form(page, user):
    # === NAME ===
    name_input = page.locator('input[name="name"]')
    name_input.fill(user["name"])
    assert name_input.input_value() == user["name"]

    # ---- EMAIL ----
    email_input = page.locator('input[name="email"]')
    email_input.fill(user["email"])
    assert email_input.input_value() == user["email"]

    # ---- PASSWORD ----
    pw_input = page.locator('input[name="password"]')
    pw_input.fill(user["password"])
    assert len(pw_input.input_value()) == len(user["password"])

    # === DATE OF BIRTH ===
    dob_input = page.locator('input[name="dateOfBirth"]')
    dob_input.fill(user["birthdate"])
    assert dob_input.input_value() == user["birthdate"]

    # === GENRE (MUI SELECT) ===
    # Open the dropdown
    gender_input = page.locator('#mui-component-select-genre[role="combobox"]')
    gender_input.click()

    # Click the option
    page.get_by_role("option", name=user["gender"], exact=True).nth(0).click()

    assert gender_input.inner_text().strip() == user["gender"]

    # === ALLOW WALLET WATCH CHECKBOX ===
    # Only interact if the user wants it enabled
    if user["wallet"]:
        # Ensure advanced section is expanded
        advanced_section = page.get_by_test_id("create-user-dropdown-advanced-features")
        if "Show" in advanced_section.inner_text():
            advanced_section.click()

        checkbox = page.get_by_label("Allow Wallet Watch")
        checkbox.wait_for()
        checkbox_input = page.locator('input.PrivateSwitchBase-input[type="checkbox"]')
        checkbox_input.click()

        assert checkbox.is_checked() is True


@pytest.mark.parametrize("user", valid_user_data)
def test_valid_user_creation(login, user):
    page = login

    # Go to users page
    go_to_users_page(page)

    # Open dialog
    open_create_user_dialog(page)

    # Fill & submit
    fill_user_form(page, user)
    page.get_by_role("button", name="Save").click()

    # EXPECTATION: dialog must close
    page.wait_for_selector('[data-testid="create-user-dialog"]', state="detached")

    matching_row = find_row_by_email(page, user["email"])
    assert (
        matching_row is not None
    ), f"User with email {user['email']} not found in data grid"


def go_to_users_page(page):
    if not page.url.endswith("/users"):
        page.locator("span", has_text="Users").click()
    page.wait_for_selector('[data-testid="loading-spinner"]', state="detached")


def open_create_user_dialog(page):
    # 2. Click the button using your stable selector
    page.get_by_test_id("create-user-button").click()

    # 3. Assert that the dialog opens
    dialog = page.wait_for_selector('[data-testid="create-user-dialog"]')
    return dialog
