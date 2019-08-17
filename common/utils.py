#coding:utf-8
import hashlib
import urllib
import socket


def handler_paramer(request):
    header_data = request.META
    header_string = ''
    for k,v in header_data.items():
        if k.startswith('HTTP_'):
            key = k.replace('HTTP_', '').replace('_', '-')
            if key in ['ACCEPT', 'USER-AGENT', 'CONNECTION', 'ACCEPT-ENCODING', 'HOST', 'ACCEPT-LANGUAGE']:
                pass
            else:
                header_string += ' -H "%s:%s"'%(key, v)

    if request.method == 'POST':
        request_data = request.POST.dict()
        request_string = urllib.urlencode(request_data)
        request_string = urllib.unquote(request_string)
        reqeust_url = 'http://%s%s'%(header_data['HTTP_HOST'], header_data['PATH_INFO'])
        request_cmd = 'curl -d "%s" %s %s'%(request_string, header_string, reqeust_url)
    else:
        request_data = request.GET.dict()
        request_string = urllib.urlencode(request_data)
        request_string = urllib.unquote(request_string)
        if request_string:
            reqeust_url = 'http://%s%s?%s'%(header_data['HTTP_HOST'], header_data['PATH_INFO'], request_string)
        else:
            reqeust_url = 'http://%s%s'%(header_data['HTTP_HOST'], header_data['PATH_INFO'])

        request_cmd = 'curl %s %s'%( header_string, reqeust_url)
    return request_cmd


def get_md5sum(text):
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]



def gen_tags(tags):
    ret = {}
    for i in tags.split(','):
        key = i.split('=')[0]
        value = i.split('=')[1]
        ret[key] = value
    return ret



def serialize_number(n, step):  #[1...9]  ->  [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    data = []
    temp = []
    for i in xrange(1, n + 1):
        if i % step != 0:
            temp.append(i)
            if i == n:
                data.append(temp)
        else:
            temp.append(i)
            data.append(temp)
            temp = []

    return data