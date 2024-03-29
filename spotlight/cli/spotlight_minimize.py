#! /usr/bin/env python
""" Optimizes a refinement plan.
"""

import argparse
import numpy
import os
import socket
import time
from mystic import termination
from mystic import tools
from spotlight import version
from spotlight.io import configuration_file
from spotlight.io import solution_file
from spotlight.io import state_file

# get parallel-processing information
hostname = socket.gethostname()
run_dir = os.getcwd()
try:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    comm = None if size == 1 else comm
except ImportError:
    print("The mpi4py packages was not found!")
    comm = None
    size = 1
    rank = 0

def main():

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-files", nargs="+", required=True)
    parser.add_argument("--config-overrides", nargs="+")
    parser.add_argument("--tmp-dir", default="tmp")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--version", action=version.VersionAction)
    opts = parser.parse_args()
    
    # move to temporary dir, read configuration file, and get refinement plan
    tmp_dir = "{}_{}".format(opts.tmp_dir, rank)
    config = configuration_file.ConfigurationFile(opts.config_files, tmp_dir, change=True,
                                                  config_overrides=opts.config_overrides)
    cost = config.get_refinement_plan()
    
    # set random seed
    seed = config.seed if hasattr(config, "seed") else 0
    seed += rank
    numpy.random.seed(seed)
    tools.random_seed(seed)
    
    # create an archive file for output data
    output_file = config.solution_file if config.solution_file.startswith("/") \
                      else run_dir + "/" + config.solution_file
    fp_sol = solution_file.SolutionFile(output_file, config)
    if rank == 0:
        print("Rank 0 is writing configuration to {}".format(output_file))
        fp_sol.save_config()
    if comm:
        print("Rank {} is waiting".format(rank))
        comm.Barrier()
    
    # create an archive file for state data
    output_file = config.state_file if config.state_file.startswith("/") \
                      else run_dir + "/" + config.state_file
    fp_state = state_file.StateFile(output_file)
    
    # run one of ensemble of solvers
    for i in range(config.num_solvers):
        local_tag = "_".join(map(str, [rank, i, config.tag if hasattr(config, "tag") else seed]))
    
        # check if there is a previous state for a local solver
        fp_sol.arch.load(local_tag)
        fp_state.arch.load(local_tag)
        if local_tag in fp_sol.arch.keys() and local_tag in fp_state.arch.keys():
    
            # if the local solver has not terminated then start from there
            # we have to explicltly set the termination conditions because Mystic
            # parses ``__doc__`` for getting the conditions YIKES!
            if fp_sol.arch[local_tag][4] == 0:
                print("Loading a previous state for {}".format(local_tag))
                local_solver = fp_state.arch[local_tag]
                local_solver.local_solver.SetEvaluationLimits(
                    local_solver.max_iterations,
                    local_solver.max_evaluations)
                local_solver.stop = termination.NormalizedChangeOverGeneration(
                    local_solver.stop_change, local_solver.stop_generations)
    
            # otherwise initialize a local solver from configuration file
            else:
                print("Optimization loop already terminated for {}".format(local_tag))
                continue
    
        # if there is not a previous state initialize local solver
        else:
            print("Initializing a state for {}".format(local_tag))
            local_solver = config.get_solver(arch=fp_sol, iteration=i)
    
        # print statement
        print("Process {} of {} running walker {} of {} on {}".format(
                  rank + 1, size, i + 1, config.num_solvers, hostname))
    
        # main optimization loop with checkpointing
        if hasattr(config, "checkpoint_stride"):
            stop = False
            while not stop:
    
                # set timer
                t_start = time.time()
        
                # take steps in optimization
                for _ in range(config.checkpoint_stride):
                    stop = local_solver.step(cost)
    
                # end timer
                duration = time.time() - t_start
    
                # save output
                fp_sol.save_data(local_tag, local_solver, duration)
                fp_state.save_state(local_tag, local_solver)
    
        # main optimization loop without checkpointing
        else:
            t_start = time.time()
            local_solver.solve(cost)
            duration = time.time() - t_start
            fp_sol.save_data(local_tag, local_solver, duration)
            fp_state.save_state(local_tag, local_solver)
    
        # print statement
        print("Evaluation time for process {} of {} running walker {} of {} on {} is {}s".format(
                  rank, size, i + 1, config.num_solvers, hostname, fp_sol.arch[local_tag][5]))
    
    # finish
    if comm:
        comm.Barrier()
    if rank == 0:
        print("Finished!")

if __name__ == "__main__":
    main()
