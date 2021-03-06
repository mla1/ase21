from abc import ABC, abstractmethod
from urllib.parse import urlparse, parse_qs
import requests
import logging
import os

startUrl = "https://reset.inso.tuwien.ac.at/ase/assignment/{studentId}/token"
testcaseUrl = "https://reset.inso.tuwien.ac.at/ase/assignment/{studentId}/stage/{stage}/testcase/{testcase}?token={token}"
pdfUrl = "https://reset.inso.tuwien.ac.at/ase/assignment/{studentId}/stage/{stage}/pdf?token={token}"

class StageSolver:

    def __init__(self, sutdentId, stageImplementations=[], outdir="out"):
        if not sutdentId:
            raise ValueError("sutdentId")

        self.studentId = sutdentId
        self.stageImplementations = stageImplementations
        self.outdir = outdir
        self.stage = 1
        self.testcase = 1

        self.tokens = []
        self.currentToken = None
        self.initialTokenUrl = startUrl.format(studentId=self.studentId)
    
    # Download assignemnt for first stage
    def getInitialAssignment():
        logging.info("downloading initial assignment / stage {}".format(self.stage))
        self.currentToken = self.__getToken()
        self.__getAssignment()
    
    # steps are performed in a loop
    #   get token
    #   get pdf
    #   solve stage (get testcase, solve, repeat)
    #   get next token
    def run(self):
        self.currentToken = self.__getToken()

        for stageImpl in self.stageImplementations:
            logging.info("starting stage {}".format(self.stage))
            self.__getAssignment()
            try:
                stageResult = self.__solveStage(stageImpl)

                if not stageResult:
                    # did not solve stage
                    logging.info("stage failed")
                    return
                
                self.currentToken = stageResult
            except Exception as ex:
                logging.error("something went wrong - stopping")
                logging.error(ex)
                return
            
            logging.info("stage {} cleared!".format(self.stage))

        return self.currentToken

    # get testcase
    # solve
    # parse response - return or repeat
    def __solveStage(self, solver):
        if not isinstance(solver, Stage):
            raise TypeError("given stage solutions not of type Stage")
        
        solver: Stage = solver
        while True:
            logging.debug("testcase {}".format(self.testcase))
            testcase = self.__getTestcase()
            answer = solver.solveTask(testcase)
            logging.debug("answer: {}".format(answer))
            response = self.__postAnswer(answer)

            if response.status_code == 202:
                # next testcase or next stage
                logging.debug("testcase solved: {}".format(response.text))
                (s,tc,to) = self.__parseResponse(response)
                logging.debug("s: {}, tc: {}, to: {}".format(s,tc,to))
                if int(s) == self.stage:
                    self.testcase = int(tc)
                    self.currentToken = to
                else:
                    # next stage - reset testcase
                    self.testcase =1
                    return to

            else:
                logging.error("testcase {} failed: {}".format(testcase, response.text))
                return False
        

    #parses stage, testcase and token from success URL
    def __parseResponse(self, response):
        json = response.json()
        linkToNextTask = json['linkToNextTask']
        o = urlparse(linkToNextTask)
        path = o.path.split("/")
        query = o.query
        querydict = parse_qs(query)

        if 'token' in querydict:
            nextToken = querydict['token'].pop()
        else:
            logging.error("something went wrong, no token in valid response")
        
        logging.debug("parsed path: {}".format(path))
        if len(path) > 3:
            nextTestcase = path[-1]
            nextStage = path[-3]

        return (nextStage, nextTestcase, nextToken) 

    # get testcase
    def __getTestcase(self):
        logging.debug("GET testcase {}".format(self.__testcaseUrl()))
        r = requests.get(self.__testcaseUrl())
        res = r.json()
        logging.debug(res)
        return res
    
    #submit answer
    def __postAnswer(self, answer):
        logging.debug("POST answer {} for testcase {}".format(answer, self.testcase))

        r = requests.post(self.__testcaseUrl(), json=answer)
        logging.debug("HTTP {} - {}: {}".format(r.status_code, r.reason, r.text))
        return r

    # queries current assignment document and saves it
    def __getAssignment(self):
        logging.debug("GET assignment pdf {}".format(self.__pdfUrl()))

        r = requests.get(self.__pdfUrl())
        dest = os.path.join(self.outdir, "assignment{}.pdf".format(self.stage))
        with open(dest, "wb") as f:
            f.write(r.content)

        logging.debug("file {} written".format(dest))
    
    # GETs initial token
    def __getToken(self):
        logging.debug("GET initial token")
        r = requests.get(startUrl.format(studentId=self.studentId))
        res = r.json()
        logging.debug(res)
        return res['token']

    def __testcaseUrl(self):
        return testcaseUrl.format(stage=self.stage, studentId=self.studentId, testcase=self.testcase, token=self.currentToken)
    
    def __pdfUrl(self):
        return pdfUrl.format(stage=self.stage, studentId=self.studentId, token=self.currentToken)


    
class Stage(ABC):
    
    @abstractmethod
    def solveTask(testcase):
        pass