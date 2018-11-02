import codecs
import json
import os
import sys
from bs4 import BeautifulSoup


def parseSingleBugFile(bugGroupFileName, projectName):
    f = codecs.open(bugGroupFileName, 'r', 'utf-8')
    content = f.read()
    f.close()
    contents = content.split("{\r\n    \"fields\"")
    size = len(contents)
    for index in range(1, size):
        bugReport = '{\r\n    \"fields\"' + contents[index]
        bugReportJson = json.loads(bugReport)
        summary = bugReportJson['issue']['summary']  # 标题
        key = bugReportJson['issue']['key']  # LANG-727
        leftPanel = bugReportJson['panels']['leftPanels']
        leftPanelHtml = leftPanel[0]['html']
        leftPanelSoup = BeautifulSoup(leftPanelHtml, 'html.parser')
        type = leftPanelSoup.find('span', attrs={'id': 'type-val'}).text
        if 'Bug' not in type:
            # 不是bug
            continue
        priority = leftPanelSoup.find('span', attrs={'id': 'priority-val'})
        priority = priority.text.strip() if priority is not None else ''
        resolution = leftPanelSoup.find('span', attrs={'id': 'resolution-val'})
        resolution = resolution.text.strip() if resolution is not None else ''
        fixVersions = leftPanelSoup.find('span', attrs={'id': 'fixVersions-field'})
        fixVersions = fixVersions.text.strip() if fixVersions is not None else ''
        affectsVersions = leftPanelSoup.find('span', attrs={'id': 'versions-field'})
        affectsVersions = affectsVersions.text.strip() if affectsVersions is not None else ''
        components = leftPanelSoup.find('span', attrs={'id': 'components-field'})
        components = components.text.strip() if components is not None else ''
        result = {}
        result['summary'] = summary
        result['key'] = key
        result['priority'] = priority
        result['resolution'] = resolution
        result['fixVersions'] = fixVersions
        result['affectsVersions'] = affectsVersions
        result['components'] = components
        resultDir = 'result/' + projectName
        if not os.path.exists(resultDir):
            os.makedirs(resultDir)
        f = open(resultDir + '/' + key + '.txt', 'w', encoding='utf-8')
        f.write(json.dumps(result, indent=4))
        f.close()


if __name__ == '__main__':
    projectNames = ['HTTPCLIENT', 'SPR', 'LOGGING', 'CLI', 'COLLECTIONS', 'LANG', 'COMMON-IO', 'CODEC', 'LOGBACK',
                    'LOG4J2']
    size = len(projectNames)
    startProjectIndex = int(sys.argv[1])
    startBugGroupIndex = int(sys.argv[2])
    startBugIndex = int(sys.argv[3])
    for projectIndex in range(startProjectIndex, size):
        projectName = projectNames[projectIndex]
        projectPath = projectName + '_dest'
        bugGroups = os.listdir(projectPath)
        bugGroups.sort()  # 0.txt,1.txt...
        bugGroupSize = len(bugGroups)
        print(bugGroupSize)
        print(projectName)
        print(bugGroups)
        # 遍历项目文件夹下的0.txt 1.txt...
        for bugGroupIndex in range(bugGroupSize):
            if startProjectIndex == projectIndex and bugGroupIndex < startBugGroupIndex:
                # 当项目index == 启始项目index 且 bug组Index < 启始bug组Index时，说明这些项目已经解析过
                continue
            bugGroupFileName = projectPath + '/' + bugGroups[bugGroupIndex]
            parseSingleBugFile(bugGroupFileName, projectName)
            print(projectIndex, bugGroupIndex)
