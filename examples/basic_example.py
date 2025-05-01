import time
from os.path import dirname, join, abspath
from src.anarede_executor import install_workers, is_installed, run_anarede


if __name__ == "__main__":
    if not is_installed():
        install_workers()
    else:
        cases_dir = abspath(join(dirname(__file__), "cases"))
        pwf_files = [f"{cases_dir}\\case65\\case65-{str(i + 1).zfill(2)}\\case65.pwf" for i in range(30)]

        parallel_start_time = time.time()
        run_anarede(pwf_files, num_workers=8)
        parallel_end_time = time.time()
        parallel_total_time = parallel_end_time - parallel_start_time

        serial_start_time = time.time()
        run_anarede(pwf_files, num_workers=1)
        serial_end_time = time.time()
        serial_total_time = serial_end_time - serial_start_time

        print(f"Tempo gasto utilizando paralelismo: {parallel_total_time}s")
        print(f"Tempo gasto utilizando execução serial: {serial_total_time}s")
