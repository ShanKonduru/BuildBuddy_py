REM curl -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d "{\"model\": \"llama2:latest\", \"prompt\": \"Hello, how are you?\"}"

curl -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d "{\"model\": \"llama3.2\", \"messages\": [{ \"role\": \"user\", \"content\": \"why is the sky blue?\" }]}"
