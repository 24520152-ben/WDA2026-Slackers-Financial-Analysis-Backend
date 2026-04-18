import requests
import json

def test(url: str, ticker: str) -> None:
    url = url
    
    payload = {
        "ticker": ticker,
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() 
        
        data = response.json()
        
        print(data["fundamental_analysis"])
        
    except requests.exceptions.RequestException as e:
        print(str(e))
        if response is not None: # type: ignore
            print(f"Exception detail: {response.text}") # type: ignore

if __name__ == "__main__":
    test(url="http://127.0.0.1:8000/fundamental_analysis/", ticker="VCB")