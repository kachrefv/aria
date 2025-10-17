# 🌀 aria - Achref Riahi AI Assistant


[![PyPI version](https://img.shields.io/pypi/v/aria-cli.svg)](https://pypi.org/project/aria-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**aria** is an intelligent CLI + TUI framework that understands your coding goals, plans step-by-step strategies, and generates production-ready code - all in your terminal.

## ✨ Features

- 🧠 **AI-Powered Task Decomposition** - Break complex projects into executable subtasks
- 🎨 **Beautiful TUI Interface** - Navigate and manage projects visually
- 🏗️ **Smart Scaffolding** - Generate boilerplate for Next.js, Flask, Spring Boot, and more
- 🔌 **Plugin System** - Extensible architecture for new frameworks and tools
- 📊 **Progress Tracking** - Visualize your project completion status
- 🤖 **AI Reasoning Log** - See the AI's thought process in real-time

## 🚀 Quick Start

```bash
pip install aria-cli

# Set your AI API key
export DEEPSEEK_API_KEY="your-key-here"

# Create a new project plan
aria decompose "Build an AI-powered ecommerce platform with Next.js and Stripe"

# View in beautiful TUI
aria view plan.json

# Generate the project
aria run plan.json
