import os
import easygui
import psutil
import shutil
import subprocess
from os.path import dirname, join, abspath


def install_workers():
    if is_installed():
        return None
    else:
        anarede_exe = easygui.fileopenbox("Selecione o executavel do do ANAREDE", "Executavel do ANAREDE",
                                          "C:\\Cepel\\Anarede")

        if anarede_exe is None:
            easygui.msgbox("Não foi obtido um executavel valido do ANAREDE. A execucao nao sera possivel.", "Nenhum executavel selecionado")
            return None

        anarede_dir = dirname(anarede_exe)

        num_cpu = psutil.cpu_count()

        num_worker = round(0.75 * num_cpu)

        worker_dir = easygui.diropenbox("Selecione o diretorio dos workers", "Diretorio dos workers")

        if worker_dir is None:
            easygui.msgbox("Não foi obtido um diretorio para instalar os workers. A execucao nao sera possivel.", "Nenhum diretorio selecionado")
            return None

        for i in range(num_worker):
            shutil.copytree(anarede_dir, abspath(join(worker_dir, f"w{i + 1}")))

        subprocess.run(["setx", "ANAREDE_WORKERS_DIR", worker_dir], shell=True)

        return None


def is_installed():
    try:
        worker_dir = os.environ["ANAREDE_WORKERS_DIR"]
        return True
    except KeyError:
        return False
