'''
    Evan Grissino 2025
    Data Reader for Binary Encoded Odds (BEO) strings

    Uses mewtru.com is-odd web api

'''

import sympy
import requests

URL_BASE = "https://is-odd-api.mewtru.com/v1/numbers/"

def getJsonResponse(url):
    '''
    Performs GET request on url and returns response as json
    '''
    try:
        response = requests.get(url)

        if response.status_code == 404:
            return None
        
         # Raise an HTTPError for bad responses
        response.raise_for_status()
        
        # Parse response as JSON
        json_data = response.json()
        return json_data

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def getIsOdd (n):
    '''
    Use the mewtru API to fetch if the number is odd
    '''
    # Format URL with the number
    url = URL_BASE + str(n)

    # Make Get Request and parse JSON response, if 404, then no value set
    json = getJsonResponse (url)

    return json
 
def readString (n, rng):
    '''
    Read Encoded string from database with a range of numbers
    '''
    outputString = ""
    outputBits = ""
    end = n + len(rng)

    for n in rng:
        data = getIsOdd (n)
        if (data != None):
            outputBits += "0" if data['odd'] else "1"
        else:
            print ("Failed to get Number")
            break
    
    while (outputBits):
        byte = outputBits[:8]
        outputString += chr ( int("0b{}".format(byte),2) )
        outputBits = outputBits[8:]
    
    return outputString

def readPrimeString (p, count):
    '''
    Read String from primes range
    '''
    start = sympy.nextprime(p)
    primes = [start]
    for _ in range(1,count):
        primes.append (sympy.nextprime(primes[-1]))

    print ("Found {} primes starting at {}".format(len(primes), start))
    
    return readString (start, primes)


if __name__ == "__main__":

    # Test String
    N = 140674
    C = 104
    testString = readPrimeString (N, C)
    print (testString)
