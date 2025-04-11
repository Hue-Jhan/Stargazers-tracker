# Stargazers-checker
Simple script that tells you if a given user has new stargazers and in which repos.

# 💻Code

Once entered a new github username, the code will create a json file where all data about all users will be stored. Then throught the github api the code will fetch the list of stargazers for every repository of that user, if the user is new to the dataset, all the stargazers are considered new and will then be displayed, if the user is already in the datababase, then the code will simply display the stargazers not present in the file, which will also be updated with the new ones.

Here is an example:


![star1](https://github.com/user-attachments/assets/b808c662-bb7c-4869-bed8-19290e981380)

