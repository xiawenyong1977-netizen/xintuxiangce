# coding:utf-8
# From ywdblog/certbot-letencrypt-wildcardcertificates-alydns-au (Python version)
# Compatible with Python 3; Signature bytes decoded for urlencode.

import base64
import urllib
import hmac
import datetime
import random
import string
import json
import sys
import os

pv = "python2"
if sys.version_info[0] < 3:
    from urllib import quote
    from urllib import urlencode
    import hashlib
else:
    from urllib.parse import quote
    from urllib.parse import urlencode
    from urllib import request
    pv = "python3"


class AliDns:
    def __init__(self, access_key_id, access_key_secret, domain_name):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.domain_name = domain_name

    @staticmethod
    def getDomain(domain):
        domain_parts = domain.split('.')
        if len(domain_parts) > 2:
            dirpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            domainfile = dirpath + "/domain.ini"
            domainarr = []
            if os.path.exists(domainfile):
                with open(domainfile) as f:
                    for line in f:
                        val = line.strip()
                        if val:
                            domainarr.append(val)
            if not domainarr:
                domainarr = ["com", "cn", "net", "org", "top", "io", "me", "com.cn", "net.cn"]
            rootdomain = '.'.join(domain_parts[-(2 if domain_parts[-1] in domainarr else 3):])
            selfdomain = domain.split(rootdomain)[0].rstrip('.')
            return (selfdomain, rootdomain)
        return ("", domain)

    @staticmethod
    def generate_random_str(length=14):
        str_list = [random.choice(string.digits) for i in range(length)]
        return ''.join(str_list)

    @staticmethod
    def percent_encode(str):
        res = quote(str.encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    @staticmethod
    def utc_time():
        return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def sign_string(url_param):
        percent_encode = AliDns.percent_encode
        sorted_url_param = sorted(url_param.items(), key=lambda x: x[0])
        can_string = ''
        for k, v in sorted_url_param:
            can_string += '&' + percent_encode(str(k)) + '=' + percent_encode(str(v))
        string_to_sign = 'GET' + '&' + '%2F' + '&' + percent_encode(can_string[1:])
        return string_to_sign

    @staticmethod
    def access_url(url):
        if pv == "python2":
            f = urllib.urlopen(url)
            result = f.read().decode('utf-8')
            return json.loads(result)
        else:
            req = request.Request(url)
            with request.urlopen(req) as f:
                result = f.read().decode('utf-8')
            return json.loads(result)

    def visit_url(self, action_param):
        common_param = {
            'Format': 'json',
            'Version': '2015-01-09',
            'AccessKeyId': self.access_key_id,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': AliDns.utc_time(),
            'SignatureVersion': '1.0',
            'SignatureNonce': AliDns.generate_random_str(),
            'DomainName': self.domain_name,
        }
        url_param = dict(common_param, **action_param)
        string_to_sign = AliDns.sign_string(url_param)
        hash_bytes = self.access_key_secret + "&"
        if pv == "python2":
            h = hmac.new(hash_bytes, string_to_sign, digestmod=hashlib.sha1)
        else:
            h = hmac.new(hash_bytes.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod='SHA1')
        if pv == "python2":
            signature = base64.encodestring(h.digest()).strip()
        else:
            signature = base64.encodebytes(h.digest()).strip()
            if isinstance(signature, bytes):
                signature = signature.decode('utf-8')
        url_param['Signature'] = signature
        url = 'https://alidns.aliyuncs.com/?' + urlencode(url_param)
        return AliDns.access_url(url)

    def add_domain_record(self, type, rr, value):
        action_param = dict(Action='AddDomainRecord', RR=rr, Type=type, Value=value)
        return self.visit_url(action_param)

    def delete_domain_record(self, id):
        action_param = dict(Action='DeleteDomainRecord', RecordId=id)
        return self.visit_url(action_param)

    def describe_domain_records(self):
        action_param = dict(Action='DescribeDomainRecords', PageNumber='1', PageSize='500')
        return self.visit_url(action_param)


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print("Usage: alydns.py add|clean <CERTBOT_DOMAIN> _acme-challenge <CERTBOT_VALIDATION> <ACCESS_KEY_ID> <ACCESS_KEY_SECRET>")
        sys.exit(1)
    file_name, cmd, certbot_domain, acme_challenge, certbot_validation, ACCESS_KEY_ID, ACCESS_KEY_SECRET = sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
    selfdomain, rootdomain = AliDns.getDomain(certbot_domain)
    if selfdomain:
        rr = acme_challenge + "." + selfdomain
    else:
        rr = acme_challenge
    domain = AliDns(ACCESS_KEY_ID, ACCESS_KEY_SECRET, rootdomain)
    if cmd == "add":
        result = domain.add_domain_record("TXT", rr, certbot_validation)
        if "Code" in result:
            print("aly dns add failed: " + str(result.get("Code", "")) + " " + str(result.get("Message", "")))
            sys.exit(1)
        print("aly dns add ok: " + rr + "." + rootdomain)
    elif cmd == "clean":
        data = domain.describe_domain_records()
        if "Code" in data:
            print("aly dns describe failed: " + str(data.get("Code", "")) + " " + str(data.get("Message", "")))
            sys.exit(1)
        record_list = data.get("DomainRecords", {}).get("Record", [])
        for item in record_list:
            if item.get('RR') == rr:
                domain.delete_domain_record(item['RecordId'])
                print("aly dns deleted: " + item['RecordId'])
        print("aly dns clean ok")
    else:
        print("Unknown cmd: " + cmd)
        sys.exit(1)
