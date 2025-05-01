from os.path import dirname, join, abspath
from src.anarede_executor import install_workers, is_installed, run_anarede


if __name__ == "__main__":
    if not is_installed():
        install_workers()
    else:
        cases_dir = abspath(join(dirname(__file__), "cases"))
        pwf_files = [f"{cases_dir}\\case65\\case65-{str(i + 1).zfill(2)}\\case65.pwf" for i in range(30)]
        run_anarede(pwf_files, num_workers=8)
