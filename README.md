# MyFinance-Django

Projeto Django para gerenciamento de finanças pessoais.

## Pré-requisitos

Certifique-se de que você tenha as seguintes ferramentas instaladas em seu ambiente:

- Python 3.10 ou superior
- Pip (Python package installer)
- Virtualenv (opcional, mas recomendado)

## Configuração do Ambiente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/JanielMS/MyFinance-Django.git
   cd MyFinance-Django
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências:**

   Execute o comando abaixo para instalar as dependências listadas no `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   Caso não exista o arquivo `requirements.txt`, você pode criar um com o seguinte comando:

   ```bash
   pip freeze > requirements.txt
   ```

   **Dependências do projeto:**
   ```
   asgiref==3.8.1
   Django==5.1.5
   sqlparse==0.5.3
   ```


4. **Realize as migrações do banco de dados:**

   ```bash
   python manage.py migrate
   ```

5. **Execute o servidor de desenvolvimento:**

   ```bash
   python manage.py runserver
   ```

   O projeto estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Funcionalidades

- Gerenciamento de transações (em breve)
- CRUD de categorias, em breve: transações e contas

## Como contribuir

1. Faça um fork do repositório.
2. Crie uma branch para sua feature: `git checkout -b minha-feature`.
3. Faça commit das suas alterações: `git commit -m 'Adicionei uma nova feature'`.
4. Envie para o repositório remoto: `git push origin minha-feature`.
5. Abra um Pull Request.

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
**Autor:** Janiel Maia  
[Link do GitHub](https://github.com/JanielMS)