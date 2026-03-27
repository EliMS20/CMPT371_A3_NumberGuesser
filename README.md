# 371-project NumberGuesser
- Grant Deng 301586691 gjd4@sfu.ca
- Elijah Mangoyab Santos 301577116 erm6@sfu.ca

## **Multi-player Number Guessing Game**
- An interactive number guessing game with multiple simultaneous players.
- Connect to a game server, and guess randomly generated numbers over several pre-set rounds.
- Compete with other players and gain points based on how close your guess is. Most points win!
## **Questions**
- How to handle multiple Clients at the same time
- How to prevent Data Races, and keep data accurate
- How to wait for other clients
## **Limitations**
- Running with a large amount of clients connecting using threads could cause performance issues. No player max capacity set, and large player numbers have not been tested.
- People disconnecting mid-game cannot reconnect
- No security, all data is sent as normal plaintext and is not encrypted.
## **WorkFlow**
## **Step by Step How To Guide**
1) Begin by cloning this repository **or** downloading this repository as a zip file directly from github.
```bash
git clone https://github.com/your-username/your-repo.git
```
2) Open the repository folder in your terminal then run the following command:
```bash
python server.py
```
3) Open the repository folder inside two additional terminal instances and run the following command in each terminal:
```bash
python client.py
```
4) In each instance of **client.py** you will be greeted with this message:
```bash
Enter your name:
```
5) Type in a name in the prompt for each **client.py** instance and **press enter**.
6) Once you have setup both instances of **client.py** you will be prompted with:
```bash
You have 10 seconds! Guess a number between 1 and 100:
```
7) You will have 10 seconds to type a number and when you finishing typing a number **press enter**.
8) **IF YOU WANT TO CLOSE A CLIENT: PRESS CTRL-C**
