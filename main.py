import logging
import argparse
import os
from stageSolver import StageSolver
from stages.stage01 import Stage01

def main(studentId, outdir, onlyFetchInitialTask):
    logging.info("Starting with student ID: {id}\noutDir: {out}\njust initial: {ini}".format(id=studentId, out=outdir, ini=onlyFetchInitialTask))
    
    stages = [Stage01()] # TODO: implement and pass stages to solver
    solver = StageSolver(studentId, stageImplementations=stages, outdir=outdir)

    if onlyFetchInitialTask:
        solver.getInitialAssignment()
    else:
        solver.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("studentId", help="Your student ID")
    parser.add_argument("--init", help="Retrieves the first task description", action='store_true')
    parser.add_argument("--debug", help="better logging", action='store_true')

    args = parser.parse_args()

    outdir = "out"
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    #logging.basicConfig(filename=outdir + "/log", format='%(asctime)s %(levelname)s: %(message)s')
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG if args.debug else logging.INFO)
    main(args.studentId, outdir, args.init)
