import json
import os
import sys
import codecs

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    startFileName = sys.argv[1]
    startKeyIndex = int(sys.argv[2])
    sourceDir = 'LOGBACK_source/'
    destDir = 'LOGBACK_dest/'
    # jira
    # url = 'https://issues.apache.org/jira/secure/AjaxIssueAction!default.jspa?issueKey=%s&decorator=none&prefetch=false&shouldUpdateCurrentProject=false&loadFields=false&'
    # spring
    # url = 'https://jira.spring.io/secure/AjaxIssueAction!default.jspa?issueKey=%s&decorator=none&prefetch=false&shouldUpdateCurrentProject=false&loadFields=false&_=1541068516647'
    # LOGBACK
    url = 'https://jira.qos.ch/secure/AjaxIssueAction!default.jspa?issueKey=%s&decorator=none&prefetch=false&shouldUpdateCurrentProject=false&loadFields=false&_=1541138840233'

    files = os.listdir(sourceDir)
    files.sort()
    print(files)
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    for file in files:
        if file < startFileName:
            continue
        filePath = sourceDir + file
        f = codecs.open(filePath, 'r', 'utf-8')
        content = f.read()
        f.close()
        contentJson = json.loads(content)
        keys = contentJson['issueTable']['table']
        f = open(destDir + file, 'a')
        index = -1
        for key in keys:
            index += 1
            if index < startKeyIndex and file == startFileName:
                continue
            issueName = key['key']
            num = issueName.split('-')[1]
            realUrl = url % issueName
            response = requests.get(realUrl)
            response.encoding = 'utf-8'
            # print(response.text)
            f.write(json.dumps(json.loads(response.text), indent=4))
            f.write("\n")
            print(file, index)
        f.close()
