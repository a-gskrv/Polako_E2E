import pytest
from TP_Polako_E2E.pages.profile.user_profile_page import UserProfilePage

@pytest.mark.skip(reason="User interface updated — tests temporarily disabled")
def test_user_can_update_first_name(authenticated_page):
    profile_page = UserProfilePage(authenticated_page)

    old_value = profile_page.get_first_name_value()
    new_value = "FirstNameTest"
    if old_value == new_value:
        new_value = "FirstNameTestTest"

    try:
        profile_page.fill_first_name(new_value)
        profile_page.click_save_profile()

        assert profile_page.get_first_name_value() == new_value

    finally:
        profile_page.fill_first_name(old_value)
        profile_page.click_save_profile()
