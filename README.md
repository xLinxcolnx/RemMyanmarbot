# 🤖 Rem Bot | Myanmar's Smart Schedule Assistant

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/RemMyanmarbot)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Rem Bot** is a specialized Telegram assistant designed to help users in Myanmar stay on top of their schedules. In an environment where Telegram is the primary hub for entertainment and social interaction, Rem Bot bridges the gap between relaxation and productivity.

## 📊 The "Why": Data-Driven Insights
Before writing a single line of code, I conducted a survey of **71 participants** to understand the scheduling habits of Myanmar users. Using **Power BI**, I uncovered key "pain points":

* **The Target Audience:** My research showed that the **18–24 age group** is the most active but also the most likely to miss scheduled tasks.
* **The Distraction Factor:** Users reported missing schedules specifically while **watching movies or chatting** within Telegram.
* **The Solution:** Users indicated a need for in-app notifications that bypass the "VPN fatigue" often associated with other social platforms.

> **Key Finding:** Standard phone alarms are easily ignored during full-screen media usage. Rem Bot provides native Telegram alerts that appear exactly where the user is already spending their time.

---

## ✨ Key Features
Rem Bot isn't just a simple timer; it's a personalized notification system:

* **☀️ Morning Summaries:** Receive a daily breakdown of your tasks every morning at a time you choose (default 07:00 AM).
* **⏰ Proactive Alerts:** Get reminded **10 to 30 minutes before** a task starts to ensure you have time to prepare.
* **🌍 Timezone Intelligent:** Built-in support for global timezones, including specific mapping for Myanmar users to ensure precision.
* **🛠️ Full CRUD Capability:** Easily `/set`, `/view`, `/edit`, and `/delete` your schedules through an intuitive interface.

---

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Framework:** `python-telegram-bot`
* **Data Persistence:** JSON-based local database (`rems.json`) for lightweight performance
* **Analysis:** Power BI & Excel (Market Research Phase)

---

## 🚀 Getting Started

### Commands
| Command | Description |
| :--- | :--- |
| `/start` | Setup your timezone and notification preferences |
| `/set` | Add a new schedule with date, time, and description |
| `/view` | See today's upcoming tasks and future reminders |
| `/edit` | Update an existing schedule description |
| `/delete` | Remove a schedule from your list |
| `/setting` | Change your morning summary or reminder lead-time |

### Installation (For Developers)
1. Clone the repo:
   ```bash
   git clone [https://github.com/yourusername/rem-bot.git](https://github.com/yourusername/rem-bot.git)
