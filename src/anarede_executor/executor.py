import os
import time
import random
import subprocess
from os.path import dirname, join, abspath
from functools import partial

import psutil
from concurrent.futures import ProcessPoolExecutor


MAX_NUM_WORKERS = round(0.75 * psutil.cpu_count())
DEFAULT_TIMEOUT = 60
MIN_CPU_USE_INTERVAL = 0.01
DEFAULT_MAX_CPU_ZERO_COUNT = 50
DEFAULT_WORKERS_DIR = os.environ.get("ANAREDE_WORKERS_DIR", None)


def run_pwf_file(pair, num_workers=MAX_NUM_WORKERS, timeout=DEFAULT_TIMEOUT, cpu_use_interval=MIN_CPU_USE_INTERVAL,
                 max_cpu_zero_count=DEFAULT_MAX_CPU_ZERO_COUNT, worker_dir=DEFAULT_WORKERS_DIR):
    anarede_path, pwf_file = pair
    cmd = [anarede_path, pwf_file]
    print(f"Executando: {' '.join(cmd)}")

    time.sleep((5 + random.randint(0, 10)) * cpu_use_interval)

    num_files_start = len(os.listdir(dirname(pwf_file)))

    process = subprocess.Popen(
        cmd
    )
    process_info = psutil.Process(process.pid)

    time.sleep((2 + random.randint(0, 5)) * cpu_use_interval)

    start = time.time()

    try:
        cpu_zero_count = -1
        while True:
            if process_info.cpu_percent(interval=cpu_use_interval) == 0.0:
                if cpu_zero_count != -1:
                    cpu_zero_count += 1
            else:
                cpu_zero_count = 0
            elapsed_time = time.time() - start
            if elapsed_time > timeout:
                print(f"Timeout atingido. Encerrando processo {pwf_file}...")
                process.kill()
                process.wait()
                break
            if cpu_zero_count > max_cpu_zero_count:
                num_files = len(os.listdir(dirname(pwf_file)))
                if num_files > num_files_start:
                    print(f"CPU count atingido. Encerrando processo {pwf_file}...")
                    process.kill()
                    process.wait()
                    break
                else:
                    print(f"CPU count atingido. Nenhum arquivo adicional detectado. Aguardando processo {pwf_file}...")
                    cpu_zero_count -= 25
            time.sleep(cpu_use_interval)
    except Exception as error:
        raise error

    time.sleep(2 * cpu_use_interval)

    return f"{pwf_file} finalizado com {anarede_path}"


def distribute_pwf_files(pwf_files, workers_paths):
    pairs = []
    for file_index, file in enumerate(pwf_files):
        path = workers_paths[file_index % len(workers_paths)]
        pairs.append((path, file))
    return pairs


def run_anarede(pwf_files, num_workers=MAX_NUM_WORKERS, timeout=DEFAULT_TIMEOUT, cpu_use_interval=MIN_CPU_USE_INTERVAL,
                max_cpu_zero_count=DEFAULT_MAX_CPU_ZERO_COUNT, worker_dir=DEFAULT_WORKERS_DIR):
    if worker_dir is None:
        raise EnvironmentError("Workers do ANAREDE nao instalados")

    workers_paths = [f"{worker_dir}\\w{i + 1}\\anarede.exe" for i in range(num_workers)]

    pairs = distribute_pwf_files(pwf_files, workers_paths)

    execute_anarede = partial(run_pwf_file, num_workers=num_workers, timeout=timeout,
                              cpu_use_interval=cpu_use_interval, max_cpu_zero_count=max_cpu_zero_count,
                              worker_dir=worker_dir)

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(execute_anarede, pairs)

    for result in results:
        print(result)
