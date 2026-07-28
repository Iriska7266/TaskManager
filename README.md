# Task Manager (terminal version)

---
To run the program you need installed PostgreSQL
---
## DB initialization
1. Go to PostgreSQL\bin folder.
2. Run `psql -U -user_name -d tasks_system_db < path_to_db_dump.sql`. db_dump.sql is located in database folder, enter you DB name after `-U`.
3. Created database already contains test data with 1 user and 2 tasks. Test account login and password: Test Test.
---
## Dotenv preparing
1. Open .env.example and edit all information you need (user_name, password, host, port). Don't need to edit DB_URL.
2. Rename this file to .env.
---
## Final step
Install all requirements from requirements.txt.
That's all, now you can run main.py file and use the program

Database also includes actions_log table, which stores history of all data manipulations, it can't be seen from task manager, but if you want you can observe it in your DBMS
