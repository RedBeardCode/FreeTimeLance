#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration of the pytest with CmdLine options, Fixtures and TearDown
function
"""
import os
try:
    from httplib import HTTPException
except ImportError:
    from http.client import HTTPException
from random import randint

import pytest
from invitations.models import Invitation
from pytest_splinter.plugin import get_args, _take_screenshot
from selenium.common.exceptions import WebDriverException

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
    """Splinter browser instance getter. To be used for getting of
     plugin.Browser's instances.

    :return: function(parent). Each time this function will return new instance
    of plugin.Browser class.
    """
    def get_browser(splinter_webdriver, retry_count=3):
        kwargs = get_args(driver=splinter_webdriver,
                          download_dir=splinter_file_download_dir,
                          download_ftypes=splinter_download_file_types,
                          firefox_pref=splinter_firefox_profile_preferences,
                          firefox_prof_dir=splinter_firefox_profile_directory,
                          remote_url=splinter_remote_url,
                          executable=splinter_webdriver_executable,
                          driver_kwargs=splinter_driver_kwargs)
        try:
            return splinter_browser_class(
                splinter_webdriver,
                visit_condition=splinter_browser_load_condition,
                visit_condition_timeout=splinter_browser_load_timeout,
                wait_time=splinter_wait_time, **kwargs
            )
        except Exception:  # NOQA
            if retry_count > 1:
                return get_browser(splinter_webdriver, retry_count - 1)
            else:
                raise

    def prepare_browser(request, parent):
        splinter_webdriver = request.getfuncargvalue('splinter_webdriver')
        splinter_session_scoped_browser = request.getfuncargvalue(
            'splinter_session_scoped_browser')
        splinter_close_browser = request.getfuncargvalue(
            'splinter_close_browser')
        browser_key = id(parent)
        browser = browser_pool.get(browser_key)
        if not splinter_session_scoped_browser:
            browser = get_browser(splinter_webdriver)
            if splinter_close_browser:
                request.addfinalizer(browser.quit)
        elif not browser:
            browser = browser_pool[browser_key] = get_browser(
                splinter_webdriver)

        if request.scope == 'function':
            def _take_screenshot_on_failure():
                if splinter_make_screenshot_on_failure and \
                        request.node.splinter_failure:
                    _take_screenshot(
                        request=request,
                        fixture_name=parent.__name__,
                        browser_instance=browser,
                        splinter_screenshot_dir=splinter_screenshot_dir,
                        splinter_screenshot_getter_html=splinter_screenshot_getter_html,
                        splinter_screenshot_getter_png=splinter_screenshot_getter_png,
                    )
            request.addfinalizer(_take_screenshot_on_failure)

        try:
            if splinter_webdriver not in browser.driver_name.lower():
                raise IOError('webdriver does not match')
            if hasattr(browser, 'driver'):
                browser.driver.implicitly_wait(splinter_selenium_implicit_wait)
                browser.driver.set_speed(splinter_selenium_speed)
                browser.driver.command_executor.set_timeout(
                    splinter_selenium_socket_timeout)
                browser.driver.command_executor._conn.timeout = \
                    splinter_selenium_socket_timeout
                if splinter_window_size:
                    browser.driver.set_window_size(*splinter_window_size)
            browser.cookies.delete()
            for url in splinter_clean_cookies_urls:
                browser.visit(url)
                browser.cookies.delete()
            if hasattr(browser, 'driver'):
                browser.visit_condition = splinter_browser_load_condition
                browser.visit_condition_timeout = splinter_browser_load_timeout
                browser.visit('about:blank')
        except (IOError, HTTPException, WebDriverException):
            # we lost browser, try to restore the justice
            try:
                browser.quit()
            except Exception:  # NOQA
                pass
            browser = browser_pool[browser_key] = get_browser(
                splinter_webdriver)
            prepare_browser(request, parent)

        return browser

    return prepare_browser


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
