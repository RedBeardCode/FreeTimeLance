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


@pytest.fixture(scope='session')
def splinter_driver_kwargs():
    try:
        tunnel_id = os.environ['TRAVIS_JOB_NUMBER']
        browser = os.environ['SAUCE_BROWSER']
        platform = os.environ['SAUCE_PLATFORM']
        desired_cap = {
            'platform': platform,
            'browserName': browser,
            'tunnelIdentifier': tunnel_id
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


@pytest.fixture
def logined_admin_browser(browser, live_server, db, admin_user):
    create_test_data()
    browser.visit(live_server.url)
    browser.find_by_name('username')[0].value = 'admin'
    browser.find_by_name('password')[0].value = 'password'
    browser.find_by_value('Login')[0].click()
    assert browser.is_element_not_present_by_id('#project_list_table',
                                                wait_time=3)
    yield browser
    browser.driver.close()
