from abc import ABC, abstractmethod
from urllib.parse import urlparse, parse_qs
import requests
import logging
import os

startUrlTemplate = "https://reset.inso.tuwien.ac.at/ase/assignment/{studentId}/token"
testcaseUrlTemplate = "https://reset.inso.tuwien.ac.at/ase/assignment/{studentId}/stage/{stage}/testcase/{testcase}?token={token}"
pdfUrlTemplate = "https://reset.inso.tuwien.ac.at/ase/assignment/{studentId}/stage/{stage}/pdf?token={token}"

class StageSolver:

    def __init__(self, sutdentId, stageImplementations=[], outdir="out"):
        if not sutdentId:
            raise ValueError("sutdentId")

        self.studentId = sutdentId
        self.stageImplementations = stageImplementations
        self.outdir = outdir
        self.stage = 1
        self.testcase = 1

        self.currentToken = None
        self.linkToNextTask = None
        self.initialTokenUrl = startUrlTemplate.format(studentId=self.studentId)

        self.session = requests.Session()
    
    # Download assignemnt for first stage
    def getInitialAssignment(self):
        logging.info("downloading initial assignment / stage {}".format(self.stage))
        self.currentToken = self.__getToken()
        self.__getAssignment(self.studentId, self.stage, self.currentToken)
        
    # steps are performed in a loop
    #   get token
    #   get pdf
    #   solve stage (get testcase, solve, repeat)
    #   get next token
    def run(self):
        self.stage = 1
        self.testcase = 1
        self.currentToken = self.__getToken()
        self.linkToNextTask = self.__testcaseUrl(self.studentId, self.stage, self.testcase, self.currentToken)

        for stageImpl in self.stageImplementations:
            logging.info("starting stage {}".format(self.stage))
            try:
                (nextStageUrl, nextToken) = self.__solveStage(stageImpl, self.linkToNextTask)

                if not nextStageUrl:
                    logging.info("stage failed")
                    return
            except Exception as ex:
                logging.error("something went wrong - stopping")
                logging.error(ex)
                return
            
            self.linkToNextTask = nextStageUrl
            self.currentToken = nextToken
            self.stage = self.stage+1

            logging.info("stage {} cleared! Next url: {}".format(self.stage, self.linkToNextTask))
            self.__getAssignment(self.studentId, self.stage, self.currentToken)

        logging.info("all implemented stages ({}) solved".format(len(self.stageImplementations)))
    

    # get testcase
    # solve
    # parse response - return or repeat
    def __solveStage(self, solver, startUrl):
        if not isinstance(solver, Stage):
            raise TypeError("given stage solutions not of type Stage")
        
        solver: Stage = solver
        url = startUrl
        testcaseNo = 1

        while True:
            testcase = self.__getTestcase(url)
            logging.info("testcase {}: {}".format(testcaseNo, testcase))
            answer = solver.solveTask(testcase)
            logging.info("answer: {}".format(answer))
            response = self.__postAnswer(url, answer)

            if response.status_code == 202:
                # next testcase or next stage
                logging.info("testcase solved")
                logging.debug("response: {}".format(response.text))

                (s,tc,to, nextUrl) = self.__parseResponse(response)
                url = nextUrl
                logging.debug("s: {}, tc: {}, to: {}".format(s,tc,to))

                if int(s) == self.stage:
                    testcase = int(tc)
                else:
                    # stage finished, return url and token for next stage
                    return (url, to)

            else:
                logging.error("testcase {} failed: {}".format(testcase, response.text))
                return (False, False)
        

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
        
        if len(path) > 3:
            nextTestcase = path[-1]
            nextStage = path[-3]

        return (nextStage, nextTestcase, nextToken, linkToNextTask) 

    # get testcase
    def __getTestcase(self, url):
        logging.debug("GET testcase {}".format(url))
        r = self.session.get(url)
        res = r.json()
        logging.debug(res)
        return res
    
    #submit answer
    def __postAnswer(self, url, answer):
        logging.debug("POST answer {}".format(answer))

        r = self.session.post(url, json=answer)
        logging.debug("HTTP {} - {}: {}".format(r.status_code, r.reason, r.text))
        return r

    # queries current assignment document and saves it
    def __getAssignment(self, studentId, stage, token):
        logging.info("Downloading assignment for stage {}".format(stage))
        logging.debug("GET {}".format(self.__pdfUrl(studentId, stage, token)))

        r = self.session.get(self.__pdfUrl(studentId, stage, token))
        dest = os.path.join(self.outdir, "assignment{}.pdf".format(stage))
        with open(dest, "wb") as f:
            f.write(r.content)

        logging.debug("file {} written".format(dest))
    
    # GETs initial token
    def __getToken(self):
        logging.debug("GET initial token")
        r = self.session.get(startUrlTemplate.format(studentId=self.studentId))
        res = r.json()
        logging.debug(res)
        return res['token']

    def __testcaseUrl(self, studentId, stage, testcase, token):
        return testcaseUrlTemplate.format(stage=stage, studentId=studentId, testcase=testcase, token=token)
    
    def __pdfUrl(self, studentId, stage, token):
        return pdfUrlTemplate.format(stage=stage, studentId=studentId, token=token)


    
class Stage(ABC):
    
    @abstractmethod
    def solveTask(testcase: dict):
        pass