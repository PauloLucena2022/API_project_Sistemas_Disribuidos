# Instruções para Executar a API

## Como Executar

Certifique-se de que você tem o **Docker** e o **Docker Compose** instalados.

1. Abra um terminal na raiz do seu projeto (`API_project_Sistemas_Distribuidos/`).

2. Execute o seguinte comando para construir a imagem e iniciar o contêiner:

   ```bash
   docker compose up --build
   ```

3. Caso já tenha construído o contêiner com `docker compose up --build`, use apenas o seguinte comando para executar o contêiner:

   ```bash
   docker compose up
   ```

4. Após a execução, sua API estará rodando e acessível em `http://localhost:5000`. Você poderá interagir com os endpoints `/login` e `/predict` conforme definido em `api_flask.py`.