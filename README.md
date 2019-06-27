# data_science 
Projeto de analise de dados proposto no teste da empresa cognitivo.

# Instalação do projeto:
## Requerimentos do projeto
  python 3.7
  
  1) Criar uma virtualenv ou qualquer enviroment e instalar as dependencias do projeto.
  
    
    
  ```
  Para instalar o Virtualenv com Python 3:
    Linux
    $ pip3 install virtualenv
    
  Criar um ambiente virtual
    Linux
    $ python3 -m venv myvenv
    
    Windows
    C:\Users\Name\djangogirls> python -m venv myvenv
    
  Ativar ambiente virtual
    Linux
    $ source myvenv/bin/activate
    
    Windows
    Observação: no Windows 10, 
    você pode obter um erro no Windows PowerShell que diz execution of scripts is disabled on this system. 
    Neste caso, abra uma outra janela do Windows PowerShell com a opção de "Executar como Administrador". 
    Assim, execute o comando abaixo antes de iniciar o seu ambiente virtual:
    
    C:\WINDOWS\system32> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
    
  Instalando pacotes
    Linux
    (myvenv) ~$ pip install -r requirements.txt
    
    Windows
    C:\Users\Name\djangogirls> python -m pip install -r requirements.txt
   ```
   
   # Rodando o projeto.
   
   ```
   No diretorio do projeto, ative o ambiente virtual criado e execute o script relatorio.py
    $ python relatorio.py
    
   Caso, já exista um "arquivo.csv" no diretorio, são dados já apurados.
   Melhor experi￿ência será excluindo o arquivo "arquivo.csv", pois o dados serão apurados em tempo real.
    
   Os csvs gerados dos top10 são gerados a cada vez que o programa é gerado, a api do twitter é muito variavel
   portanto seria melhor investigar os top10 em forma de series temporais. Cada arquivo csv, retornara o top10
   do momento.
   ```
   
   # Duvidas Sobre o projeto
   ```
   Seria preciso criar uma api web para disponibilizar os dados? No documento de teste não ficou claro essa abordagem.
   ```
