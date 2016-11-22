#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration of the pytest with CmdLine options, Fixtures and TearDown function
"""
import os

import pytest

from django.core.management import call_command
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
