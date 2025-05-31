# Project Documentation: Softy, a Voice-Activated Project Management Chatbot

## 1. Introduction

Softy is a Python-based application designed to streamline project management through intuitive voice and text interactions. This system integrates speech-to-text and text-to-speech technologies with a robust chatbot, allowing users to efficiently manage projects, retrieve information, and interact with the system using natural language. Whether you're creating a new project, checking its status, or seeking assistance, this application aims to provide a comfortable developing experience.

**Key Features:**

* **Speech-to-Text (STT):** Convert spoken language into text commands and queries.
* **Text-to-Speech (TTS):** Receive spoken responses from the chatbot.
* **Intelligent Chatbot:** Interact with a conversational AI to manage projects and retrieve information.
* **Project Management:** Create, view, and manage projects through the intuitive interface.
* **API Integration:** Potential for integration with external services to enhance project workflows.

## 2. Getting Started

This section guides you through setting up and running the Voice-Activated Project Management Chatbot.

### 2.1. Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x:** The application is built with Python.
* **`pip`:** Python's package installer, usually included with Python installations.

### 2.2. Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Marlu0/softies_project.git
    cd https://github.com/Marlu0/softies_project.git
    ```

2.  **Install Dependencies:**
    Navigate to the project's root directory and install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Vosk Model:**
    The `models/vosk-model-small-en-us-0.15/` directory should already contain the necessary Vosk speech recognition model. If it's missing or corrupted, you might need to download it separately from the Vosk website and place it in the specified directory.

### 2.3. Running the Application

To start the application, execute the `main.py` file from the `src/` directory:

```bash
python src/main.py
```

Once the application starts, it will typically open in your default web browser at an address like `http://127.0.0.1:5000/` or `http://localhost:5000/`.

## 3. User Interface Guide

The application's user interface is designed for ease of use, providing clear navigation and intuitive interactions.

### 3.1. Homepage (`templates/index.html`)

Upon launching the application, you will land on the homepage. This page serves as the central hub for accessing the main functionalities.

* **Navigation Bar:** Provides links to key sections like "Chat," "New Project," "View Projects," and "Settings."
* **Welcome Message:** Introduces the application and its purpose.
* **Quick Actions:** May include shortcuts to common tasks or information.

### 3.2. Chat Interface (`templates/chat.html`)

This is where you interact with the chatbot, either through voice or text.

* **Microphone Button:** Click to enable speech-to-text input. Speak your query or command clearly.
* **Text Input Field:** Type your message to the chatbot.
* **Chat History:** Displays your conversation with the chatbot, showing both your input and the chatbot's responses.
* **Send Button:** Submits your text input to the chatbot.

**Interacting with the Chatbot:**

* **To ask a question:** "What is the status of Project X?"
* **To create a task:** "Create a task called 'Review documentation' for Project Y."
* **To get help:** "Help me with project creation."

### 3.3. New Project (`templates/create_project.html`)

This page allows you to create new projects within the system.

* **Project Name:** Enter a unique name for your project.
* **Description:** Provide a brief description of the project's goals and scope.
* **Project Type:** Select the type of project (e.g., Java, C++, Python, General). This might influence specific project templates or configurations.
* **Start Date / End Date:** Define the project's timeline.
* **Submit Button:** Creates the new project and adds it to your project list.

### 3.4. View Projects (`templates/view_projects.html`)

This page displays a list of all your active and completed projects.

* **Project List:** Shows a table or list of projects with key details like name, type, and status.
* **Search/Filter Options:** (If implemented) Allows you to search for specific projects or filter by status, type, etc.
* **Project Details Link:** Click on a project to view more detailed information about it.

### 3.5. Project Details (`templates/project_details.html`)

This page provides a comprehensive overview of a selected project.

* **Project Overview:** Displays the project name, description, dates, and status.
* **Tasks/Milestones:** (If implemented) Lists tasks or milestones associated with the project, their status, and assigned members.
* **Team Members:** (If implemented) Shows the team members assigned to the project.
* **Activity Log:** (If implemented) Displays a history of actions taken on the project.

### 3.6. Settings (`templates/settings.html`)

The settings page allows you to configure various aspects of the application.

* **Speech Settings:** Adjust microphone sensitivity, voice output preferences, etc.
* **API Key Management:** (If applicable) Configure API keys for external service integrations.
* **User Preferences:** (If applicable) Set personal preferences for notifications or display.

## 4. Advanced Features

*(This section will be expanded as advanced functionalities are implemented.)*

* **Custom Chatbot Commands:** In future versions, users may be able to define custom commands or phrases for the chatbot to recognize and execute specific actions.

## 6. Troubleshooting

This section provides solutions to common issues you might encounter.

* **"Microphone not detected" error:**
    * **Solution:** Ensure your microphone is properly connected and enabled in your operating system's settings. Check browser permissions for microphone access.
* **Speech-to-text not working accurately:**
    * **Solution:** Speak clearly and at a moderate pace. Ensure there is minimal background noise. Verify the Vosk model is correctly loaded in `models/vosk-model-small-en-us-0.15/`.
* **Application not starting:**
    * **Solution:** Check the console output for error messages. Ensure all dependencies from `requirements.txt` are installed. Verify that Python 3.x is being used to run the script.
* **"API key invalid" or similar errors:**
    * **Solution:** If using external APIs, ensure your API keys are correctly configured in the settings or hardcode them directly.
* **Database connection issues:**
    * **Solution:** Verify the database configuration in `src/database.py`. Ensure the database server is running and accessible.
