#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2023 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor                                              #
#                                                           #
#      Version: 8.0.1 -                                     #
#                                                           #
#############################################################
#
#
#  @File: cli/register.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Mon Jan  2 15:39:08 CST 2023
#
import logging
import os

from base64 import b64decode, urlsafe_b64encode
from json import loads as json_loads
from string import Template


logger = logging.getLogger('Pyarmor')


def parse_token(data):
    from struct import unpack

    if not data or data.find(' ') == -1:
        return {
            'token': 0,
            'rev': 0,
            'features': 0,
            'licno': 'pyarmor-vax-000000',
            'regname': '',
            'product': '',
            'note': 'This is trial license'
        }

    buf = b64decode(data.split()[0])

    token, value = unpack('II', buf[:8])
    rev, features = value & 0xff, value >> 8
    licno = unpack('20s', buf[16:36]).decode('utf-8')

    pstr = []
    i = 64
    for k in range(4):
        n = buf[i]
        i += 1
        pstr.append(buf[i:i+n].decode('utf-8'))
        i += n

    return {
        'token': token,
        'rev': rev,
        'features': features,
        'licno': licno,
        'machine': pstr[0],
        'regname': pstr[1],
        'product': pstr[2],
        'note': pstr[3],
    }


class Register(object):

    def __init__(self, ctx):
        self.ctx = ctx
        self.notes = []

    def check_args(self, args):
        if args.upgrade and args.keyfile.endswith('.zip'):
            raise RuntimeError('use .txt file to upgrade, not .zip file')

    def _get_old_rcode(self):
        old_license = self.ctx.read_license()
        if not old_license:
            raise RuntimeError('no license file')
        if len(old_license) == 256:
            raise RuntimeError('no old purchased license')
        data = b64decode(old_license)
        i = data.find(b'pyarmor-vax-')
        if i == -1:
            raise RuntimeError('no valid old license')
        return data[i:i+18].decode()

    def regurl(self, ucode, product=None, rcode=None, prepare=False):
        url = self.ctx.cfg['pyarmor']['regurl'] % ucode
        if product:
            url += '&product=' + urlsafe_b64encode(product.encode('utf-8'))
        if rcode:
            url += '&rcode=' + rcode
        if prepare:
            url += '&prepare=1'
        return url

    def update_license_token(self):
        from .core import Pytransform3
        return Pytransform3.get_license_info(self.ctx)

    @property
    def license_info(self):
        return parse_token(self.ctx.read_token())

    def _license_type(self, info):
        return 'basic' if info['features'] == 1 else \
            'pro' if info['features'] == 7 else \
            'trial' if info['token'] == 0 else 'unknown'

    def _license_to(self, info):
        name = info['regname']
        product = info['product']
        return '%s - %s' % (name, product) if name and product else \
            '' if not name else '%s - %s' % (name, 'non-profits')

    def parse_keyfile(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                marker = 'Dear '
                if line.startswith(marker):
                    regname = line[len(marker):].strip(' ,')
                    break

            for line in f:
                line = line.strip()
                if len(line) == 192 and line.find(' ') == -1:
                    return regname, line

        raise RuntimeError('no registration code found in %s' % filename)

    def register_regfile(self, regfile, clean=True):
        from zipfile import ZipFile

        path = self.ctx.home_path
        with ZipFile(regfile, 'r') as f:
            for item in ('license.lic', '.pyarmor_capsule.zip'):
                logger.debug('extracting %s' % item)
                f.extract(item, path=path)

        if clean:
            self._remove_token()

    def __str__(self):
        '''$advanced

Notes
* Internet connection is required to verify Pyarmor license
$notes
'''

        info = self.license_info
        lictype = self._license_type(info)

        fmt = '%-16s: %s'
        lines = [
            fmt % ('License Type', 'pyarmor-' + lictype),
            fmt % ('License No.', info['licno']),
            fmt % ('License To', self._license_to(info)),
            '',
        ]

        bccmode = info['features'] & 2
        rftmode = info['features'] & 4
        advanced = [
            fmt % ('BCC Mode', 'Yes' if bccmode else 'No'),
            fmt % ('RFT Mode', 'Yes' if rftmode else 'No'),
        ]
        if lictype == 'trial':
            self.notes.append(
                '* Trial license can\'t obfuscate big script and mix str'
            )

        lines.append(Template(self.__str__.__doc__).substitute(
            advanced='\n'.join(advanced),
            notes='\n'.join(self.notes),
        ))

        return '\n'.join(lines)


upgrade_to_basic_info = Template('''
You are about to upgrade old Pyarmor license to Pyarmor Basic
License for Pyarmor 8.0+

The original license no: $rcode

The upgraded license information will be''')

upgrade_to_pro_info = Template('''
You are about to upgrade old Pyarmor license to Pyarmor Pro
License for Pyarmor 8.0+

The original license no: $rcode

The upgraded license information will be''')


class WebRegister(Register):

    def _send_request(self, url, timeout=6.0):
        from urllib.request import urlopen
        from ssl import _create_unverified_context
        context = _create_unverified_context()
        return urlopen(url, None, timeout, context=context)

    def _remove_token(self):
        if os.path.exists(self.ctx.license_token):
            logger.debug('remove old token')
            os.remove(self.ctx.license_token)

    def prepare(self, keyfile, product, upgrade=False):
        reginfo = self.parse_keyfile(keyfile)
        logger.info('prepare "%s"', keyfile)

        rcode = self._get_old_rcode() if upgrade else None
        url = self.regurl(reginfo[1], rcode=rcode, prepare=True)
        logger.debug('url: %s', url)

        logger.info('query key file from server')
        res = self._send_request(url)
        if not res:
            raise RuntimeError('no response from license server')
        if res.code != 200:
            raise RuntimeError(res.read().decode('utf-8'))

        info = json_loads(res.read(), encoding='utf-8')
        if info['product'] not in ('', 'TBD') and product != info['product']:
            raise RuntimeError('product name has been set to "%s"',
                               info['product'])
        if info['product'] in ('', 'TBD'):
            info['product'] = product if product else 'non-profits'

        lines = []
        if upgrade:
            if info['upgrade']:
                lines.append(upgrade_to_pro_info.substitute(rcode=rcode))
            else:
                lines.append(upgrade_to_basic_info.substitute(rcode=rcode))
        else:
            if info['lictype'] not in ('BASIC', 'PRO'):
                raise RuntimeError('unknown license type %s' % info['lictype'])
            lines.append('This license registration information will be')

        fmt = '%-16s: %s'
        lines.extend([
            '',
            fmt % ('License Type', 'pyarmor-' + info['lictype'].lower()),
            fmt % ('License Owner', info['regname']),
            fmt % ('Bind Product', info['product']),
            '',
        ])
        if info['product'] == 'non-profits':
            lines.append('This license is about to be ussd for non-profits')

        lines.extend(['', ''])
        return '\n'.join(lines)

    def upgrade(self, keyfile, product):
        logger.info('process upgrading file "%s"', keyfile)
        reginfo = self.parse_keyfile(keyfile)

        rcode = self._get_old_rcode()
        logger.info('old license no: %s', rcode)

        url = self.regurl(reginfo[1], product=product, rcode=rcode)
        logger.debug('url: %s', url)

        logger.info('send upgrade request to server')
        res = self._send_request(url)

        if not res:
            raise RuntimeError('no response from license server')
        if res.code != 200:
            raise RuntimeError(res.read().decode())

        logger.info('update license token')
        self.update_license_token()
        logger.info('The upgraded license information:\n\n%s', str(self))

    def register(self, keyfile, product):
        if keyfile.endswith('.zip'):
            logger.info('register "%s"', keyfile)
            self.register_regfile(keyfile)
            return

        logger.info('process activation file "%s"', keyfile)
        reginfo = self.parse_keyfile(keyfile)

        url = self.regurl(reginfo[1], product=product)
        logger.debug('url: %s', url)

        logger.info('send register request to server')
        res = self._send_request(url)
        regfile = self._handle_response(res)

        logger.info('register "%s"', regfile)
        self.register_regfile(regfile)

        logger.info('update license token')
        self.update_license_token()

        self.notes = (
            '* Please backup regfile "%s" carefully, and '
            'use this file for next registration' % regfile,
            '* Do not use "%s" again, it may not work' % keyfile,
        )
        logger.info('This license registration information:\n\n%s', str(self))

    def _handle_response(self, res):
        if res and res.code == 200:
            dis = res.headers.get('Content-Disposition')
            filename = dis.split('"')[1] if dis else 'pyarmor-regfile.zip'
            logger.info('write registration file "%s"', filename)
            with open(filename, 'wb') as f:
                f.write(res.read())
            return filename

        elif res:
            raise RuntimeError(res.read().decode('utf-8'))

        raise RuntimeError('no response from license server')
