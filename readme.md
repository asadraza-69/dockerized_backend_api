# Blog Website with Django

This is a Authentication project built using the Django web framework and restapi. The project allows users to signin, signup signout, add to cart and product search. It also includes user authentication for creating and managing accounts.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [LocalEnviroment](#localenviroment)
- [DockerEnviroment](#dockerenviroment)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started
local_setting.py is use to run project on local env
### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- pip package manager

### Installation

0. Clone the repository:

   ```shell
   git clone git@github.com:asadraza-69/dockerized_backend_api.git

### localenviroment

1. Creating env and activating env :
    ```shell
    python3 -m venv docker_backend_env
    source bin\activate

2. Navigate to the project directory:
    ```shell
    cd dockerized_backend_api

3. Install the project dependencies:
    ```shell
    pip install -r requirements.txt

4. Apply migrations:
    ```shell
    python manage.py migrate

5. Applying fixtures:
    ```shell
    python manage.py loaddata initial_data

6. Start the development server:
    ```shell
    python manage.py runserver --settings  backend_api.local_settings

### dockerenviroment
1. First run this command for update your os dependencies:
    ```shell
    sudo apt-get update

2. Fetches the Docker package from the repositories and installs it on your system:
    ```shell
    sudo apt install docker.io

3. Download and install the Docker package from the Snap Store, which is a central repository for snap packages:
    ```shell
    sudo snap install docker

4. Docker version:
    ```shell
    docker --version

5. Download any docker image/container:
    ```shell
    sudo docker run (image name)

6. Available docker image/container in your system:
    ```shell
    sudo docker ps -a

7. Install all dependencies in your Docker that your project need:
    ```shell
    sudo docker build -t myapp 

8. Command to build docker-compose file:
    ```shell
    sudo docker-compose up --build

9. you check all images in your system:
    ```shell
    sudo docker ps -a

    output:
    CONTAINER ID           IMAGE                       COMMAND                  CREATED          STATUS                      PORTS     NAMES
    9ff0241e7711     django_project_lambda-web   "bash -c 'python man…"   19 seconds ago   Exited (1) 16 seconds ago                myapp

10. For restart the docker container run this command:
    ```shell    
    sudo docker-compose restart

11. If you want to stop the running docker container run this command:
    ```shell
    sudo docker-compose down

12. If you want to start docker container run this command:
    ```shell    
    sudo docker-compose up


### Usage
User can signup.
User can signin.
User can signout.
User can search any product.
User can add product to cart.
Customize the project by modifying templates, adding styles, or extending functionality as needed.

### Contributing
Contributions are welcome! Here's how you can get involved:

Fork the project on GitHub.
Create a new branch with a descriptive name for your feature or bug fix.
Make your changes and test thoroughly.
Submit a pull request with a clear description of your changes and why they are necessary.

### License
This project is licensed under the MIT License - see the LICENSE file for details.


In this example `README.md` file, we provide an overview of the project, instructions for installation and usage, guidelines for contributing, and information about the project's license. You should replace placeholders such as `your-username` with your actual GitHub username and adapt the content to your project's specifics.
