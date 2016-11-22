#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration of the pytest with CmdLine options, Fixtures and TearDown function
"""
import os

import pytest

from django.core.management import call_command
from splinter import Browser

from project.tests.utilities import create_test_data



@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        create_test_data()


@pytest.fixture(scope='session')
def splinter_driver_kwargs():
    try:
        user = os.environ['SAUCE_USERNAME']
        key = os.environ['SAUCE_ACCESS_KEY']
        url = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'.format(user, key)
        tunnel_id = os.environ['TRAVIS_JOB_NUMBER']
        browser = os.environ['SAUCE_BROWSER']
        platform = os.environ['SAUCE_PLATFORM']
        kwargs = {
            'url': url,
            'platform': platform,
            'browserName': browser,
            'tunnelIdentifier': tunnel_id
        }
        return kwargs
    except BaseException:
        return {}


@pytest.fixture(scope='session')
def browser(request,browser_instance_getter):
    user = os.environ['SAUCE_USERNAME']
    key = os.environ['SAUCE_ACCESS_KEY']
    url = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'.format(user, key)
    tunnel_id = os.environ['TRAVIS_JOB_NUMBER']
    browser_name = os.environ['SAUCE_BROWSER']
    platform = os.environ['SAUCE_PLATFORM']
    browser = Browser(driver_name="remote",
            url=url,
            browser=browser_name,
            platform=platform,
                      tunnelIdentifier=tunnel_id,
            name="Test of IE 9 on WINDOWS")
    return browser