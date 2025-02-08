const express = require('express');
// Node 18+ já possui global fetch; caso contrário, use "node-fetch"
const app = express();
const port = 5000;

app.use(express.json());
app.use(express.static('public'));

const OLLAMA_API_URL = "http://localhost:11434/api/generate";

async function askOllama(prompt) {
    const payload = {
        prompt: prompt,
        model: "deepseek-r1:14b" // ajuste se necessário
    };
    try {
        const response = await fetch(OLLAMA_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const text = await response.text();
        // Divide a resposta pelos saltos de linha (assumindo que cada linha seja um JSON)
        const lines = text.split('\n').filter(line => line.trim() !== '');
        let combinedResponse = '';
        for (let line of lines) {
            try {
                const obj = JSON.parse(line);
                combinedResponse += obj.response;
                if (obj.done) break;
            } catch (e) {
                console.error("Erro ao fazer parse de uma linha:", e);
            }
        }
        return combinedResponse || "Resposta não encontrada.";
    } catch (error) {
        return `Erro ao chamar o Ollama: ${error}`;
    }
}

app.post('/api/ask', async (req, res) => {
    const { prompt } = req.body;
    if (!prompt) return res.status(400).json({ error: "Nenhum prompt fornecido." });
    const answer = await askOllama(prompt);
    res.json({ answer });
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
