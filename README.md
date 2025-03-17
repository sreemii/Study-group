study Group Coordinator API

Overview:
The Study Group Coordinator API helps users create, manage, and participate in study groups. It includes features such as group creation, session scheduling, resource sharing.

Tech Stack:
Backend: FastAPI
Database: SQLite + SQLAlchemy
Data Validation: Pydantic
Testing: Pytest
API Documentation: OpenAPI
Database Migrations: Manual (SQLAlchemy)

Installation:
1.Clone the Repository
git clone https://github.com/your-repo/study-group.git
cd study-group

2.Create and Activate a Virtual Environment
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows

3.Install Dependencies
pip install -r requirements.txt

4.Run the Application
uvicorn main:app --reload

API Endpoints
Users Management:
-Create User - POST /users/create
-Get All Users - GET /users/
-Get a User by ID - GET /users/{user_id}
-Update User Profile - PUT /users/update/{user_id}
-Delete a User - DELETE /users/delete/{user_id}

Authentication
-Register a User - POST /auth/register
-User Login - POST /auth/login

Study Groups Management
-Create a Study Group - POST /groups/create
-Get All Study Groups - GET /groups/
-Get Study Group by ID - GET /groups/{group_id}
-Join a Study Group - POST /groups/join/{group_id}
-Leave a Study Group - POST /groups/leave/{group_id}
-Update Study Group - PUT /groups/update/{group_id}
-Delete a Study Group - DELETE /groups/delete/{group_id}

Group Members
-Add User to a Group - POST /groups/add-user/{group_id}
-Remove User from a Group - DELETE /groups/remove-user/{group_id}/{user_id}

Study Sessions
-Create a Study Session - POST /sessions/create
-Get All Sessions - GET /sessions/
-Get Session by ID - GET /sessions/{session_id}
-update a Study Session - PUT /sessions/update/{session_id}
-Delete a Study Session - DELETE /sessions/delete/{session_id}

Resources
-Add Resource to a Group - POST /resources/create
-Get All Resources - GET /resources/
-Get Resource by ID - GET /resources/{resource_id}
-Update a Resource - PUT /resources/update/{resource_id}
-Delete a Resource - DELETE /resources/delete/{resource_id}

Error Handling:
{
  "error": "Error Type",
  "message": "Detailed error message"
}
