import requests
from PIL import Image

BASE_URL = "https://api.mangadex.org"

# searches titles and returns a list of ids of the results
def search(title: str):
    encoded = title.replace(" ", "%20") # replaces spaces with %20 for URL
    response = requests.get(BASE_URL + f"/manga?title={encoded}").json() # gets response in JSON
    results = response["data"] # gets only the data 

    print(f"{'-'*25}\nRESULTS: ")
    ids = []
    for i, result in enumerate(results): # iterates through each result
        ids.append(result["id"]) # adds id to ids for easy access

        print(f"{i+1}: {list(result['attributes']['title'].values())[0]}") # prints title

    return ids

# gets details about a title with its id
def get_details(id: str):
    print('-'*25)
    print(f"URL: https://mangadex.org/title/{id}\n") # prints mangadex page
    response = requests.get(f"{BASE_URL}/manga/{id}?includes[]=cover_art").json() # Gets response in JSON
    results = response['data'] # gets only the data

    print("Description:\n" + results['attributes']["description"]['en']) # prints description
    print('-'*25)

    # gets cover art
    COVER_URL = "https://uploads.mangadex.org/covers/"
    file_name = results['relationships'][2]['attributes']['fileName'] # gets file name (in relationships, index 2, attributes, fileName)
    cover_req = requests.get(f"{COVER_URL}{id}/{file_name}", stream=True)

    # displays cover art
    img = Image.open(cover_req.raw)
    img.show()


ids = search(input("What would you like to search?\n"))
print(f"{'-'*25}")
get_details(ids[int(input("Which one would you like to learn more about? (enter number):\n"))-1])