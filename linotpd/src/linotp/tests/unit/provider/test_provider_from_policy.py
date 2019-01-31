# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2019 KeyIdentity GmbH
#
#    This file is part of LinOTP server.
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License, version 3, as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the
#               GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    E-mail: linotp@keyidentity.com
#    Contact: www.linotp.org
#    Support: www.keyidentity.com
#

import unittest
from mock import patch

from linotp.lib.user import User
from linotp.provider import get_provider_from_policy

mocked_context = {
    'Client': '123.123.123.123'
    }

class TestProviderFromPolicy(unittest.TestCase):
    """
    unit test to identify provider  from policy
    """
    @patch('linotp.provider.request_context', new=mocked_context)
    def test_get_default_provider(self):
        """
        get the default providers if no policy
        """
        with patch("linotp.provider.get_client_policy") as mock_policy:
            with patch(
                "linotp.provider._get_default_provider_name") as mock_default:

                mock_policy.return_value = {}
                mock_default.return_value = 'default'

                provider = get_provider_from_policy(
                    'sms', user=User('login', 'realm'))

                assert provider == ['default']


    @patch('linotp.provider.request_context', new=mocked_context)
    def test_get_policy_provider(self):
        """
        get the providers from the policy
        """

        with patch("linotp.provider.get_client_policy") as mocked_policy:

            mocked_policy.return_value = {
                'one': {
                    'name': 'one',
                    'scope': 'authentication',
                    'active': True,
                    'action': 'sms_provider=  one   two ,  ',
                    'realm': '*',
                    'user': '*'
                    }
                }

            provider = get_provider_from_policy(
                'sms', user=User('login', 'realm'))

            assert provider == ['one', 'two']


# eof #
