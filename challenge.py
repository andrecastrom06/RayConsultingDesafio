from googleapiclient.discovery import build

idAPI = "AIzaSyA9oZQetlGjiN2Ve5c8-3Rg0vBbhTd1dgY" #id da api
idPlaylist = "PLfoNZDHitwjUv0pjTwlV1vzaE0r7UDVDR" #id da playlist que sera utilizada
clienteAPI = build('youtube', 'v3', developerKey=idAPI) #autenticação e especificação da api utilizada

def getVideos(clienteAPI, idPlaylist, maxResultados = 24): #busca os videos na playlist, máximo de 24 já que é o número corridas no ano de 2024
    try:
        requestVideos = clienteAPI.playlistItems().list( #pede uma lista com o conteudo da playlist
            part = "snippet,contentDetails", #guarda em part os detalhes relevantes dos videos
            playlistId = idPlaylist, #guarda a id da playlist
            maxResults = maxResultados #guarda em maxResults o número máximo de resultados que podem ser achados (24)
        )
        responseVideos = requestVideos.execute() #executa o que foi solicitado
        return responseVideos['items'] #retorna somente a lista dos videos que foram solicitados
    except Exception as e:
        print(f"Erro ao buscar vídeos: {e}") #se houve erro informa qual foi
        return []

def getDados(clienteAPI, idVideos):
    try:
        requestDetalhesVideos = clienteAPI.videos().list( #pede uma lista com detalhes de cada vídeo
            part="snippet,statistics", #guarda em part os detalhes relevantes de cada video
            id=",".join(idVideos) #passa os ids para id e os separa por virgula
        )
        responseDetalhesVideos = requestDetalhesVideos.execute() 
        return responseDetalhesVideos['items'] #retorna somente a lista dos dados dos videos que foram solicitados
    except Exception as e:
        print(f"Erro ao buscar dados dos vídeos: {e}")
        return []
    
def main():
    print("\n")
    videos = getVideos(clienteAPI, idPlaylist) #chama getVideos
    idVideos = [video['contentDetails']['videoId'] for video in videos] #percorre video por video e salva em idVideos
    dadosVideos = getDados(clienteAPI, idVideos) #chama getDados
    ordemVideos = sorted(dadosVideos, key=lambda x: int(x['statistics']['viewCount']), reverse=True) #ordena os videos em ordem crescente de visualização
    for indice, video in enumerate(ordemVideos, start=1): #estrutura que se repete ate armazenar e printar no console todos os videos
        tituloVideo = video['snippet']['title'] #armazena titulo do video
        visualizacoes = video['statistics']['viewCount'] #armazena numero de visualizações do video
        curtidas = video['statistics']['likeCount']
        comentarios = video['statistics']['commentCount']
        print(f"{indice}. Título: {tituloVideo}\nVisualizações: {visualizacoes}\nCurtidas: {curtidas}\nComentários: {comentarios}") #printa no console
        print("\n\n")

if __name__ == "__main__":
    main()