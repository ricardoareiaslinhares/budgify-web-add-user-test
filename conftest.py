import pytest
from constants import login_url, highlights_url, admin_username, admin_password


@pytest.fixture
def login(playwright):
    # Launch a browser context with slow motion
    context = playwright.chromium.launch_persistent_context(
        user_data_dir="/tmp/playwright",
        headless=True,
        # slow_mo=1000,  # delay per action
    )
    page = context.new_page()
    page.set_default_timeout(10000)
    page.goto(login_url)
    page.get_by_label("Email").fill(admin_username)
    page.get_by_label("Password").fill(admin_password)

    # Click the login button
    page.locator('button[type="submit"]').click()

    # Wait to be redirected
    page.wait_for_url(highlights_url)

    yield page
    context.close()
