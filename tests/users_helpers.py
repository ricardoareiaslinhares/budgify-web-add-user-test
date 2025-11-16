from playwright.sync_api import Page
from users_data import User


def fill_user_form(page: Page, user: User):
    # NAME
    name_input = page.locator('input[name="name"]')
    name_input.fill(user["name"])
    assert name_input.input_value() == user["name"]

    # EMAIL
    email_input = page.locator('input[name="email"]')
    email_input.fill(user["email"])
    assert email_input.input_value() == user["email"]

    # PASSWORD
    pw_input = page.locator('input[name="password"]')
    pw_input.fill(user["password"])
    assert len(pw_input.input_value()) == len(user["password"])

    # DATE OF BIRTH
    user_birthdate_value = user["dateOfBirth"]
    if user_birthdate_value != "":
        dob_input = page.locator('input[name="dateOfBirth"]')
        dob_input.fill(user_birthdate_value)
        assert dob_input.input_value() == user_birthdate_value
    """
       The only way to have a wrong value in the date field is not to put nothing at all,
       otherwise the browser forces corrected values 
    """

    # GENRE
    # Open the dropdown
    gender_input = page.locator('#mui-component-select-genre[role="combobox"]')
    gender_input.click()

    # Click the option
    page.get_by_role("option", name=user["genre"], exact=True).nth(0).click()

    assert gender_input.inner_text().strip() == user["genre"]

    # ALLOW WALLET WATCH
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


def find_row_by_email(page: Page, email_to_find: str):
    grid = page.locator('div[role="grid"]')
    grid.wait_for()

    rows = grid.locator('div[role="row"]')
    total_rows = rows.count()
    print(f"Total rows found (including header): {total_rows}")

    for i in range(total_rows):
        row = rows.nth(i)
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
