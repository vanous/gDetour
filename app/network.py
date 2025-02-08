# Copyright (C) 2025 vanous
#
# This file is part of gDetour.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ifaddr


def get_interfaces():
    data = []
    for adapter in ifaddr.get_adapters():
        for ip in adapter.ips:
            if type(ip.ip) is tuple:  # ipv6 addresses, skip
                continue
            if ip.ip.startswith("169.254."):
                continue  # local link addresses on Windows, skip
            data.append((ip.ip, ip.nice_name))
    return data
