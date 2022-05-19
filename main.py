import requests
from PIL import Image

BASE_URL = "https://api.mangadex.org"

# searches titles and returns a list of ids of the results
def search(title: str):
    url_title = title.replace(" ", "%20") # replaces spaces with %20 for URL

    response = requests.get(BASE_URL + f"/manga?title={url_title}").json() # gets response in JSON
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

    print("TITLE: " + results['attributes']['title']['en'] + '\n')

    # prints description
    print("Description:")
    print(results['attributes']["description"]['en'])
    print('-'*25)


    # gets cover art
    COVER_URL = "https://uploads.mangadex.org/covers/"

    for i, relationship in enumerate(results['relationships']): # searches for cover art
        if relationship['type'] == 'cover_art':
            index = i
            break

    file_name = results['relationships'][index]['attributes']['fileName'] # gets file name
    cover_req = requests.get(f"{COVER_URL}{id}/{file_name}", stream=True)

    # displays cover art
    img = Image.open(cover_req.raw)
    img.show()


def random():
    response = requests.get(f"{BASE_URL}/manga/random?includes[]=cover_art").json() # requests random manga

    id = response['data']['id'] # gets id
    get_details(id) # prints details


def main():
    # menu
    print("1. Search \n2. Random")
    choice = int(input("Select an option: \n"))

    if choice == 1:
        ids = search(input("What would you like to search?\n"))
        print(f"{'-'*25}")
        get_details(ids[int(input("Which one would you like to learn more about? (enter number):\n"))-1])
    
    else:
        random()


if __name__ == '__main__':
    main()