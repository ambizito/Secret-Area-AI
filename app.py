from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# URL do endpoint da API do Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Altere conforme necessário

def ask_ollama(prompt):
    """
    Envia o prompt para o Ollama e retorna a resposta.
    Ajuste o payload e o tratamento conforme a especificação da API do Ollama.
    """
    payload = {
        "prompt": prompt,
        "model": "deepseek-r1:14b"  # Ajuste se necessário
        # Adicione outros parâmetros se necessário
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Gera exceção se ocorrer erro
        try:
            data = response.json()
            # Supondo que a resposta do Ollama contenha a chave 'response'
            return data.get("response", "Resposta não encontrada.")
        except ValueError as e:
            return f"Erro ao processar a resposta do Ollama: {e}\nResposta: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Erro ao chamar o Ollama: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Nenhum prompt fornecido."}), 400
    answer = ask_ollama(prompt)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    # O servidor ficará acessível na LAN (0.0.0.0) na porta 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
