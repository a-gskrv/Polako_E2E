import re
import os
import pytest

import pytest
from playwright.sync_api import expect

from TP_Polako_E2E.base.base_test import BaseUserTest
from TP_Polako_E2E.utils.constants import (
    INVALID_NEW_PASSWORD,
    INVALID_PROFILE_DATA,
    PARTIAL_PROFILE_DATA,
    VALID_NEW_PASSWORD,
    VALID_PROFILE_DATA,
)


class TestUserProfile(BaseUserTest):

    # ELEMENTS VISIBILITY
    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_profile_sidebar_button(self):
        self.user_profile.verify_profile_btn_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_purchase_history_sidebar_button(self):
        self.user_profile.verify_purchase_history_btn_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_balance_sidebar_button(self):
        self.user_profile.verify_balance_btn_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_user_role_badge(self):
        self.user_profile.verify_user_role_badge()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_logout_button(self):
        self.user_profile.verify_logout_button_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_first_name_input_field(self):
        self.user_profile.verify_first_name_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_last_name_input_field(self):
        self.user_profile.verify_last_name_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_email_input_field(self):
        self.user_profile.verify_email_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_phone_input_field(self):
        self.user_profile.verify_phone_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_instagram_input_field(self):
        self.user_profile.verify_instagram_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_telegram_input_field(self):
        self.user_profile.verify_telegram_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_new_password_input_field(self):
        self.user_profile.verify_new_password_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_confirm_password_input_field(self):
        self.user_profile.verify_confirm_password_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_visibility_change_password_submit_button(self):
        self.user_profile.verify_change_password_btn_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigation_routing(self):
        self.user_profile.click_purchase_history_btn()
        expect(self.page).to_have_url(re.compile(r"purchases"))

        self.user_profile.click_balance_btn()
        expect(self.page).to_have_url(re.compile(r"balance"))

        self.user_profile.click_profile_btn()
        expect(self.page).to_have_url(re.compile(r"personal-information"))

    # DATA PROFILE

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_successful_full_profile_update(self):
        self.user_profile.click_profile_btn()

        self.user_profile.fill_all_profile_fields(VALID_PROFILE_DATA)
        self.user_profile.click_save_profile()

        self.page.reload()

        actual_data = self.user_profile.get_all_profile_values()
        assert (
            actual_data == VALID_PROFILE_DATA
        ), f"It was expected {VALID_PROFILE_DATA}, but it appears in the UI {actual_data}."

    @pytest.mark.skip(reason="Test is under development")
    def test_partial_profile_update_and_field_clearing(self):
        self.user_profile.click_profile_btn()

        self.user_profile.fill_all_profile_fields(PARTIAL_PROFILE_DATA)
        self.user_profile.click_save_profile()

        self.page.reload()

        actual_data = self.user_profile.get_all_profile_values()
        assert actual_data["first_name"] == PARTIAL_PROFILE_DATA["first_name"]
        assert actual_data["last_name"] == ""

    @pytest.mark.skip(reason="Test is under development")
    def test_invalid_profile_data_validation(self):
        self.user_profile.click_profile_btn()

        self.user_profile.fill_all_profile_fields(INVALID_PROFILE_DATA)
        self.user_profile.click_save_profile()

        self.page.reload()
        actual_data = self.user_profile.get_all_profile_values()
        assert (
            actual_data != INVALID_PROFILE_DATA
        ), "The system saved critically invalid data!"

    # CHANGE PASSWORD

    @pytest.mark.skip(reason="Test is under development")
    def test_successful_password_change(self):
        self.user_profile.click_profile_btn()
        self.user_profile.verify_new_password_visible()
        self.user_profile.verify_confirm_password_visible()

        self.user_profile.change_password(
            new_pass=VALID_NEW_PASSWORD,
            confirm_pass=VALID_NEW_PASSWORD,
            expected_status=200,
        )

        self.user_profile.change_password(
            new_pass=os.getenv("SIMPLE_USER_PASSWORD"),
            confirm_pass=os.getenv("SIMPLE_USER_PASSWORD"),
            expected_status=200,
        )

    @pytest.mark.skip(reason="Test is under development")
    def test_password_mismatch_error(self):
        self.user_profile.click_profile_btn()

        self.user_profile.change_password(
            new_pass=VALID_NEW_PASSWORD,
            confirm_pass=VALID_NEW_PASSWORD[::-1],
            expected_status=None,
        )

        error_message = self.user_profile.page.locator(
            ".error-message-selector"
        ).text_content()
        assert "The passwords do not match!" in error_message

    @pytest.mark.skip(reason="Test is under development")
    def test_empty_password_submission_error(self):
        self.user_profile.click_profile_btn()

        self.user_profile.change_password(
            new_pass="", confirm_pass="", expected_status=None
        )

        self.user_profile.change_password(
            new_pass=INVALID_NEW_PASSWORD,
            confirm_pass=INVALID_NEW_PASSWORD,
            expected_status=None,
        )

        assert self.user_profile.page.is_disabled("button.change-password-submit")
