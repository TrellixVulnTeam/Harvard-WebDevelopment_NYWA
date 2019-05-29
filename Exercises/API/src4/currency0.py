import requests

def main():
    res = requests.get("https://api.fixer.io/latest?base=USD&symbols=EUR")
    if res.status_code != 200: #status code
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json() #extracting the result of the request and saving it as a variable
    print(data)

if __name__ == "__main__":
    main()
