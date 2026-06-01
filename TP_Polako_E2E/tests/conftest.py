import os
import re
from pathlib import Path
from urllib.parse import urlparse

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from TP_Polako_E2E.api.auth_api import AuthApi
from TP_Polako_E2E.api.profile_api import ProfileApi

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

print("DEBUG STG_URL =", repr(os.getenv("STG_URL")))

ENVIRONMENTS = {
    "stg": os.getenv("STG_URL"),
}

missing = []
for env_name, url in ENVIRONMENTS.items():
    if not url:
        missing.append(f"{env_name} (STG_URL)")

if missing:
    raise RuntimeError(f"Missing env variables: {', '.join(missing)}")

ARTIFACTS_DIR = ROOT_DIR / "artifacts"

SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"

for directory in (
    SCREENSHOTS_DIR,
    VIDEOS_DIR,
    TRACES_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="stg",
        help="Environment: stg",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "smoke: smoke tests",
    )

    config.addinivalue_line(
        "markers",
        "regression: regression tests",
    )

    config.addinivalue_line(
        "markers",
        "ui: ui tests",
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    env = pytestconfig.getoption("--env")

    if env not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment: {env}")

    return ENVIRONMENTS[env]


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args,
):
    if os.getenv("CI"):
        headless_mode = True
    else:
        headless_mode = os.getenv("HEADLESS", "false").lower() == "false"  #true

    return {
        **browser_type_launch_args,
        "headless": headless_mode,
    }


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args,
):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "record_video_dir": str(VIDEOS_DIR),
    }


@pytest.fixture
def app_page(
    page: Page,
    base_url,
    request,
):
    test_name = request.node.name

    page.context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    page.set_default_timeout(10_000)
    page.set_default_navigation_timeout(30_000)

    page.context.clear_cookies()

    page.goto(
        base_url,
        wait_until="domcontentloaded",
    )

    page.evaluate(
        "() => {" "window.localStorage.clear();" "window.sessionStorage.clear();" "}"
    )

    page.reload()

    try:
        yield page

    finally:
        safe_name = re.sub(
            r'[<>:"/\\\\|?*]',
            "_",
            test_name,
        )

        trace_path = TRACES_DIR / f"{safe_name}.zip"

        page.context.tracing.stop(path=str(trace_path))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call,
):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    if report.passed:
        return

    page = item.funcargs.get("app_page") or item.funcargs.get("page")

    if not page:
        return

    safe_name = re.sub(
        r'[<>:"/\\\\|?*]',
        "_",
        item.name,
    )

    screenshot_path = SCREENSHOTS_DIR / f"{safe_name}.png"

    page.screenshot(
        path=str(screenshot_path),
        full_page=True,
    )


@pytest.fixture(scope="session")
def user_api_token():
    base_url = os.getenv("STG_URL")
    email = os.getenv("SIMPLE_USER_EMAIL")
    password = os.getenv("SIMPLE_USER_PASSWORD")

    auth_client = AuthApi(base_url)
    return auth_client.login_and_save_token(email, password)


@pytest.fixture(scope="session")
def manager_api_token():
    base_url = os.getenv("STG_URL")
    email = os.getenv("VALID_EMAIL")
    password = os.getenv("VALID_PASSWORD")

    auth_client = AuthApi(base_url)
    return auth_client.login_and_save_token(email, password)


@pytest.fixture(scope="session")
def api_auth_token(manager_api_token):
    return manager_api_token


def _authenticate_via_cookie(page, token: str):
    raw_url = os.getenv("STG_URL")
    parsed = urlparse(raw_url)
    clean_base_url = f"{parsed.scheme}://{parsed.netloc}"
    domain = parsed.netloc

    page.context.add_cookies([
        {
            "name": "access_token",
            "value": token,
            "domain": domain,
            "path": "/",
        }
    ])
    page.goto(f"{clean_base_url}/ru/user/personal-information")
    page.wait_for_load_state("networkidle")


@pytest.fixture(scope="function")
def authorized_profile_api(api_auth_token, base_url):
    return ProfileApi(base_url=base_url, token=api_auth_token)


@pytest.fixture(scope="function")
def user_page(app_page, user_api_token):
    return _authenticate_via_cookie(app_page, user_api_token)


@pytest.fixture(scope="function")
def manager_page(app_page, manager_api_token):
    return _authenticate_via_cookie(app_page, manager_api_token)


@pytest.fixture(scope="function")
def authenticated_page(manager_page):
    return manager_page
