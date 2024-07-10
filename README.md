<div align="center">
  <h1 style="background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px;">
    YouTube Video Downloader
  </h1>
  <img src="https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif" alt="Download Animation"/>
</div>

Este projeto é um aplicativo web simples que permite baixar vídeos do YouTube. Utilizando Python Flask no backend e tecnologias web modernas no frontend, ele fornece uma interface amigável para realizar o download de vídeos.

## Recursos

- Download de vídeos do YouTube fornecendo a URL do vídeo.
- Exibição do progresso do download em tempo real.
- Notificação de conclusão do download.
- Interface simples e intuitiva.

## Tecnologias Utilizadas

- Python Flask
- yt-dlp (fork do youtube-dl)
- Socket.IO
- Bootstrap 4
- SweetAlert2

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/lanroo/downloadering.git
   cd downloadering
2. Crie um ambiente virtual e ative-o:
   
   ```bash
    python -m venv venv
    source venv/bin/activate # No Windows use: venv\Scripts\activate

3. Instale as dependências:

   ```bash
    pip install -r requirements.txt

4. Configure a aplicação (se necessário):

- Verifique o arquivo config.py para qualquer configuração específica.

## Uso

1. Execute o servidor Flask:

    ```bash
    flask run
    
3. Acesse a aplicação no navegador:

 - Abra o navegador e vá para http://127.0.0.1:5000.

4. Baixe um vídeo:
   - Insira a URL do vídeo do YouTube na interface web.
   - Clique em "Baixar".
   - Acompanhe o progresso do download na barra de progresso.
   - Após a conclusão, você será notificado e poderá baixar o arquivo.

## Contribuição

 1. Faça um fork do repositório.

 2. Crie uma nova branch:
  
  ```bash
  git checkout -b feature/nova-feature
  ```
 3. Faça suas alterações e commit:

  ```bash
  git commit -m 'Adicionar nova feature'
  ```
4. Faça push para a branch:
  ```bash
  git push origin feature/nova-feature
  ```
5. Envie um Pull Request.

## Contato
Se você tiver dúvidas ou sugestões, sinta-se à vontade para entrar em contato:

Nome: Lanna
Email: yladacz@gmail.com

Feito com ❤️ por Lanna
