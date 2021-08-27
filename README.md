# Hamburgueria Heat

## Como rodar o projeto localmente
- Verifique a versão de instalação do seu python, o projeto está usando a versão 3.7.9
- Instale a lib para acessar a virtual env `pip install virtualenv`
- Crie uma virtual env `virtualenv venv`
- Ative a virtual env `.\venv\Scripts\activate`
- Verifique a instalação dos pacotes rodando o comando `pip install -r requirements.txt`
- Use o arquivo .env.example para criar seu arquivo .env
- Para iniciar o servidor flask basta rodar o arquivo `python .\app.py`
- Para iniciar o servidor com auto reload coloque o atributo `debug=True` na função `app.run()` no arquivo `app.py` **(Lembre de não comentar com o `debug=True`)**
