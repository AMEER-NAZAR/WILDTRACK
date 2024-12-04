from google_images_search import GoogleImagesSearch

api_key = "AIzaSyA14jBe9ttnW3Dy2xrEyskgkkn-nT8PGvU"
cx = "f267b5cb582df45ba"

gis = GoogleImagesSearch(api_key, cx)

search_params = {
    'q': 'different food images',
    'num': 100,  # Number of results to fetch
    'safe': 'high',  # Safe search level ('high', 'medium', 'off')
}

gis.search(search_params=search_params)

# Download images
try:
    for image in gis.results():
        image.download(r"data")  # Specify the path where you want to save the images


    # Print image URLs
    for image in gis.results():
        print(image.url)
except:
    pass