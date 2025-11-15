from constants import users_url
from users_data import valid_user_data, generate_invalid_user_data
import pytest


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
