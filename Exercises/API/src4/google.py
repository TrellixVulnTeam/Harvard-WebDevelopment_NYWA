import requests

def main():
    res = requests.get("https://www.google.com/")
    print(res.text)

    #printing out the response of google, the html version


if __name__ == "__main__":
    main()
