from multiprocessing import Pool, freeze_support
from time import sleep
import streamlit as st
from stqdm import stqdm

c1, c2, _ = st.columns([1,1,1])

num_p = c1.number_input('Number of processes', value=2, min_value=1, max_value=100)
num_i = c2.number_input('Number of iterations', value=100, min_value=1, max_value=1000, step=100)

control = st.empty()
message = st.empty()

def sleep_and_return(i):
    sleep(0.5)
    return i

def run_pool(n_processes, n_iterations):
    with Pool(processes=n_processes) as pool:
        pool.imap()
        for i in stqdm(pool.imap(sleep_and_return, range(n_iterations)), total=n_iterations):
            print(i)
            message.info(f'Iteration: {i}')

if __name__ == '__main__':
    # On Windows an error was being thrown which suggested freeze_support() as a fix
    #   "An attempt has been made to start a new process before the
    #    current process has finished its bootstrapping phase...."
    freeze_support()

    if control.checkbox('Run', False):
        while True:
            run_pool(n_processes=num_p, n_iterations=num_i)
    else:
        message.info('Check to run the pool')