from googleapiclient.discovery import build
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

idAPI = "AIzaSyA9oZQetlGjiN2Ve5c8-3Rg0vBbhTd1dgY"  # id da API
idPlaylist = "PLfoNZDHitwjUv0pjTwlV1vzaE0r7UDVDR"  # id da playlist que será utilizada
clienteAPI = build('youtube', 'v3', developerKey=idAPI)  # autenticação e especificação da API utilizada

def getVideos(clienteAPI, idPlaylist, maxResultados=24):
    try:
        requestVideos = clienteAPI.playlistItems().list(  # pede uma lista com o conteúdo da playlist
            part="snippet,contentDetails",  # guarda em 'part' os detalhes relevantes dos vídeos
            playlistId=idPlaylist,  # guarda a id da playlist
            maxResults=maxResultados  # define o número máximo de resultados
        )
        responseVideos = requestVideos.execute()  # executa o que foi solicitado
        return responseVideos['items']  # retorna somente a lista dos vídeos que foram solicitados
    except Exception as e:
        print(f"Erro ao buscar vídeos: {e}")  # se houve erro, informa qual foi
        return []

def getDados(clienteAPI, idVideos):
    try:
        requestDetalhesVideos = clienteAPI.videos().list(  # pede uma lista com detalhes de cada vídeo
            part="snippet,statistics",  # guarda em 'part' os detalhes relevantes de cada vídeo
            id=",".join(idVideos)  # passa os ids para 'id' e os separa por vírgula
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
    
    fig, ax = plt.subplots(figsize=(14, 8))  # Criando o gráfico de barras
    x = range(len(tituloVideo))  # Posições para o título dos vídeos no gráfico
    
    # Função para atualizar o gráfico com base nas seleções
    def selecionarGrafico(label):
        ax.clear()  # Limpa o gráfico atual
        
        if 'Visualizações' in label:
            ax.bar(x, visualizacoesVideo, width=0.2, label="Visualizações", align="center")
        if 'Curtidas' in label:
            ax.bar(x, curtidasVideo, width=0.2, label="Curtidas", align="center")
        if 'Comentários' in label:
            ax.bar(x, comentariosVideo, width=0.2, label="Comentários", align="center")

        # Adicionando título e rótulos
        ax.set_title("Desafio Ray Consulting, consumo de API para dados de F1", fontsize=16)
        ax.set_xticks(x)
        ax.set_xticklabels(tituloVideo, rotation=90, fontsize=10)
        ax.legend(fontsize=12)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Exibindo o gráfico
        fig.tight_layout()
        plt.draw()

    # Adicionando os checkboxes para selecionar quais dados visualizar
    ax_check = plt.axes([0.02, 0.25, 0.18, 0.5], frameon=False)  # Posicionando os checkboxes à esquerda
    check = CheckButtons(ax_check, ['Visualizações', 'Curtidas', 'Comentários'], [True, True, True])  # Inicializa todos como True
    
    # Aumentando o tamanho da fonte dos CheckButtons
    for label in check.labels:
        label.set_fontsize(8)  # Aumenta o tamanho da fonte para tornar os botões mais visíveis
        label.set_fontweight('bold')  # Deixa o texto mais destacado

    # Ajustando a posição dos checkbuttons para ficarem mais visíveis à esquerda
    ax_check.set_position([0, 0.1, 0.05, 0.3])  # Posição dos checkbuttons para alinhamento à esquerda com mais espaço para a palavra
    
    check.on_clicked(selecionarGrafico)  # Atualiza o gráfico conforme a seleção
    
    # Exibindo o gráfico interativo
    selecionarGrafico(['Visualizações', 'Curtidas', 'Comentários'])
    plt.show()

if __name__ == "__main__":  # Garante a execução de maneira correta
    main()