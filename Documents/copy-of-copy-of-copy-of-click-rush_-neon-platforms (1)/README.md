# 🎮 Click Rush - Neon Platforms

> Um jogo interativo de plataformas em tempo real com múltiplas fases, power-ups e sistema de leaderboard

[![React](https://img.shields.io/badge/React-19.2-61DAFB?logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6?logo=typescript)](https://www.typescriptlang.org)
[![Vite](https://img.shields.io/badge/Vite-6.2-646CFF?logo=vite)](https://vitejs.dev)

## 🌟 Características

- **4 Fases Únicas** - Cada uma com tema, cor e dificuldade próprios
  - 🌳 Pomar Digital
  - 🦁 Safari Selvagem
  - 🏎️ Garagem Turbo
  - 🎀 Doce Lar

- **Sistema de Power-ups** - Potencialize sua experiência de jogo
  - Shield (Escudo)
  - Slow Motion
  - Multiplicadores de pontos

- **Mecânicas Avançadas**
  - Sistema de combos dinâmico
  - Efeitos visuais e sonoros
  - Múltiplas vidas e moedas coletáveis
  - Progressão de dificuldade gradual

- **Multiplayer Social**
  - Leaderboard global
  - Sistema de skins customizáveis
  - Estatísticas detalhadas

## 🚀 Quick Start

**Pré-requisitos:**
- Node.js 18+

**Instalação:**

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/click-rush-neon-platforms.git
cd click-rush-neon-platforms

# Instalar dependências
npm install

# Configurar API key (opcional - para recursos IA)
echo "VITE_GEMINI_API_KEY=sua_chave_aqui" > .env.local

# Iniciar servidor de desenvolvimento
npm run dev
```

Abra [http://localhost:5173](http://localhost:5173) no seu navegador.

## 🛠️ Tecnologias

- **Frontend:** React 19 + TypeScript
- **Build:** Vite 6
- **Styling:** Tailwind CSS
- **API:** Gemini AI (para features avançadas)
- **Audio:** Web Audio API
- **Database:** Firebase/Supabase ready

## 📁 Estrutura do Projeto

```
├── components/          # Componentes React
│   ├── Game.tsx        # Lógica principal do jogo
│   ├── Platform.tsx    # Componente de plataforma
│   ├── PowerUp.tsx     # Sistema de power-ups
│   └── ...
├── services/           # Serviços
│   ├── audioService.ts # Gerenciador de áudio
│   ├── geminiService.ts# Integração com IA
│   ├── databaseService.ts
│   └── wordBank.ts
├── types.ts            # Tipos TypeScript
└── App.tsx             # Componente raiz
```

## 📦 Scripts Disponíveis

```bash
npm run dev      # Inicia servidor de desenvolvimento
npm run build    # Build para produção
npm run preview  # Preview da build
```

## 🎯 Como Jogar

1. Escolha seu nome de jogador
2. Clique nas plataformas para ganhar pontos
3. Colete moedas para poder-ups
4. Progresse através das fases
5. Compete no leaderboard global

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👥 Autor

Desenvolvido com ❤️ 

---

**Divirta-se jogando! 🎮✨**
