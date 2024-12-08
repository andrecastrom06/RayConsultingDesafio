from googleapiclient.discovery import build
import matplotlib.pyplot as plt

idAPI = "AIzaSyA9oZQetlGjiN2Ve5c8-3Rg0vBbhTd1dgY"  # id da API
idPlaylist = "PLfoNZDHitwjUv0pjTwlV1vzaE0r7UDVDR"  # id da playlist que será utilizada
clienteAPI = build('youtube', 'v3', developerKey=idAPI)  # autenticação e especificação da API utilizada

def getVideos(clienteAPI, idPlaylist, maxResultados=24):
    try:
        requestVideos = clienteAPI.playlistItems().list( #pede uma lista com o conteudo da playlist
            part = "snippet,contentDetails", #guarda em part os detalhes relevantes dos videos
            playlistId = idPlaylist, #guarda a id da playlist
            maxResults = maxResultados #guarda em maxResults o número máximo de resultados que podem ser achados (24)
        )
        responseVideos = requestVideos.execute()  # executa o que foi solicitado
        return responseVideos['items']  # retorna somente a lista dos vídeos que foram solicitados
    except Exception as e:
        print(f"Erro ao buscar vídeos: {e}")  # se houve erro, informa qual foi
        return []

def getDados(clienteAPI, idVideos):
    try:
        requestDetalhesVideos = clienteAPI.videos().list(  # pede uma lista com detalhes de cada vídeo
            part = "snippet,statistics",  # guarda em 'part' os detalhes relevantes de cada vídeo
            id = ",".join(idVideos)  # passa os ids para 'id' e os separa por vírgula
        )
        responseDetalhesVideos = requestDetalhesVideos.execute()
        return responseDetalhesVideos['items']  # retorna somente a lista dos dados dos vídeos
    except Exception as e:
        print(f"Erro ao buscar dados dos vídeos: {e}")
        return []

def main():
    print("\n")
    videos = getVideos(clienteAPI, idPlaylist)  # chama getVideos
    idVideos = [video['contentDetails']['videoId'] for video in videos]  # percorre vídeo por vídeo e salva em idVideos
    dadosVideos = getDados(clienteAPI, idVideos)  # chama getDados
    ordemVideos = sorted(dadosVideos, key=lambda x: int(x['statistics']['viewCount']), reverse=True)  # ordena os vídeos em ordem crescente de visualização
    
    tituloVideo = []
    visualizacoesVideo = []
    curtidasVideo = []
    comentariosVideo = []
    
    for indice, video in enumerate(ordemVideos, start=1):  # estrutura que se repete até armazenar e printar no console todos os vídeos
        titulo = video['snippet']['title']  # armazena título do vídeo
        visualizacoes = video['statistics']['viewCount']  # armazena número de visualizações
        curtidas = video['statistics']['likeCount']  # armazena número de curtidas
        comentarios = video['statistics']['commentCount']  # armazena número de comentários

        # Popula os campos que irão ao gráfico
        tituloVideo.append(titulo)
        visualizacoesVideo.append(int(visualizacoes))  # Converte para inteiro
        curtidasVideo.append(int(curtidas))  # Converte para inteiro
        comentariosVideo.append(int(comentarios))  # Converte para inteiro

        print(f"{indice}. Título: {titulo}\nVisualizações: {visualizacoes}\nCurtidas: {curtidas}\nComentários: {comentarios}")  # Print no console
        print("\n\n")
    
    plt.figure(figsize=(14, 8)) # Criando o gráfico de barras
    
    x = range(len(tituloVideo))  # Posições para o título dos vídeos no gráfico
    
    # Populando as barras para visualizações, curtidas e comentários
    plt.bar(x, visualizacoesVideo, width=0.2, label="Visualizações", align="center")
    plt.bar(x, curtidasVideo, width=0.2, label="Curtidas", align="edge")
    plt.bar(x, comentariosVideo, width=0.2, label="Comentários", align="edge")

    # Adicionando título e rótulos
    plt.xlabel("Vídeos", fontsize=14)
    plt.ylabel("Contagem", fontsize=14)
    plt.title("Comparação de Visualizações, Curtidas e Comentários por Vídeo", fontsize=16)
    
    # Definindo os rótulos do eixo X
    plt.xticks(x, tituloVideo, rotation=90, fontsize=10)
    
    # Adicionando uma legenda
    plt.legend(fontsize=12)
    
    # Adicionando o grid para facilitar a leitura dos valores
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Ajustando o layout para não cortar rótulos
    plt.tight_layout()
    
    # Exibindo o gráfico
    plt.show()

if __name__ == "__main__":  # Garante a execução de maneira correta
    main()