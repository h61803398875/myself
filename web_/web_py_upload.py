# -*- coding:utf8 -*-

import subprocess
import time

import web

# web.config.debug = False

urls = (
    '/', 'Index',
    '/wpa', 'WPA',
    '/tsf', 'TSF'
)

usage = """
uasge:
    /tsf    启/停/查看 PHP的TSF服务
    /wpa    添加WPA页面到不同测试环境
"""


class Index:
    def GET(self):
        i = web.input(m=None)

        if i.m == "pwd":
            log_file_name = "/data/home/chazzhuang/test_svr_mgmt/log/pwd_chg." + time.strftime("%Y-%m-%d") + ".log"
            ret = subprocess.check_output("cat " + log_file_name, shell=True)
        elif i.m == "chpwd":
            cmd = "/data/home/chazzhuang/test_svr_mgmt/change.svr.pwd.sh change_pwd >> /data/home/chazzhuang/test_svr_mgmt/run.log"
            ret = subprocess.check_output(cmd, shell=True)
        else:
            ret = usage

        return ret


class TSF:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return """<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"><title>TSF</title></head><body>
<form method="POST" enctype="multipart/form-data" action="">

<label>method:</label>
<select name="method">
<option value="list">list</option>
<option value="stop">stop</option>
<option value="start">start</option>
</select>
<br/>

<label>module:</label>
<input type="text" name="module" />

<input type="submit" />
</form>
</body></html>"""

    def POST(self):

        ret = "Done"
        svr_ip = "10.219.134.31"

        i = web.input(method=None, module=None)

        if i.method == "stop" or i.method == "start":
            cmd = "ssh root@{0} 'cd /usr/local/services/TSF2-1.0/bin;./tsf {1} {2}'".format(svr_ip, i.module,
                                                                                            i.method)
            try:
                ret = subprocess.check_output(cmd, shell=True)
            except Exception, e:
                ret = e
        elif i.method == "list":
            cmd = "ssh root@{0} 'cd /usr/local/services/TSF2-1.0/bin;./tsf list'".format(svr_ip)
            try:
                ret = subprocess.check_output(cmd, shell=True)
            except Exception, e:
                ret = e

        else:
            ret = usage

        return ret


class WPA:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return """<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"><title>WPA</title></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="wpa_file" />
<br/>
<label>env:</label>
<select name="env">
<option value="trunk">trunk</option>
<option value="branch_e">branch_e</option>
<option value="branch_d">branch_d</option>
</select>

<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(env=None, wpa_file={})

        ret = "Done"
        svr_ip = "10.213.170.99"

        filepath = x.wpa_file.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
        filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)

        wpa_file_path = '/data/home/chazzhuang/test_svr_mgmt/' + filename
        with open(wpa_file_path, 'w') as fout:
            fout.write(x.wpa_file.file.read())  # writes the uploaded file to the newly created file.

        if x.env == "branch_e":
            file_dest_path = "/data/web_deployment/htdocs/hengine/qidian"
        elif x.env == "branch_d":
            file_dest_path = "/data/web_deployment/htdocs/hengine/qidian_branch_d"
        else:
            file_dest_path = "/data/web_deployment/htdocs/hengine/qidian_branch_e"

        cmd = "scp {0} root@{1}:{2}".format(wpa_file_path, svr_ip, file_dest_path)
        try:
            ret = subprocess.check_output(cmd, shell=True)
        except Exception, e:
            ret = e

        cmd = "rm -rf {0}".format(wpa_file_path)
        try:
            ret = subprocess.check_output(cmd, shell=True)
        except Exception, e:
            ret = e

        return ret


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
