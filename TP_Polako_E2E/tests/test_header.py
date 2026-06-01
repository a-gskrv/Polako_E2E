import pytest
from playwright.sync_api import expect

from TP_Polako_E2E.base.base_test import BaseTest
from TP_Polako_E2E.pages.common.header import CONTACT_LINKS
from TP_Polako_E2E.utils.constants import EXPECTED_MARKERS, SECTIONS_MAPPING


class TestHeader(BaseTest):

    def test_login_button_for_guest(self):
        self.header_page.verify_login_button_visible()

    def test_header_for_authorized_user(self):
        self.login_page.login_as_valid_user()

        self.header_page.verify_profile_button_visible()

    def test_click_logo(self):
        self.header_page.click_logo()

    def test_verify_logo_visible(self):
        self.header_page.verify_logo_visible()

    def test_logo_navigation_to_home(self):
        self.page.goto(f"{self.page.url}/events")

        self.header_page.verify_logo_visible()

        self.header_page.click_logo()

        expect(self.page).to_have_url("https://stg.polakohedonist.club/ru")

    def test_header_elements_for_guest(self):
        self.header_page.verify_logo_visible()

        self.header_page.verify_login_button_visible()

    def test_language_switching_flow(self):
        assert "Русский" in self.header_page.get_current_language_text()

        self.header_page.change_language("en")
        expect(self.page).to_have_url("https://stg.polakohedonist.club/en")

        assert "English" in self.header_page.get_current_language_text()

        self.header_page.change_language("sr")
        expect(self.page).to_have_url("https://stg.polakohedonist.club/sr")

        assert "Srpski" in self.header_page.get_current_language_text()

        self.header_page.change_language("ru")
        expect(self.page).to_have_url("https://stg.polakohedonist.club/ru")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_main_navigation_links(self):
        for section, url_path in SECTIONS_MAPPING.items():
            self.header_page.verify_nav_link_visible(section)
            self.header_page.click_nav_link(section)

            if url_path.startswith("http"):
                expected_url = url_path
            elif url_path.startswith("#"):
                expected_url = f"https://stg.polakohedonist.club/ru{url_path}"
            else:
                expected_url = f"https://stg.polakohedonist.club/ru/{url_path}"

            expect(self.page).to_have_url(expected_url)

            if url_path.startswith("http"):
                self.page.goto("https://stg.polakohedonist.club/ru")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_cart_button_navigation(self):
        self.header_page.click_cart()
        expect(self.header_page.get_cart_drawer_locator()).to_be_visible(timeout=3000)

    @pytest.mark.parametrize("network_name, selector", CONTACT_LINKS.items())
    def test_contacts_dropdown_links(self, network_name, selector):
        self.header_page.open_contacts_dropdown()

        actual_href = self.header_page.get_contact_href(network_name)

        assert EXPECTED_MARKERS[network_name] in actual_href, (
            f"Error in social media {network_name}! "
            f"Wait marker '{EXPECTED_MARKERS[network_name]}', but received '{actual_href}'"
        )
