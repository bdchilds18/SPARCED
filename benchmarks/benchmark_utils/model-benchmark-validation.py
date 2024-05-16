# -*- coding: utf-8 -*-
#!/usr/bin/env python     
"""
Created on Thurs. 05/16/2024 10:45:00 - JRH

Script to automate model-benchmark comparison to prior validated results of
the SPARCED model.

Provide a path to the model directory and the script will run all benchmarks, 
outputing visual results to a 'results' directory within the model directory 
for anlysis. 

Users are anticipated to compare simulation results to prior validated results.
"""

#-----------------------Package Import & Defined Arguements-------------------#
import os
import argparse
import subprocess, sys


# Parse the command line arguments
parser = argparse.ArgumentParser(description=
                                 'Perform model benchmark validation')
parser.add_argument('-m', '--model', type=str, 
                                    help='Path to the model directory')
args = parser.parse_args()

# Check if the model directory was provided
try:
    assert args.model is not None
except:
    print("Please provide a path to the model directory")
    sys.exit(1)

#-----------------------Function to Run All Benchmarks-------------------------#
def run_all_benchmarks(model_path: str):
    """
    Run all benchmarks in the benchmarks directory
    Input:
        Model: Path to the model directory

    Output:
        simulation results for all benchmarks to a 'results' directory
        within the model directory
    """

    os.chdir('..')

    # Find all benchmarks to be completed
    directory_contents = os.listdir()

    # Remove the benchmark_utils directory
    directory_contents = [d for d in directory_contents if d!= 'benchmark_utils']

    # Remove any files in the directory
    directory_contents = [d for d in directory_contents if os.path.isdir(d)]

    for benchmark in directory_contents:

        # Run the benchmark
        print(f"Running benchmark {benchmark}")

        Command = "mpiexec -n 4 python3 run_benchmark.py -m {args.model} -b {benchmark}"

        subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE)


#-----------------------Run All Benchmarks-------------------------------------#
if __name__ == '__main__':
    run_all_benchmarks()