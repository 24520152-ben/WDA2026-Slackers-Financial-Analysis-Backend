import requests
import json

def test(url: str, ticker: str, length: str) -> None:
    url = url
    
    payload = {
        "ticker": ticker,
        "length": length,
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() 
        
        data = response.json()
        
        print(data["technical_analysis"])
        
    except requests.exceptions.RequestException as e:
        print(str(e))
        if response is not None: # type: ignore
            print(f"Exception detail: {response.text}") # type: ignore

if __name__ == "__main__":
    test(url="http://127.0.0.1:8000/technical_analysis/", ticker="VCB", length="3M")