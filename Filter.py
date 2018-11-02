import codecs
import json
import os


def check(priority, resolution, affectsVersion, fixVersions):
    if priority != 'Critical' and priority != 'Major':
        return False
    if resolution != 'Fixed':
        return False
    if affectsVersion == '':
        return False
    if fixVersions == '':
        return False
    return True


if __name__ == '__main__':
    dest = 'filter/'
    baseDir = 'C:\\cs\\pythonspace\\JiraBugSite\\result\\'
    projectNames = os.listdir(baseDir)
    for projectName in projectNames:
        result = {}
        print(projectName)
        projectDir = baseDir + projectName
        bugList = os.listdir(projectDir)
        for bug in bugList:
            bugPath = projectDir + '/' + bug
            f = codecs.open(bugPath, 'r', 'utf-8')
            content = f.read()
            f.close()
            contentJson = json.loads(content)
            priority = contentJson['priority']
            resolution = contentJson['resolution']
            affectsVersion = contentJson['affectsVersions']
            fixVersions = contentJson['fixVersions']
            if check(priority, resolution, affectsVersion, fixVersions):
                aVersions = affectsVersion.split(',')
                for aVersion in aVersions:
                    key = projectName + '_' + aVersion.strip()
                    if key not in result.keys():
                        result[key] = {}
                        result[key]['bugs'] = []
                    result[key]['bugs'].append(contentJson)
        totalSize = 0
        for nameVersion in result.keys():
            tempSize = len(result[nameVersion]['bugs'])
            result[nameVersion]['size'] = tempSize
            totalSize += tempSize
        result['size'] = totalSize
        f = open(dest+projectName+'.txt','w',encoding='utf-8')
        f.write(json.dumps(result,indent=4))
        f.close()