# This file is part of fedmsg.
# Copyright (C) 2014 Red Hat, Inc.
#
# fedmsg is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# fedmsg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with fedmsg; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <oddshocks@riseup.net>
#
""" Tests for Fedimg messages """

import unittest

from fedmsg.tests.test_meta import Base

from .common import add_doc


class TestImageUploadStart(Base):
    """ These messages are published when an image upload has started. 
        At this point, Fedimg has picked up a completed Koji
        createImage task and will begin the process of registering
        the .raw.xz file as as an image with a cloud provider. """

    expected_title = "fedimg.image.upload"
    image_name = "fedora-cloud-base-rawhide-20140604.x86_64"
    dest = "EC2-eu-west-1"
    expected_subti = "{0} started uploading to {1}".format(image_name,
                                                                 dest)
    expected_link = None
    expected_icon = 'https://apps.fedoraproject.org/img/icons/fedimg.png'
    expected_secondary_icon = None
    expected_packages = set([])
    expected_usernames = set([])
    expected_objects = set(['image/upload/started'])
    msg = {
        u'i': 1,
        u'msg': {
            u'image_url': 'https://kojipkgs.fedoraproject.org//work/'
                          'tasks/5144/6925144/fedora-cloud-base-'
                          'rawhide-20140604.x86_64.raw.xz',
            u'image_name': 'fedora-cloud-base-rawhide-20140604.x86_64',
            u'destination': 'EC2-eu-west-1',
            u'status': 'started',
        },
        u'topic': u'org.fedoraproject.stg.fedimg.image.upload',
        u'username': u'fedimg',
        u'timestamp': 1371498303.125771,
    }


class TestImageUploadComplete(Base):
    """ These messages are published when an image upload finishes.
        At this point, Fedimg has completed registering a .raw.xz
        image with a cloud provider. """

    expected_title = "fedimg.image.upload"
    image_name = "fedora-cloud-base-rawhide-20140604.x86_64"
    dest = "EC2-eu-west-1"
    ami_id = 'ami-1234fda'
    virt_type = 'HVM'
    vol_type = 'gp2'
    expected_subti = "{0} finished uploading to {1} ({2}, {3}, {4})".format(
            image_name, dest, ami_id, virt_type, vol_type)
    expected_link = None
    expected_icon = 'https://apps.fedoraproject.org/img/icons/fedimg.png'
    expected_secondary_icon = None
    expected_packages = set([])
    expected_usernames = set([])
    expected_objects = set(['image/upload/completed'])
    msg = {
        u'i': 1,
        u'msg': {
            u'image_url': 'https://kojipkgs.fedoraproject.org//work/'
                          'tasks/5144/6925144/fedora-cloud-base-'
                          'rawhide-20140604.x86_64.raw.xz',
            u'image_name': 'fedora-cloud-base-rawhide-20140604.x86_64',
            u'destination': 'EC2-eu-west-1',
            u'status': 'completed',
            u'extra': {
                u'id': 'ami-1234fda',
                u'virt_type': 'HVM',
                u'vol_type': 'gp2',
            },
        },
        u'topic': u'org.fedoraproject.stg.fedimg.image.upload',
        u'username': u'fedimg',
        u'timestamp': 1371498303.125771,
    }


class TestImageTestStart(Base):
    """ These messages are published when an image test has started.
        At this point, Fedimg tries to start an instance of a
        image that it registered in the previous step, and check
        to see that it's running properly. """

    expected_title = "fedimg.image.test"
    image_name = "fedora-cloud-base-rawhide-20140604.x86_64"
    dest = "EC2-eu-west-1"
    ami_id = 'ami-1234fda'
    virt_type = 'HVM'
    vol_type = 'gp2'
    expected_subti = "{0} started testing on {1} ({2}, {3}, {4})".format(
            image_name, dest, ami_id, virt_type, vol_type)
    expected_link = None
    expected_icon = 'https://apps.fedoraproject.org/img/icons/fedimg.png'
    expected_secondary_icon = None
    expected_packages = set([])
    expected_usernames = set([])
    expected_objects = set(['image/test/started'])
    msg = {
        u'i': 1,
        u'msg': {
            u'image_url': 'https://kojipkgs.fedoraproject.org//work/'
                          'tasks/5144/6925144/fedora-cloud-base-'
                          'rawhide-20140604.x86_64.raw.xz',
            u'image_name': 'fedora-cloud-base-rawhide-20140604.x86_64',
            u'destination': 'EC2-eu-west-1',
            u'status': 'started',
            u'extra': {
                u'id': 'ami-1234fda',
                u'virt_type': 'HVM',
                u'vol_type': 'gp2',
            },
        },
        u'topic': u'org.fedoraproject.stg.fedimg.image.test',
        u'username': u'fedimg',
        u'timestamp': 1371498303.125771,
    }

add_doc(locals())

if __name__ == '__main__':
    unittest.main()
