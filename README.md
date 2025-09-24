
# 🎮 ResolutionChanger

A modern tool in PyQt6 for changing the screen resolution before launching a game from Steam, and automatically restoring it when the game is closed.

## 🔍 Features

- Modern and clean UI using PyQt6
- Automatic resolution management
- Steam games integration
- Custom resolution support
- Automatic resolution restoration
- Real-time logging
- 4:3 aspect ratio calculation

## 🧰 Requirements

- Python 3.11 or above
- Steam installed
- Windows operating system

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/xKineticK/ResolutionChanger.git
cd ResolutionChanger
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## ▶️ Usage

Run the application:
```bash
python run.py
```

## 🏗️ Project Structure

```
ResolutionChanger/
├── src/
│   ├── models/          # Data and business logic
│   ├── views/           # UI components
│   ├── presenters/      # Application logic
│   ├── services/        # External services integration
│   └── utils/           # Utility functions and classes
├── config/             # Configuration files
├── resources/          # Application resources
└── tests/             # Unit tests
```

## 🛠️ Development

This project follows the MVP (Model-View-Presenter) architecture pattern:

- **Models**: Handle data and business logic
- **Views**: Handle user interface
- **Presenters**: Handle application logic and user input
- **Services**: Handle external integrations
- **Utils**: Common utilities and helpers

## 💡 Credits

Developed by xKineticK with ♥ and a little bit of madness for aspect ratio.
