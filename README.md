# Anarede  Executor
*Python library to run ANAREDE PWF files using parallelism.*

Este repositório contém um programa em Python para executar o ANAREDE em paralelo, aproveitando múltiplas instâncias do 
executável para acelerar o processamento de arquivos de fluxo de carga.

## ⚠️ Atenção

> É necessário que o **ANAREDE esteja instalado** previamente em sua máquina. O executável `anarede.exe` deve estar 
> disponível nos diretórios das instâncias paralelas.

## ⚠️ Atenção

> Na primeira execução, é necessário usar o comando `install_workers()` para criar as pastas das instâncias paralelas.
> Consulte os exemplos.

---

## ✅ Pré-requisitos

- Python 3.8 ou superior (testado apenas no Python 3.13)
- Executável do ANAREDE disponível (e com permissão de execução)

---

## 📦 Instalação

Recomenda-se instalar usando o pip:

```bash
pip install git+https://github.com/munizrodrigo/anarede-executor
```

Mas **apenas se você quiser ter acesso em um local específico da sua máquina**, clone este repositório:

```bash
git clone https://github.com/munizrodrigo/anarede-executor
```

Entre na pasta clonada e instale os requisitos:

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

### 🔧 Definindo arquivos e caminhos

```python
from anarede_executor import install_workers, is_installed, run_anarede # Importe as funções necessárias
cases_dir = abspath(join(dirname(__file__), "cases"))
pwf_files = [f"{cases_dir}\\case65\\case65-{str(i + 1).zfill(2)}\\case65.pwf" for i in range(30)] # Crie uma lista de arquivos a serem executados em paralelo
```

### 🧵 Execução paralela

```python
run_anarede(pwf_files, num_workers=8) # Execute os arquivos em paralelo usando 8 instâncias independentes
```

### 📌 Exemplo completo

```python
import time
from os.path import dirname, join, abspath
from anarede_executor import install_workers, is_installed, run_anarede


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
```

---

## 🧪 Testes

> ⚠️ Recomendação: inicie os testes com **8 arquivos de entrada** e **8 instâncias**, monitorando se cada instância está sendo corretamente ativada e se os arquivos de saída não estão sendo sobrescritos.

> ⚠️ Recomendação: Garanta que os arquivos .pwf não estejam direcionando seus relatórios para arquivos iguais.

> ⚠️ Recomendação: O mais adequado é que cada arquivo .pwf a ser executado esteja sozinho em sua própria pasta, sendo assim não é ncessário se preocupar com os nomes dos relatórios gerados.

---

## 🙋 Contribuição

Contribuições são bem-vindas! Sinta-se livre para abrir _issues_ ou enviar _pull requests_ com melhorias ou correções.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE.md) para mais detalhes.
