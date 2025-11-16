from tests.users_data import User, valid_user_data, generate_invalid_user_data
from tests.users_helpers import fill_user_form, find_row_by_email
from playwright.sync_api import Page
import pytest


def go_to_users_page(page: Page):
    if not page.url.endswith("/users"):
        page.locator("span", has_text="Users").click()
    page.wait_for_selector('[data-testid="loading-spinner"]', state="detached")


def open_create_user_dialog(page: Page):
    # 1. Open Dialog
    page.get_by_test_id("create-user-button").click()

    # 2. Assert that the dialog opens
    dialog = page.wait_for_selector('[data-testid="create-user-dialog"]')
    return dialog


# This tests the 2 cases where the user is created - TC2
@pytest.mark.parametrize("user", valid_user_data)
def test_valid_user_creation(login: Page, user: User):
    page = login

    # Go to users page
    go_to_users_page(page)

    # Open dialog
    open_create_user_dialog(page)

    # Fill & submit
    fill_user_form(page, user)
    page.get_by_role("button", name="Save").click()

    # Dialog must close
    page.wait_for_selector('[data-testid="create-user-dialog"]', state="detached")

    # User must be present in data grid
    matching_row = find_row_by_email(page, user["email"])
    assert (
        matching_row is not None
    ), f"User with email {user['email']} not found in data grid"


# This tests the 62 cases where data is not acepted - TC1
@pytest.mark.parametrize("user", generate_invalid_user_data())
def test_invalid_user_creation(login: Page, user: User):
    print(user)
    page = login

    # Go to users page
    go_to_users_page(page)

    # Open dialog
    open_create_user_dialog(page)

    # Fill & submit
    fill_user_form(page, user)
    page.get_by_role("button", name="Save").click()

    # All invalid elements must have aria-invalid="true" - means that have a red border
    for field, value in user.items():
        if value == "" and field != "wallet":
            input_el = page.locator(f"input[name='{field}']")
            assert (
                input_el.get_attribute("aria-invalid") == "true"
            ), f"{field} should be invalid"
