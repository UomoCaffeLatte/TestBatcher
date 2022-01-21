import templates as tplate
import concurrent.futures
from typing import Iterable, Callable
import pandas as pd
from pathlib import Path

class Batcher:
    def __init__(self, fileName:str, saveFilePath:str = ".") -> None:
        self.fileName = fileName
        self.filePath = saveFilePath
        self.fullPath = f"{saveFilePath}/{self.fileName}.xlsx"
        self.__CheckFileNameAndPath()
        self.latestID = 0
        self.testCases: dict = {}
        self.__results = {}
    
    def __CheckFileNameAndPath(self):
        if not Path(self.filePath).is_dir(): raise ValueError("Directory does not exist.")
        if Path(self.fullPath).is_file(): raise ValueError("File with filename already exists, cannot override files for saftey reasons.")

    def __GenerateID(self) -> int:
        self.latestID += 1
        return self.latestID

    def CreateTestCase(self, function:Callable, testName:str) -> tplate.TestBase:
        id = self.__GenerateID()
        self.testCases[id] = tplate.TestBase(function, id, testName)
        return self.testCases[id]

    def __Save(self) -> None:
        writer = pd.ExcelWriter(self.fullPath, engine="xlsxwriter")
        try:
            for testID in self.__results:
                testResult = self.__results[testID]
                # # generate input headers dict
                inputHeaders = []
                inputArgNames = self.testCases[testID].func.args
                for i in range(0, len(testResult)):
                    temp = {}
                    for j in range(0, len(inputArgNames)):
                        temp[f"i:{inputArgNames[j]}"] = self.testCases[testID].tests[i][j]
                    inputHeaders.append(temp)
                # append input headers to results
                for i in range(0, len(testResult)):
                    testResult[i] = {**inputHeaders[i], **testResult[i]}
                # save
                dF = pd.DataFrame(testResult)
                dF.to_excel(writer, sheet_name=self.testCases[testID].name)
        except:
            print("Something went wrong in the save function!")
        writer.save()

    def Run(self) -> None:
        for testCase in self.testCases:
            testCaseResult = self.__ProcessPoolExecutor(self.testCases[testCase])
            self.__results[self.testCases[testCase].ID] = testCaseResult
        self.__Save()

    def __Args2Map(self, args):
        # convert list of test args to map format for PPE.
        map = []
        for i in range(0, len(args[0])):
            temp = []
            for arg in args:
                temp.append(arg[i])
            map.append(temp)
        return map

    def __ProcessPoolExecutor(self, testCase:tplate.TestBase) -> dict:
        # multi procesing tests.
        results = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            process = executor.map(testCase.func.callable, *self.__Args2Map(testCase.tests))
            for result in process:
                results.append(result)
        return results

def tester(a, c) -> dict:
        return {"alo":6, "ded":10}
    

if __name__ == "__main__":
    b = Batcher("test")
    
    t = b.CreateTestCase(tester, "test1")
    t.AddTest(10, 1)
    t.AddTest(10, 1)

    t = b.CreateTestCase(tester, "test2")
    t.AddTest(10, 1)
    t.AddTest(10, 1)
    
    b.Run()