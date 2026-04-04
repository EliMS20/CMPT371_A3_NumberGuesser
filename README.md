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
## **Video Demo**
[https://www.youtube.com/watch?v=vZ2nY_vixc4](https://www.youtube.com/watch?v=vZ2nY_vixc4)
## **Step by Step How To Guide**
**DISCLAIMER: IT IS RECOMMENDED TO READ EACH STEP BEFORE ATTEMPTING AND ONLY PROCEED TO THE NEXT SECTION AFTER COMPLETING EACH STEP OF THE PREVIOUS SECTION**
### **1. Cloning Repo**
1) Begin by cloning this repository **or** downloading this repository as a zip file directly from github.
```bash
git clone https://github.com/your-username/your-repo.git
```
### **2. Starting up the server**
1) Open the repository folder in a terminal then run the following command:
```bash
python server.py
```
### **3. Connecting each player (clients)**
1) To connect **player 1**, open the repository folder in a **new terminal** and run:
```bash
python client.py
```
2) To connect **player 2**, open the repository folder in a **new terminal** and run:
```bash
python client.py
```
### **4. Navigating each client terminal**
1) In each instance of **client.py** you will be greeted with this message:
```bash
Enter your name:
```
2) Type a name in the prompt **for each client.py** instance and **press enter**.
### **5. Playing the game**
1) Once you have setup both instances of **client.py** you will be prompted with:
```bash
You have 10 seconds! Guess a number between 1 and 100:
```
2) You will have 10 seconds to type a number and when you finishing typing a number **press enter**.
3) Once the game is finished, **each client will disconnect and shut down**
### **6. Shutting down the server**
1) To shut down the server when the game finishes, **press CTRL-C**
