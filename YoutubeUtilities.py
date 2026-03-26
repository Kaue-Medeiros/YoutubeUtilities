# Youtube Utilities
# Version 1.0
# Made by Kaue Medeiros

import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "[YOUR_CLIENT_SECRETS_FILE_HERE]"

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    #youtube = googleapiclient.discovery.build( api_service_name, api_version, credentials=credentials)
    youtube = get_authenticated_service()

    request = youtube.search().list(part="snippet", maxResults=25, q="gameplayrj")
    #request = youtube.channels().list(part="snippet", maxResults=25, q="surfing")
    response = request.execute()
    ListaPesquisa = []
    for i, pesquisa in enumerate(response['items']):
        title = pesquisa['snippet']['title']
        kind = pesquisa['id']['kind']
        kind = kind[kind.find('#')+1:]
        urlID = pesquisa['id']['channelId'] if kind == 'channel' else ( pesquisa['id']['videoId'] if kind == 'video' else 'null')
        ListaPesquisa.append((title, kind, urlID))
        print(i+1, ' - ', ListaPesquisa[i][0], ' - ', ListaPesquisa[i][1], ' - ', ListaPesquisa[i][2])


    print("\n\nQual pesquisa voce deseja o link: ", end="")
    pesquisaInput = int(input())
    url = f"www.youtube.com/{ListaPesquisa[pesquisaInput-1][1]}/{ListaPesquisa[pesquisaInput-1][2]}"
    print("Url: ", url)




def get_authenticated_service():
    if os.path.exists("CREDENTIALS_PICKLE_FILE"):
        with open("CREDENTIALS_PICKLE_FILE", 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        with open("CREDENTIALS_PICKLE_FILE", 'wb') as f:
            pickle.dump(credentials, f)
    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

if __name__ == "__main__":
    main()
