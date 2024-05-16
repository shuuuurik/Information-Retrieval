import requests
import os
import shutil
from requests.adapters import HTTPAdapter, Retry

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
s.mount("http://", HTTPAdapter(max_retries=retries))

headers = {
    "Connection": "Keep-Alive",
    "User-Agent": "M"
}

def downloadFiles(startNum, endNum):
    while (startNum <= endNum):
        downloadBooks(startNum, min(startNum + 100, endNum))
        startNum += 101

def downloadBooks(startNum, endNum):
    numberEBook = startNum - 1

    while (numberEBook < endNum):
        numberEBook += 1
        try:
            response = s.get(f"https://www.gutenberg.org/cache/epub/{numberEBook}/pg{numberEBook}.txt", headers=headers)
            if (response.status_code != 200):
                print("404")
                continue
        except:
            print("Exception")
            continue
        
        numberEBookWithZeros = str(numberEBook).zfill(5)
        dirPath = os.path.join(os.getcwd(), f"eBooks/eBook_{numberEBookWithZeros}")
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        tmpFile = os.path.join(dirPath, "tmp.txt")
        with open(tmpFile, 'wb') as f:
            f.write(response.content)

        with open(tmpFile, 'r', encoding="UTF-8") as f:
            data = f.read()

        # tmpFile = os.path.join(dirPath, "tmp.txt")
        # try:
        #     wget.download(f"https://www.gutenberg.org/cache/epub/{numberEBook}/pg{numberEBook}.txt", tmpFile)
        # except:
        #     print("404")
        #     shutil.rmtree(dirPath)
        #     continue
        # with open(tmpFile, 'r', encoding="UTF-8") as f:
        #     data = f.read()

        os.remove(tmpFile)

        languageIndex = data.find("Language:")
        data = data[languageIndex:]

        endParagraphIndex = data.find("\n")
        languageStr = data[:endParagraphIndex]
        if (languageStr != "Language: English"):
            print(languageStr)
            # print("Pomoika")
            os.rmdir(dirPath)
            continue
        startIndex = data.find("*** START OF THE PROJECT GUTENBERG EBOOK")
        data = data[startIndex:]

        downloadBookBySegments(dirPath, data)

def downloadBookBySegments(dirPath, data):
    i = 1
    while(True):
            strPortion = data[:2000]
            if (strPortion.strip() == "" or (i == 1 and strPortion.find("Sorry, but this file is broken and has been removed") != -1)):
                shutil.rmtree(dirPath)
                break
            data = data[2000:]
            endIndex = strPortion.find("*** END OF THE PROJECT GUTENBERG EBOOK")
            if (endIndex != -1):
                strPortion = strPortion[:endIndex].strip()
                if (len(strPortion) > 0):
                    file = os.path.join(dirPath, f"{i}.txt".zfill(10))
                    if not os.path.exists(file):
                        with open(file, "w", encoding="UTF-8") as f:
                            f.write(strPortion)
                break
            else:
                endParagraphIndex = data.find("\n\n")
                strPortion = (strPortion + data[:endParagraphIndex]).strip()
                data = data[endParagraphIndex:]
                if (len(strPortion) > 0):
                    file = os.path.join(dirPath, f"{i}.txt".zfill(10))
                    if not os.path.exists(file):
                        with open(file, "w", encoding="UTF-8") as f:
                            f.write(strPortion)
                i += 1

if __name__ == "__main__":
    downloadFiles(1, 10000)