# -*- coding: utf-8 -*-
#
# Copyright 2017-2018 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Renku integration tests."""

import os
from urllib.parse import urljoin

import pytest
import splinter


def test_renku_login(browser):
    """Test Renku login."""
    url = urljoin(os.getenv('RENKU_ENDPOINT', 'http://localhost'), '/login')
    browser.visit(url)

    assert browser.is_element_present_by_id('username', wait_time=60)
    browser.fill('username', 'demo')
    browser.fill('password', 'demo')
    browser.find_by_id('kc-login').click()
    assert 'Renku' in browser.title


def test_notebook_launch(browser):
    """Test launching a notebook from UI."""
    url = urljoin(os.getenv('RENKU_ENDPOINT', 'http://localhost'), '/login')
    browser.visit(url)

    browser.fill('username', 'cramakri')
    browser.fill('password', 'cramakri')
    browser.find_by_id('kc-login').click()
    assert 'Renku' in browser.title

    # go to the project page
    assert browser.is_element_present_by_text(
        'cramakri/weather-zh', wait_time=10
    )
    proj_link = browser.find_link_by_text('cramakri/weather-zh')
    assert proj_link
    proj_link[0].click()

    # go to the files tab
    files_link = browser.find_link_by_text('Files')
    assert files_link
    files_link[0].click()

    # click the notebooks tab
    notebooks_link = browser.find_link_by_text('Notebooks')
    assert notebooks_link
    notebooks_link[0].click()

    # click the notebook to be viewed
    analysis_link = browser.find_link_by_partial_text('Analysis.ipynb')
    assert analysis_link
    analysis_link[0].click()

    # click the "Launch notebook" button
    notebook_button = browser.find_by_text('Launch Notebook')
    assert notebook_button
    notebook_button[0].click()

    assert 'weather_ch' in browser.html