import logging
import argparse
import os
from stageSolver import StageSolver
from stages.example_exercise import *
# from stages.individual import * 

def main(studentId, outdir, onlyFetchInitialTask, continueStage, token):
    stages = [Stage01(), Stage02(), Stage03(), Stage04()] # TODO: implement and pass stages to solver
    
    if len(stages) < 1 or (continueStage is not None and len(stages) < continueStage):
        logging.error("NO OR TOO FEW STAGE IMPLEMENTATIONS GIVEN! Provide stage solutions in stages array")
        return

    if not continueStage:
        logging.info("Starting with student ID: {id}\noutDir: {out}\njust initial: {ini}".format(id=studentId, out=outdir, ini=onlyFetchInitialTask))
    else:
        logging.info("Continue on stage {s} with token {t} and student ID {id}".format(id=studentId, s=continueStage, t=token))

    solver = StageSolver(studentId, stageImplementations=stages, outdir=outdir, startStage=continueStage, token=token)

    if onlyFetchInitialTask:
        solver.getInitialAssignment()
    else:
        solver.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("studentId", help="Your student ID")
    parser.add_argument("--init", help="Retrieves the first task description", action='store_true')
    parser.add_argument("--debug", help="better logging", action='store_true')
    parser.add_argument("--stage", help="stage to continue on", type=int)
    parser.add_argument("--token", help="token for stage")

    args = parser.parse_args()

    outdir = "out"
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG if args.debug else logging.INFO)
    main(args.studentId, outdir, args.init, args.stage, args.token)
