# Real-time-Chat-App

# 📅 Week 1 Milestone: Environment Setup & Flask Foundation

In this initial phase, I focused on establishing a professional development environment and building the core "Skeleton" of the web application.

### **Key Achievements:**
* **Environment Configuration:** Initialized a Python virtual environment (`venv`) to manage dependencies and ensure a clean, isolated workspace for the project.
* **Flask Framework Initialization:** Successfully installed and configured **Flask**, setting up the backend server and basic routing logic to handle web requests.
* **Template Rendering:** Created the primary `@app.route('/')` to serve the initial `index.html` landing page, verifying that the backend could communicate correctly with the frontend.
* **Project Architecture:** Organized the directory structure into `templates/` and `static/` folders, following industry-standard Flask practices for better code scalability.
* **Frontend Boilerplate:** Developed the first iteration of the UI with an HTML5 boilerplate to verify the server was rendering layouts and metadata properly.

# 📅 Week 2 Milestone: User Interface & Frontend Styling

The focus for the second week was on transforming the basic HTML skeleton into a user-friendly and visually appealing interface.

### **Key Achievements:**
* **CSS Integration:** Created a dedicated stylesheet to define the visual language of the app, including custom fonts and a responsive color palette.
* **Layout Design:** Implemented a "Main Container" system to separate the chat window from the user list, improving the overall user experience (UX).
* **Form Development:** Built the initial Login and Registration forms to prepare for future user authentication features.
* **UI Responsiveness:** Applied basic CSS Flexbox properties to ensure the chat interface adjusts correctly to different screen sizes 

# 📅 Week 3 Milestone: Real-time Communication with Socket.io

This week marked the most critical technical jump: moving from a static website to a real-time communication platform.

### **Key Achievements:**
* **Socket.io Implementation:** Integrated `Flask-SocketIO` on the backend and the Socket.io client library on the frontend to enable bi-directional communication.
* **Event Handling:** Developed the first `message` event listeners to "shout" messages from the server to all connected clients instantly.
* **DOM Manipulation:** Wrote JavaScript logic to dynamically inject new messages into the chat window without requiring a page refresh.
* **Connection Testing:** Verified successful handshake protocols between the client and server through the terminal logs.

# 📅 Week 4 Milestone: Room Logic & User Sessions

The goal for Week 4 was to move beyond a single global chat and allow for organized, private conversations through "Rooms."

### **Key Achievements:**
* **Join/Leave Logic:** Implemented `join_room` and `leave_room` functions to isolate message traffic between different chat groups.
* **Session Management:** Utilized Flask `session` objects to securely track usernames and maintain user identity across different pages.
* **Dynamic Room Switching:** Created a frontend dropdown menu that allows users to jump between "General," "Internship-Group," and "Tech-Support" seamlessly.
* **State Tracking:** Developed a dictionary system to track which users are currently active in specific rooms.

# 📅 Week 5 Milestone: Enhanced UX & Error Handling

During Week 5, I focused on polishing the user experience and squashing technical bugs that appeared during room transitions.

### **Key Achievements:**
* **User List Updates:** Implemented a real-time "Online Users" sidebar that updates automatically whenever someone enters or exits a room.
* **Bug Fixes:** Resolved a critical issue where the `body` tag in `index.html` was not rendering correctly, ensuring the login screen was visible to all users.
* **Auto-Scroll Logic:** Added JavaScript to ensure the chat window automatically scrolls to the latest message, keeping the conversation fluid.
* **Status Messages:** Integrated system notifications (e.g., "Sahil has entered the room") to provide feedback on user activity.

# 📅 Week 6 Milestone: Database Persistence & Authentication

In this phase, I transitioned the application from a temporary session-based chat to a permanent system by integrating a robust database layer.

### **Key Achievements:**
* **SQLAlchemy Integration:** Successfully connected a **SQLite** database to the Flask app, allowing for structured data storage of users and messages.
* **Message Storage:** Implemented a `Message` model to record the username, room, text content, and exact timestamp for every interaction.
* **History Loading:** Developed a `load_history` event that queries the database whenever a user joins a room, delivering previous conversations instantly to the UI.
* **Authentication Security:** Added a registration and login system using `werkzeug.security` to hash passwords, ensuring user data is protected.
* **Bug Fixes:** Resolved critical issues where the `body` tag was empty and fixed variable definition errors in the room-tracking logic.
* **Version Control:** Managed repository sync conflicts and pushed the updated architecture to GitHub using GitHub Desktop.