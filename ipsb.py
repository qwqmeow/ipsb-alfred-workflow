#!/usr/bin/env python
# coding=utf-8

import sys
import json
from workflow import Workflow, ICON_INFO, ICON_ERROR, web
from commands import getoutput
import socket
from urlparse import urlparse

ISO_CODE_TO_NAME = {
    u'AD': u'\u5b89\u9053\u5c14',
    u'AE': u'\u963f\u8054\u914b',
    u'AF': u'\u963f\u5bcc\u6c57',
    u'AG': u'\u5b89\u63d0\u74dc\u548c\u5df4\u5e03\u8fbe',
    u'AI': u'\u5b89\u572d\u62c9',
    u'AL': u'\u963f\u5c14\u5df4\u5c3c\u4e9a',
    u'AM': u'\u4e9a\u7f8e\u5c3c\u4e9a',
    u'AN': u'\u8377\u5c5e\u5b89\u7684\u5217\u65af',
    u'AO': u'\u5b89\u54e5\u62c9',
    u'AQ': u'\u5357\u6781\u6d32',
    u'AR': u'\u963f\u6839\u5ef7',
    u'AS': u'\u7f8e\u5c5e\u8428\u6469\u4e9a',
    u'AT': u'\u5965\u5730\u5229',
    u'AU': u'\u6fb3\u5927\u5229\u4e9a',
    u'AW': u'\u963f\u9c81\u5df4',
    u'AX': u'\u5965\u5170\u7fa4\u5c9b',
    u'AZ': u'\u963f\u585e\u62dc\u7586',
    u'BA': u'\u6ce2\u9ed1',
    u'BB': u'\u5df4\u5df4\u591a\u65af',
    u'BD': u'\u5b5f\u52a0\u62c9\u56fd',
    u'BE': u'\u6bd4\u5229\u65f6',
    u'BF': u'\u5e03\u57fa\u7eb3\u6cd5\u7d22',
    u'BG': u'\u4fdd\u52a0\u5229\u4e9a',
    u'BH': u'\u5df4\u6797',
    u'BI': u'\u5e03\u9686\u8fea',
    u'BJ': u'\u8d1d\u5b81',
    u'BM': u'\u767e\u6155\u5927',
    u'BN': u'\u6587\u83b1',
    u'BO': u'\u73bb\u5229\u7ef4\u4e9a',
    u'BR': u'\u5df4\u897f',
    u'BS': u'\u5df4\u54c8\u9a6c',
    u'BT': u'\u4e0d\u4e39',
    u'BV': u'\u5e03\u7ef4\u5c9b',
    u'BW': u'\u535a\u8328\u74e6\u7eb3',
    u'BY': u'\u767d\u4fc4\u7f57\u65af',
    u'BZ': u'\u4f2f\u5229\u5179',
    u'CA': u'\u52a0\u62ff\u5927',
    u'CC': u'\u79d1\u79d1\u65af\uff08\u57fa\u6797\uff09\u7fa4\u5c9b',
    u'CD': u'\u521a\u679c\uff08\u91d1\uff09',
    u'CF': u'\u4e2d\u975e',
    u'CG': u'\u521a\u679c\uff08\u5e03\uff09',
    u'CH': u'\u745e\u58eb',
    u'CI': u'\u79d1\u7279\u8fea\u74e6',
    u'CK': u'\u5e93\u514b\u7fa4\u5c9b',
    u'CL': u'\u667a\u5229',
    u'CM': u'\u5580\u9ea6\u9686',
    u'CN': u'\u4e2d\u56fd',
    u'CO': u'\u54e5\u4f26\u6bd4\u4e9a',
    u'CR': u'\u54e5\u65af\u8fbe\u9ece\u52a0',
    u'CU': u'\u53e4\u5df4',
    u'CV': u'\u4f5b\u5f97\u89d2',
    u'CX': u'\u5723\u8bde\u5c9b',
    u'CY': u'\u585e\u6d66\u8def\u65af',
    u'CZ': u'\u6377\u514b',
    u'DE': u'\u5fb7\u56fd',
    u'DJ': u'\u5409\u5e03\u63d0',
    u'DK': u'\u4e39\u9ea6',
    u'DM': u'\u591a\u7c73\u5c3c\u514b',
    u'DO': u'\u591a\u7c73\u5c3c\u52a0',
    u'DZ': u'\u963f\u5c14\u53ca\u5229\u4e9a',
    u'EC': u'\u5384\u74dc\u591a\u5c14',
    u'EE': u'\u7231\u6c99\u5c3c\u4e9a',
    u'EG': u'\u57c3\u53ca',
    u'EH': u'\u897f\u6492\u54c8\u62c9',
    u'ER': u'\u5384\u7acb\u7279\u91cc\u4e9a',
    u'ES': u'\u897f\u73ed\u7259',
    u'ET': u'\u57c3\u585e\u4fc4\u6bd4\u4e9a',
    u'FI': u'\u82ac\u5170',
    u'FJ': u'\u6590\u6d4e',
    u'FK': u'\u798f\u514b\u5170\u7fa4\u5c9b\uff08\u9a6c\u5c14\u7ef4\u7eb3\u65af\uff09',
    u'FM': u'\u5bc6\u514b\u7f57\u5c3c\u897f\u4e9a\u8054\u90a6',
    u'FO': u'\u6cd5\u7f57\u7fa4\u5c9b',
    u'FR': u'\u6cd5\u56fd',
    u'GA': u'\u52a0\u84ec',
    u'GB': u'\u82f1\u56fd',
    u'GD': u'\u683c\u6797\u7eb3\u8fbe',
    u'GE': u'\u683c\u9c81\u5409\u4e9a',
    u'GF': u'\u6cd5\u5c5e\u572d\u4e9a\u90a3',
    u'GG': u'\u683c\u6069\u897f\u5c9b',
    u'GH': u'\u52a0\u7eb3',
    u'GI': u'\u76f4\u5e03\u7f57\u9640',
    u'GL': u'\u683c\u9675\u5170',
    u'GM': u'\u5188\u6bd4\u4e9a',
    u'GN': u'\u51e0\u5185\u4e9a',
    u'GP': u'\u74dc\u5fb7\u7f57\u666e',
    u'GQ': u'\u8d64\u9053\u51e0\u5185\u4e9a',
    u'GR': u'\u5e0c\u814a',
    u'GS': u'\u5357\u4e54\u6cbb\u4e9a\u5c9b\u548c\u5357\u6851\u5fb7\u97e6\u5947\u5c9b',
    u'GT': u'\u5371\u5730\u9a6c\u62c9',
    u'GU': u'\u5173\u5c9b',
    u'GW': u'\u51e0\u5185\u4e9a\u6bd4\u7ecd',
    u'GY': u'\u572d\u4e9a\u90a3',
    u'HK': u'\u9999\u6e2f',
    u'HM': u'\u8d6b\u5fb7\u5c9b\u548c\u9ea6\u514b\u5510\u7eb3\u5c9b',
    u'HN': u'\u6d2a\u90fd\u62c9\u65af',
    u'HR': u'\u514b\u7f57\u5730\u4e9a',
    u'HT': u'\u6d77\u5730',
    u'HU': u'\u5308\u7259\u5229',
    u'ID': u'\u5370\u5ea6\u5c3c\u897f\u4e9a',
    u'IE': u'\u7231\u5c14\u5170',
    u'IL': u'\u4ee5\u8272\u5217',
    u'IM': u'\u82f1\u56fd\u5c5e\u5730\u66fc\u5c9b',
    u'IN': u'\u5370\u5ea6',
    u'IO': u'\u82f1\u5c5e\u5370\u5ea6\u6d0b\u9886\u5730',
    u'IQ': u'\u4f0a\u62c9\u514b',
    u'IR': u'\u4f0a\u6717',
    u'IS': u'\u51b0\u5c9b',
    u'IT': u'\u610f\u5927\u5229',
    u'JE': u'\u6cfd\u897f\u5c9b',
    u'JM': u'\u7259\u4e70\u52a0',
    u'JO': u'\u7ea6\u65e6',
    u'JP': u'\u65e5\u672c',
    u'KE': u'\u80af\u5c3c\u4e9a',
    u'KG': u'\u5409\u5c14\u5409\u65af\u65af\u5766',
    u'KH': u'\u67ec\u57d4\u5be8',
    u'KI': u'\u57fa\u91cc\u5df4\u65af',
    u'KM': u'\u79d1\u6469\u7f57',
    u'KN': u'\u5723\u57fa\u8328\u548c\u5c3c\u7ef4\u65af',
    u'KP': u'\u671d\u9c9c',
    u'KR': u'\u97e9\u56fd',
    u'KW': u'\u79d1\u5a01\u7279',
    u'KY': u'\u5f00\u66fc\u7fa4\u5c9b',
    u'KZ': u'\u54c8\u8428\u514b\u65af\u5766',
    u'LA': u'\u8001\u631d',
    u'LB': u'\u9ece\u5df4\u5ae9',
    u'LC': u'\u5723\u5362\u897f\u4e9a',
    u'LI': u'\u5217\u652f\u6566\u58eb\u767b',
    u'LK': u'\u65af\u91cc\u5170\u5361',
    u'LR': u'\u5229\u6bd4\u91cc\u4e9a',
    u'LS': u'\u83b1\u7d22\u6258',
    u'LT': u'\u7acb\u9676\u5b9b',
    u'LU': u'\u5362\u68ee\u5821',
    u'LV': u'\u62c9\u8131\u7ef4\u4e9a',
    u'LY': u'\u5229\u6bd4\u4e9a',
    u'MA': u'\u6469\u6d1b\u54e5',
    u'MC': u'\u6469\u7eb3\u54e5',
    u'MD': u'\u6469\u5c14\u591a\u74e6',
    u'ME': u'\u9ed1\u5c71',
    u'MG': u'\u9a6c\u8fbe\u52a0\u65af\u52a0',
    u'MH': u'\u9a6c\u7ecd\u5c14\u7fa4\u5c9b',
    u'MK': u'\u524d\u5357\u9a6c\u5176\u987f',
    u'ML': u'\u9a6c\u91cc',
    u'MM': u'\u7f05\u7538',
    u'MN': u'\u8499\u53e4',
    u'MO': u'\u6fb3\u95e8',
    u'MP': u'\u5317\u9a6c\u91cc\u4e9a\u7eb3',
    u'MQ': u'\u9a6c\u63d0\u5c3c\u514b',
    u'MR': u'\u6bdb\u5229\u5854\u5c3c\u4e9a',
    u'MS': u'\u8499\u7279\u585e\u62c9\u7279',
    u'MT': u'\u9a6c\u8033\u4ed6',
    u'MU': u'\u6bdb\u91cc\u6c42\u65af',
    u'MV': u'\u9a6c\u5c14\u4ee3\u592b',
    u'MW': u'\u9a6c\u62c9\u7ef4',
    u'MX': u'\u58a8\u897f\u54e5',
    u'MY': u'\u9a6c\u6765\u897f\u4e9a',
    u'MZ': u'\u83ab\u6851\u6bd4\u514b',
    u'NA': u'\u7eb3\u7c73\u6bd4\u4e9a',
    u'NC': u'\u65b0\u5580\u91cc\u591a\u5c3c\u4e9a',
    u'NE': u'\u5c3c\u65e5\u5c14',
    u'NF': u'\u8bfa\u798f\u514b\u5c9b',
    u'NG': u'\u5c3c\u65e5\u5229\u4e9a',
    u'NI': u'\u5c3c\u52a0\u62c9\u74dc',
    u'NL': u'\u8377\u5170',
    u'NO': u'\u632a\u5a01',
    u'NP': u'\u5c3c\u6cca\u5c14',
    u'NR': u'\u7459\u9c81',
    u'NU': u'\u7ebd\u57c3',
    u'NZ': u'\u65b0\u897f\u5170',
    u'OM': u'\u963f\u66fc',
    u'PA': u'\u5df4\u62ff\u9a6c',
    u'PE': u'\u79d8\u9c81',
    u'PF': u'\u6cd5\u5c5e\u6ce2\u5229\u5c3c\u897f\u4e9a',
    u'PG': u'\u5df4\u5e03\u4e9a\u65b0\u51e0\u5185\u4e9a',
    u'PH': u'\u83f2\u5f8b\u5bbe',
    u'PK': u'\u5df4\u57fa\u65af\u5766',
    u'PL': u'\u6ce2\u5170',
    u'PM': u'\u5723\u76ae\u57c3\u5c14\u548c\u5bc6\u514b\u9686',
    u'PN': u'\u76ae\u7279\u51ef\u6069',
    u'PR': u'\u6ce2\u591a\u9ece\u5404',
    u'PS': u'\u5df4\u52d2\u65af\u5766',
    u'PT': u'\u8461\u8404\u7259',
    u'PW': u'\u5e15\u52b3',
    u'PY': u'\u5df4\u62c9\u572d',
    u'QA': u'\u5361\u5854\u5c14',
    u'RE': u'\u7559\u5c3c\u6c6a',
    u'RO': u'\u7f57\u9a6c\u5c3c\u4e9a',
    u'RS': u'\u585e\u5c14\u7ef4\u4e9a',
    u'RU': u'\u4fc4\u7f57\u65af\u8054\u90a6',
    u'RW': u'\u5362\u65fa\u8fbe',
    u'SA': u'\u6c99\u7279\u963f\u62c9\u4f2f',
    u'SB': u'\u6240\u7f57\u95e8\u7fa4\u5c9b',
    u'SC': u'\u585e\u820c\u5c14',
    u'SD': u'\u82cf\u4e39',
    u'SE': u'\u745e\u5178',
    u'SG': u'\u65b0\u52a0\u5761',
    u'SH': u'\u5723\u8d6b\u52d2\u62ff',
    u'SI': u'\u65af\u6d1b\u6587\u5c3c\u4e9a',
    u'SJ': u'\u65af\u74e6\u5c14\u5df4\u5c9b\u548c\u626c\u9a6c\u5ef6\u5c9b',
    u'SK': u'\u65af\u6d1b\u4f10\u514b',
    u'SL': u'\u585e\u62c9\u5229\u6602',
    u'SM': u'\u5723\u9a6c\u529b\u8bfa',
    u'SN': u'\u585e\u5185\u52a0\u5c14',
    u'SO': u'\u7d22\u9a6c\u91cc',
    u'SR': u'\u82cf\u91cc\u5357',
    u'ST': u'\u5723\u591a\u7f8e\u548c\u666e\u6797\u897f\u6bd4',
    u'SV': u'\u8428\u5c14\u74e6\u591a',
    u'SY': u'\u53d9\u5229\u4e9a',
    u'SZ': u'\u65af\u5a01\u58eb\u5170',
    u'TC': u'\u7279\u514b\u65af\u548c\u51ef\u79d1\u65af\u7fa4\u5c9b',
    u'TD': u'\u4e4d\u5f97',
    u'TF': u'\u6cd5\u5c5e\u5357\u90e8\u9886\u5730',
    u'TG': u'\u591a\u54e5',
    u'TH': u'\u6cf0\u56fd',
    u'TJ': u'\u5854\u5409\u514b\u65af\u5766',
    u'TK': u'\u6258\u514b\u52b3',
    u'TL': u'\u4e1c\u5e1d\u6c76',
    u'TM': u'\u571f\u5e93\u66fc\u65af\u5766',
    u'TN': u'\u7a81\u5c3c\u65af',
    u'TO': u'\u6c64\u52a0',
    u'TR': u'\u571f\u8033\u5176',
    u'TT': u'\u7279\u7acb\u5c3c\u8fbe\u548c\u591a\u5df4\u54e5',
    u'TV': u'\u56fe\u74e6\u5362',
    u'TW': u'\u53f0\u6e7e',
    u'TZ': u'\u5766\u6851\u5c3c\u4e9a',
    u'UA': u'\u4e4c\u514b\u5170',
    u'UG': u'\u4e4c\u5e72\u8fbe',
    u'UM': u'\u7f8e\u56fd\u672c\u571f\u5916\u5c0f\u5c9b\u5c7f',
    u'US': u'\u7f8e\u56fd',
    u'UY': u'\u4e4c\u62c9\u572d',
    u'UZ': u'\u4e4c\u5179\u522b\u514b\u65af\u5766',
    u'VA': u'\u68b5\u8482\u5188',
    u'VC': u'\u5723\u6587\u68ee\u7279\u548c\u683c\u6797\u7eb3\u4e01\u65af',
    u'VE': u'\u59d4\u5185\u745e\u62c9',
    u'VG': u'\u82f1\u5c5e\u7ef4\u5c14\u4eac\u7fa4\u5c9b',
    u'VI': u'\u7f8e\u5c5e\u7ef4\u5c14\u4eac\u7fa4\u5c9b',
    u'VN': u'\u8d8a\u5357',
    u'VU': u'\u74e6\u52aa\u963f\u56fe',
    u'WF': u'\u74e6\u5229\u65af\u548c\u5bcc\u56fe\u7eb3',
    u'WS': u'\u8428\u6469\u4e9a',
    u'YE': u'\u4e5f\u95e8',
    u'YT': u'\u9a6c\u7ea6\u7279',
    u'ZA': u'\u5357\u975e',
    u'ZM': u'\u8d5e\u6bd4\u4e9a',
    u'ZW': u'\u6d25\u5df4\u5e03\u97e6'
}


def flag(code):
    OFFSET = 127397
    country = code
    if country is None:
        return None
    points = [ord(x) + OFFSET for x in country.upper()]
    try:
        return chr(points[0]) + chr(points[1])
    except ValueError:
        return ('\\U%08x\\U%08x' % tuple(points)).decode('unicode-escape')


def get_local_ip():
    return getoutput('ipconfig getifaddr en0')


def ipsb(ip):

    API = 'https://api.ip.sb/geoip/%s' % ip
    try:
        res = web.get(API)
        res.raise_for_status()
        response = res.text
        if response:
            response = json.loads(response)
            pass
        else:
            return
    except Exception:
        ip = None

    result = {}

    result['organization'] = response['organization']

    result['region'] = response['region'] if response.has_key('region') else ''
    result['city'] = response['city'] if response.has_key('city') else ''

    if response['country_code'] == 'AP' and response['longitude'] == 105 and response['latitude'] == 35:
        response['country_code'] = 'TW'

    result['country'] = ISO_CODE_TO_NAME[response['country_code']]

    try:
        result["emoji"] = flag(response['country_code'])
    except KeyError:
        result["emoji"] = u'\U0001F30E'
    
    result["flag"] = 'flags/{}.png'.format(response['country_code'].lower())

    return result


def get_public_ip():
    PUBLIC_IP_QUERY_URL = 'https://api.ip.sb/ip'
    try:
        rt = web.get(PUBLIC_IP_QUERY_URL)
        rt.raise_for_status()
        ip = rt.text.strip()
    except Exception:
        ip = None

    return ip


def resolve_ip_from_dns(urlorhost):
    # resolve ip/domain/url to ip
    host = urlparse(urlorhost).hostname
    if not host:
        host = urlorhost
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        ip = None

    return host, ip


def main(wf):

    param = (wf.args[0] if len(wf.args) else '').strip()
    if param:
        title, ip = resolve_ip_from_dns(param)

    local_ip = get_local_ip()
    public_ip = get_public_ip()
    public_ip_info = ipsb(public_ip)

    if param:
        try:
            ip_info = ipsb(ip)

            wf.add_item(title='IP.SB ' + title,
                        subtitle=ip_info["emoji"] + ip + ' ' + ip_info["country"] +
                        ' '+ip_info["region"] + ' '+public_ip_info['city'] +
                        ' ' + ip_info['organization'],
                        valid=True,
                        icon=ip_info["flag"])
        except:
            wf.add_item(title=param, subtitle='...', icon=ICON_ERROR)

    wf.add_item(title='IP.SB ' + local_ip,
                subtitle=public_ip_info["emoji"] + public_ip + ' ' + public_ip_info["country"] +
                ' '+public_ip_info["region"] + ' '+public_ip_info['city']+' ' +
                public_ip_info['organization'],
                valid=True,
                icon=public_ip_info["flag"])

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
