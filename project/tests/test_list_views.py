from random import randint

import pytest


def mark_ie_xfail(logined_browser):
    if logined_browser.driver.capabilities['browserName'] in \
            ['internet explorer']:
        pytest.xfail("Because of an issue in Selenuium "
                     "https://github.com/seleniumhq/"
                     "selenium-google-code-issue-archive/issues/4403")


class TestProjectView:
    def test_list_as_staff(self, logined_admin_browser,
                           live_server):
        mark_ie_xfail(logined_admin_browser)
        logined_admin_browser.visit(live_server.url)
        table_rows = logined_admin_browser.find_by_css('.clickable-row')
        assert len(table_rows) == 50
        table_cells = logined_admin_browser.find_by_css('.clickable-row td')
        assert len(table_cells) == 200
        for i in [randint(0, 49) for _ in range(5)]:
            logined_admin_browser.is_text_present('Projektname', wait_time=3)
            logined_admin_browser.execute_script("window.scrollTo(0, 0);")
            row = logined_admin_browser.find_by_css('.clickable-row')[i]
            row.find_by_css('a')[0].click()
            assert logined_admin_browser.is_text_present(
                'Vereinbartes Zeitkontingent', wait_time=3)
            logined_admin_browser.back()
            row = logined_admin_browser.find_by_css('.clickable-row')[i]
            row.find_by_css('a')[3].click()
            logined_admin_browser.is_text_present('Submit', wait_time=3)
            assert live_server + '/update/' in logined_admin_browser.url
            logined_admin_browser.back()

    def test_side_menu_as_staff(self, logined_admin_browser,
                                live_server):
        mark_ie_xfail(logined_admin_browser)
        logined_admin_browser.visit(live_server.url)
        assert logined_admin_browser.find_by_css('.sidebar')
        assert len(logined_admin_browser.find_by_css('#side-menu ul li')) == 3
        logined_admin_browser.find_by_css('#side-menu').click()
        logined_admin_browser.find_by_css('#side-menu ul li a')[0].click()
        assert logined_admin_browser.url == live_server.url + '/customer/'
        logined_admin_browser.find_by_css('#side-menu').click()
        logined_admin_browser.find_by_css('#side-menu ul li a')[1].click()
        assert logined_admin_browser.url == live_server.url + '/'
        logined_admin_browser.find_by_css('#side-menu').click()
        logined_admin_browser.find_by_css('#side-menu ul li a')[2].click()
        assert logined_admin_browser.url == live_server.url + '/activity/'

    def test_add_button_as_staff(self, logined_admin_browser,
                                 live_server):
        mark_ie_xfail(logined_admin_browser)
        logined_admin_browser.visit(live_server.url)
        assert logined_admin_browser.find_by_css('.add-button')
        logined_admin_browser.find_by_css('.add-button').click()
        assert logined_admin_browser.is_text_present('Name of the project',
                                                     wait_time=3)
        assert logined_admin_browser.url == live_server.url + '/create/'

    def test_list_customer(self, logined_browser,
                           live_server):

        logined_browser.visit(live_server.url)
        table_rows = logined_browser.find_by_css('.clickable-row')
        assert len(table_rows) == 10
        table_cells = logined_browser.find_by_css('.clickable-row td')
        assert len(table_cells) == 30
        for i in [randint(0, 9) for _ in range(2)]:
            logined_browser.is_text_present('Projektname', wait_time=3)
            row = logined_browser.find_by_css('.clickable-row')[i]
            row.click()
            assert logined_browser.is_text_present(
                'Vereinbartes Zeitkontingent', wait_time=3)
            logined_browser.back()

    def test_side_menu_button_customer(self, logined_browser,
                                       live_server):
        logined_browser.visit(live_server.url)
        assert not logined_browser.find_by_css('.sidebar')
        assert not logined_browser.find_by_css('.add-button')


class TestActivityView:
    def test_list_as_staff(self, logined_admin_browser,
                           live_server):
        mark_ie_xfail(logined_admin_browser)
        logined_admin_browser.visit(live_server.url + '/activity/')
        table_rows = logined_admin_browser.find_by_css('.clickable-row')
        assert len(table_rows) == 500
        table_cells = logined_admin_browser.find_by_css('.clickable-row td')
        assert len(table_cells) == 2500
        for i in [randint(0, 99) for _ in range(5)]:
            logined_admin_browser.is_text_present('Aktivit', wait_time=3)
            logined_admin_browser.execute_script("window.scrollTo(0, 0);")
            row = logined_admin_browser.find_by_css('.clickable-row')[i]
            row.find_by_css('a')[0].click()
            logined_admin_browser.is_text_present('Update', wait_time=3)
            assert live_server + '/activity/update/' in \
                logined_admin_browser.url
            logined_admin_browser.back()

    def test_side_menu_button_as_staff(self, logined_admin_browser,
                                       live_server):
        logined_admin_browser.visit(live_server.url + '/activity/')
        assert logined_admin_browser.find_by_css('.sidebar')
        assert logined_admin_browser.find_by_css('.add-button')

    def test_list_customer(self, logined_browser,
                           live_server):
        logined_browser.visit(live_server.url + '/activity/')
        assert logined_browser.is_text_present(
            'Bitte geben Sie ihre Benutzerdaten ein')
        assert logined_browser.url == live_server + \
            '/accounts/login/?next=/activity/'


class TestCustomerView:
    def test_list_as_staff(self, logined_admin_browser,
                           live_server):
        mark_ie_xfail(logined_admin_browser)
        logined_admin_browser.visit(live_server.url + '/customer/')
        table_rows = logined_admin_browser.find_by_css('.clickable-row')
        assert len(table_rows) == 5
        table_cells = logined_admin_browser.find_by_css('.clickable-row td')
        assert len(table_cells) == 5
        for i in [randint(0, 4) for _ in range(2)]:
            logined_admin_browser.is_text_present('Name', wait_time=3)
            row = logined_admin_browser.find_by_css('.clickable-row')[i]
            row.find_by_css('a')[0].click()
            logined_admin_browser.is_text_present('Update', wait_time=3)
            assert live_server + '/customer/update/' in \
                logined_admin_browser.url
            logined_admin_browser.back()

    def test_side_menu_button_as_staff(self, logined_admin_browser,
                                       live_server):
        logined_admin_browser.visit(live_server.url + '/customer/')
        assert logined_admin_browser.find_by_css('.sidebar')
        assert logined_admin_browser.find_by_css('.add-button')

    def test_list_customer(self, logined_browser,
                           live_server):
        logined_browser.visit(live_server.url + '/customer/')
        assert logined_browser.is_text_present(
            'Bitte geben Sie ihre Benutzerdaten ein')
        assert logined_browser.url == live_server + \
            '/accounts/login/?next=/customer/'
