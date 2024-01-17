# SpaceWiki
The SpaceWiki API is designed to provide access to space-related content from our SpaceWiki platform. This API allows you to retrieve information about planets, stars, solar systems, and space-related vocabulary. 

## How to Install and Run the Project
1. Clone the project
    ```
    git clone https://github.com/Jamescog/SpaceWiki.git
    
    cd SpaceWiki
    ```
2. Create a virtual environment
    - For Windows
    ```
    pip install virtualenv # if you don't have virtualenv installed

    python -m venv venv

    venv\Scripts\activate
    ```
    - For Linux
    ```
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies
    ```
    pip install -r requirements.txt
    ```

4. Run the server
    ```
    py src\main.py -> for Windows

    python src/main.py -> for Linux
    ```

5. Access Documentation and Execute requests
    Fire up your favorite browser and visit either [this]('http://localhost:8000/docs') or [this]('http://localhost://localhost:8000/redoc').

Happy Coding! :rocket:
