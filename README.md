# DAMA-IT
# How to run the Application
<br>
  - be sure to have python installed on your device (if not it's suggested to install the latest version) <br>
  - be sure to have docker installed on your device (if not it's suggested to install the latest version) <br>
  - clone the repository (git clone [URL of the repo]>) <br>
  - create in the root directory a file called .env that must be fullfilled as follows:<br>
      RABBITMQ_USERNAME=myuser <br>
      RABBITMQ_PASSWORD=mypassword <br>
      RABBITMQ_IP= ... [the IP address of your rabbit container in docker] <br>
      MYSQL_USERNAME=root <br>
      MYSQL_PASSWORD=root <br>
      MYSQL_DB=db <br>
      EMAIL= ... [the email address you want] <br>
      EMAIL_PASSWORD= ... [the password of the email address] <br>
  - navigate the imports in the client.py file and install all the libraries you've not installed yet <br>
  - run the command [docker-compose up] to build up and run all the needed containers <br>
  - run python ./client.py to start one client interface <br>
<br>
what follows is an overview of what is in place once you've done all the steps above <br>
<p align="center">
  <img src="architecture.png" width="700" title="hover text">
</p>
