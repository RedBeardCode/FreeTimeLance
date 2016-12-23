#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration of the pytest with CmdLine options, Fixtures and TearDown
function
"""
import os
from random import randint

import pytest
from invitations.models import Invitation
from pytest_splinter.plugin import browser_instance_getter as splinter_browser_instance_getter

from project.tests.utilities import create_test_data


@pytest.fixture(scope='session')
def splinter_remote_url():
    url = ''
    try:
        user = os.environ['SAUCE_USERNAME']
        key = os.environ['SAUCE_ACCESS_KEY']
        url = 'http://{0}:{1}@ondemand.saucelabs.com:80/wd/hub'.format(user,
                                                                       key)
    except BaseException:
        pass
    return url


@pytest.fixture(scope='function')
def splinter_driver_kwargs(request):
    try:
        tunnel_id = os.environ['TRAVIS_JOB_NUMBER']
        browser = os.environ['SAUCE_BROWSER']
        platform = os.environ['SAUCE_PLATFORM']
        desired_cap = {
            'platform': platform,
            'browserName': browser,
            'tunnelIdentifier': tunnel_id,
            'name': request.node.name,
            'nativeEvents': False,
        }
        return desired_cap
    except BaseException:
        return {}


@pytest.fixture
def invitation():
    invite = Invitation.create('{0}@example.com'.format(randint(11111111,
                                                                99999999)))
    yield invite
    invite.delete()


@pytest.fixture(scope='function')
def browser_instance_getter(
        browser_patches,
        splinter_session_scoped_browser,
        splinter_browser_load_condition,
        splinter_browser_load_timeout,
        splinter_download_file_types,
        splinter_driver_kwargs,
        splinter_file_download_dir,
        splinter_firefox_profile_preferences,
        splinter_firefox_profile_directory,
        splinter_make_screenshot_on_failure,
        splinter_remote_url,
        splinter_screenshot_dir,
        splinter_selenium_implicit_wait,
        splinter_wait_time,
        splinter_selenium_socket_timeout,
        splinter_selenium_speed,
        splinter_webdriver_executable,
        splinter_window_size,
        splinter_browser_class,
        splinter_clean_cookies_urls,
        splinter_screenshot_getter_html,
        splinter_screenshot_getter_png,
        splinter_screenshot_encoding,
        session_tmpdir,
        browser_pool,
):
    return splinter_browser_instance_getter(
        browser_patches,
        splinter_session_scoped_browser,
        splinter_browser_load_condition,
        splinter_browser_load_timeout,
        splinter_download_file_types,
        splinter_driver_kwargs,
        splinter_file_download_dir,
        splinter_firefox_profile_preferences,
        splinter_firefox_profile_directory,
        splinter_make_screenshot_on_failure,
        splinter_remote_url,
        splinter_screenshot_dir,
        splinter_selenium_implicit_wait,
        splinter_wait_time,
        splinter_selenium_socket_timeout,
        splinter_selenium_speed,
        splinter_webdriver_executable,
        splinter_window_size,
        splinter_browser_class,
        splinter_clean_cookies_urls,
        splinter_screenshot_getter_html,
        splinter_screenshot_getter_png,
        splinter_screenshot_encoding,
        session_tmpdir,
        browser_pool)


@pytest.fixture
def freetimelance_browser(request, browser_instance_getter):
    browser = browser_instance_getter(request, freetimelance_browser)
    return browser


@pytest.fixture
def logined_admin_browser(freetimelance_browser, live_server, db, admin_user):
    create_test_data()
    freetimelance_browser.visit(live_server.url)
    freetimelance_browser.find_by_name('username')[0].value = 'admin'
    freetimelance_browser.find_by_name('password')[0].value = 'password'
    freetimelance_browser.find_by_value('Login')[0].click()
    assert freetimelance_browser.is_element_not_present_by_id(
        '#project_list_table', wait_time=3)
    yield freetimelance_browser
    freetimelance_browser.driver.close()


@pytest.fixture(scope='function')
def logined_browser(freetimelance_browser, live_server, db):
    create_test_data()
    freetimelance_browser.visit(live_server.url)
    freetimelance_browser.find_by_name('username')[0].value = 'Customer_0'
    freetimelance_browser.find_by_name('password')[0].value = 'Start123'
    freetimelance_browser.find_by_value('Login')[0].click()
    assert freetimelance_browser.is_element_not_present_by_id(
        '#project_list_table', wait_time=3)
    yield freetimelance_browser
    freetimelance_browser.driver.close()
