# **🚗 Vehicle Information System**  
**AI-Powered CLI for Vehicle Data Management**  

---

## **📌 Overview**  
The **Vehicle Information System** is a **command-line application** that uses **AI agents** to interact with users, collect vehicle data (brand, model, fuel type, etc.), and retrieve matching vehicles from a database. It leverages **Model Context Protocol (MCP)** for structured client-server communication and **LangChain** for natural language processing.  

### **✨ Key Features**  
✅ **AI-Powered Queries** – Ask questions naturally (e.g., *"Show me red Toyotas from 2020"*)  
✅ **Multi-Language Support** – Works in **English & Portuguese**  
✅ **Rich Terminal UI** – Formatted output with **Typer + Rich**  
✅ **Database Abstraction** – **SQLAlchemy** models with **Faker**-based seeding  
✅ **MCP Protocol** – Standardized **client-server** communication  

---

## **⚙️ Requirements**  
Before running, ensure you have:  

- **Python 3.12**  
- **Ollama** (for local LLM inference)
- **Pipenv** (for dependency management)  

### **📦 Installation**  
1. **Clone the repository**  
   ```bash
   git clone https://github.com/eacassecasse/c2s-virtual-agents.git
   cd c2s-virtual-agents
   ```

2. **Set up a virtual environment**  
   ```bash
   pipenv shell
   pipenv install
   ```

3. **Install Ollama & pull a model**  
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2  # or mistral, gemma, etc.
   ```

4. **Seed the database (optional)**  
   ```bash
   python -m scripts.seed
   ```

---

## **🚀 Usage**  

### **1. Start MCP Server**  
```bash
python -m app.server.server  # Runs on port 8000
```

### **2. Interactive Mode (AI Agent)**  
Start a natural-language conversation:  
```bash
python -m app.cli.console
```
**Example Queries:**  
- `Show me blue Hondas`  
- `List electric vehicles from 2022`  
- `Mostrar carros com placa ABC-1234` (Portuguese)

---

[//]: # (## **🎥 Demo**  )

[//]: # ([![Demo Video]&#40;https://img.youtube.com/vi/VIDEO_ID/0.jpg&#41;]&#40;https://youtu.be/VIDEO_ID&#41;  )

[//]: # ()
[//]: # (*&#40;Click to watch a quick demo of the system in action!&#41;*  )

---

## **🛠️ Development**  

### **Project Structure**  
```
c2s-virtual-agents/
├── app/
│   ├── cli/              # CLI commands & prompts
│   ├── core/              # Core features like the AI Agent
|   |-- db/                # Contains database related files
│   ├── models/           # SQLAlchemy models
│   └── server/            # MCP protocol logic
|   |-- storage/           # Storage engine management
├── scripts/
│   └── seed.py           # Fake data generation
├── tests/                # Unit tests
└── README.md
|__ .env                   # Environment variables
```

### **Testing**  
Run unit tests:  
```bash
python -m unittest discover
```

### **Contributing**  
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/new-feature`)  
3. Commit changes (`git commit -m "feat: add new filter option"`)  
4. Push to branch (`git push origin feature/new-feature`)  
5. Open a **Pull Request**  

---

## **📜 License**  
MIT © Edmilson Cassecasse

---

### **Why Use This?**  
🔹 **For Developers**: Clean architecture with **MCP** for scalable client-server interactions  
🔹 **For Data Teams**: Easily query & filter vehicle datasets  
🔹 **For AI Enthusiasts**: **LangChain + Ollama** integration for NLP-powered search  

**Try it now and explore vehicles like never before!** 🚀