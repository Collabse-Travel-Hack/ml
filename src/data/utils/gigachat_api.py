import requests


class GigachatAPI:
    def __init__(self, host):
        self.base_url = host

    def ask(self, system_msg, prompt_msg):
        url = f"{self.base_url}/gigachat/ask"
        payload = {
            "system_msg": system_msg,
            "prompt_msg": prompt_msg
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Проверяем, что запрос был успешным

            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None