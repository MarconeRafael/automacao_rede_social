# Instagram Hashtag Profile Collector

Este projeto permite buscar perfis do Instagram a partir de postagens associadas a uma hashtag específica, utilizando Selenium para automação.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados em sua máquina:

- **Python 3.8 ou superior**
- **Google Chrome**
- **ChromeDriver** (gerenciado automaticamente pelo `webdriver-manager`)

Além disso, instale as dependências necessárias executando o comando:

```bash
crie uma virtual env 
pip install -r requirements.txt



Opção 01:
Crie um arquivo chamado keys.py e defina as variáveis.
IG_USERNAME=seu_usuario
IG_PASSWORD=sua_senha
chave_openai = sua chave
whatsapp_link = link do whatsapp da empresa


Opção 2:
##Configuração
1. Configurar Variáveis de Ambiente
whatsapp_link

set IG_USERNAME=seu_usuario
set IG_PASSWORD=sua_senha

#No Linux/MacOS:

export IG_USERNAME=seu_usuario
export IG_PASSWORD=sua_senha
 Obs: caso escolha a opção 2 será necessário fazer leves alterações no código e terá que fazer esse Set ou export sempre que iniciar o sistema