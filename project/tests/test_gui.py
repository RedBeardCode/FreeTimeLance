# coding=utf-8


class TestAddButton:

    def test_project_add_button(self, logined_admin_browser, live_server):
        logined_admin_browser.visit(live_server.url)
        add_button = logined_admin_browser.find_by_css('.add-button')
        assert add_button
        add_button.click()
        assert logined_admin_browser.url == live_server.url + '/create/'

    def test_customer_add_button(self, logined_admin_browser, live_server):
        logined_admin_browser.visit(live_server.url + '/customer/')
        add_button = logined_admin_browser.find_by_css('.add-button')
        assert add_button
        add_button.click()
        target_url = live_server.url + '/customer/create/'
        assert logined_admin_browser.url == target_url

    def test_activity_add_button(self, logined_admin_browser, live_server):
        logined_admin_browser.visit(live_server.url + '/activity/')
        add_button = logined_admin_browser.find_by_css('.add-button')
        assert add_button
        add_button.click()
        target_url = live_server.url + '/activity/create/'
        assert logined_admin_browser.url == target_url
