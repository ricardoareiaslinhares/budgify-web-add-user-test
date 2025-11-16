import pytest
from constants import login_url, highlights_url, admin_username, admin_password

"""
When a pytest runs (function that starts with 'test_') it aumatically looks for 'fixtures' that have the same name
as the test parameter; then searchs and runs fixtures whose name is equal to those parameters.
And provides clean up after.

https://docs.pytest.org/en/stable/how-to/fixtures.html
"""


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

    yield page  # Returns to the test
    context.close()  # Runs after the test
