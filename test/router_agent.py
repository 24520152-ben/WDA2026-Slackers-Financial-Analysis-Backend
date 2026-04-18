import requests
import json

def test(url: str, message: str) -> None:
    url = url
    
    payload = {
        "message": message,
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() 
        
        data = response.json()
        
        print(data["reply"])
        print(data["investment_analysis"])
        print(data["technical_analysis"])
        print(data["fundamental_analysis"])
        
    except requests.exceptions.RequestException as e:
        print(str(e))
        if response is not None: # type: ignore
            print(f"Exception detail: {response.text}") # type: ignore

if __name__ == "__main__":
    test(url="http://127.0.0.1:8000/chat/", message="Tôi có nên đầu tư vào VCB lúc này?")
    test(url="http://127.0.0.1:8000/chat/", message="Tôi đang buồn quá, bạn có cách nào giúp tôi vui lên không?")