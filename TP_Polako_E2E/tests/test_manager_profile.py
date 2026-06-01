import pytest
from TP_Polako_E2E.base.base_test import BaseManagerTest

class TestManagerProfile(BaseManagerTest):

    # BADGE
    def test_manager_role_badge_is_visible(self):
        self.manager_profile.verify_user_role_badge()

    def test_commission_badge_and_text_format(self):
        self.manager_profile.verify_commission_badge_visible()
        commission_text = self.manager_profile.get_commission_text()

        assert len(commission_text) > 0, "The commission badge is empty"
        assert "%" in commission_text or any(char.isdigit() for char in commission_text), \
            f"The commission text '{commission_text}' has an invalid format"

    # WARNING BANNER
    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_warning_banner_visibility_and_navigation_to_contract_data(self):
        self.manager_profile.verify_warning_banner_visible()
        self.manager_profile.click_banner_fill_data()
        self.manager_profile.expect_url("contract-data")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_warning_banner_navigation_to_contracts(self):
        self.manager_profile.verify_warning_banner_visible()
        self.manager_profile.click_banner_create_contract()
        self.manager_profile.expect_url("contracts")

    # SIDEBAR NAV
    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_manager_sidebar_elements_visibility(self):
        self.manager_profile.verify_company_btn_visible()
        self.manager_profile.verify_event_management_link_visible()
        self.manager_profile.verify_contract_data_btn_visible()
        self.manager_profile.verify_contracts_btn_visible()
        self.manager_profile.verify_reports_btn_visible()
        self.manager_profile.verify_qr_code_btn_visible()
        self.manager_profile.verify_withdraw_btn_visible()
        self.manager_profile.verify_publications_btn_visible()
        self.manager_profile.verify_manage_btn_visible()

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_company_page(self):
        self.manager_profile.click_company_btn()
        self.manager_profile.expect_url("company")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_event_management(self):
        self.manager_profile.force_click_event_management_link()
        self.manager_profile.expect_url("events")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_contract_data(self):
        self.manager_profile.click_contract_data_btn()
        self.manager_profile.expect_url("contract-data")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_contracts(self):
        self.manager_profile.click_contracts_btn()
        self.manager_profile.expect_url("contracts")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_reports(self):
        self.manager_profile.click_reports_btn()
        self.manager_profile.expect_url("reports")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_qr_code_generator(self):
        self.manager_profile.click_qr_code_btn()
        self.manager_profile.expect_url("qr-generator")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_withdraw(self):
        self.manager_profile.click_withdraw_btn()
        self.manager_profile.expect_url("withdraw")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_publications(self):
        self.manager_profile.click_publications_btn()
        self.manager_profile.expect_url("publications")

    @pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
    def test_sidebar_navigate_to_manage_hub(self):
        self.manager_profile.click_manage_btn()
        self.manager_profile.expect_url("manage")
