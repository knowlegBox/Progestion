# Progestion 🚀

[![Language](https://img.shields.io/badge/language-English-blue.svg)](#)
[![Framework](https://img.shields.io/badge/Framework-Django%205.1-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Progestion** is a modern, all-in-one business management solution designed for small and medium-sized enterprises (SMEs/TPE). It simplifies administrative tasks such as invoicing, customer management, and tax tracking through a sleek and responsive interface.

[Français Version (Version Française)](README.fr.md)

---

## ✨ Key Features

- 📑 **Invoicing & Billing**: Easily create, manage, and export professional invoices (PDF generation powered by WeasyPrint).
- 👥 **Customer & Supplier CRM**: Centralize your contacts, track interactions, and manage relationships.
- 📦 **Inventory & Product Management**: Keep track of your products, stock levels, and suppliers.
- 💰 **Transaction Tracking**: Monitor your financial flows and transaction history.
- ⚖️ **Tax & Compliance**: Dedicated module for tracking taxes and regulatory requirements.
- ⚡ **Modern Stack**: Built with Django 5, HTMX for dynamic interactions, and Tailwind CSS for a premium look.

## 🛠️ Technology Stack

- **Backend**: Python 5.1+, Django 5.x
- **Frontend**: Tailwind CSS, HTMX
- **Data Processing**: Pandas, OpenPyXL
- **PDF Generation**: WeasyPrint
- **Database**: SQLite (default), PostgreSQL (recommended for production)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js (for Tailwind CSS)
- `pip` or `poetry`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Progestion.git
   cd Progestion/backend
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirment.txt
   ```

4. **Run migrations**:
   ```bash
   python src/manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python src/manage.py runserver
   ```

6. **Access the application**:
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Security

If you discover a security vulnerability, please refer to our [SECURITY.md](SECURITY.md).
