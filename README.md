# 371-project NumberGuesser
- Course: CMPT 371 - Data Communications & Networking
- Instructor: Mirza Zaeem Baig
- Semester: Spring 2026
- Group members:
  - Grant Deng | Student ID: 301586691 | email: gjd4@sfu.ca
  - Elijah Mangoyob Santos | Student ID: 301577116 | email: erm6@sfu.ca

## **Project Description: Multi-player Number Guessing Game**
- An interactive number guessing game with multiple simultaneous players.
- Connect to a game server, and guess randomly generated numbers over several pre-set rounds.
- Compete with other players and gain points based on how close your guess is. Most points win!
- Uses Python's socket library to establish a TCP interface.
- Uses Python's threading library to manage client connections.

## **Questions**
**How to handle multiple Clients at the same time**
- The server must support multiple players at once, requiring concurrency. Each client is handled in its own thread (handle_client), while the game logic runs in a separate thread (game_loop).

**How do we prevent Data Races, and keep data accurate?**
- Shared data such as scores and guesses must be synchronized to avoid inconsistencies when accessed by multiple threads. We used locks. Shared data structures (clients, guesses, points, names) are protected using threading.lock.

**How to wait for other clients**
- The system must handle late or missing guesses while ensuring fairness across players with different network conditions. It also requires for coordination of which we used timers and locks. Additionally, a threading.Event (guess_event) is used to coordinate players.

## **Limitations**
- Running with a large amount of clients connecting using threads could cause performance issues. No player max capacity set, and large player numbers have not been tested.
- People disconnecting mid-game cannot reconnect
- No security, all data is sent as normal plaintext and is not encrypted.

## **Video Demo**
Our video demo shows the code running, establishing connections, data exchange (through gameplay), and termination of clients and the server.<br/>
[https://www.youtube.com/watch?v=vZ2nY_vixc4](https://www.youtube.com/watch?v=vZ2nY_vixc4)

## **Prerequisites**
Requirements:
- Python 3.10 or higher
- No external libraries are required to run this application (we only used built-in Python libraries)
- A terminal interface (to run the application)

## **Step by Step How To Guide**
**DISCLAIMER: IT IS RECOMMENDED TO READ EACH STEP BEFORE ATTEMPTING AND ONLY PROCEED TO THE NEXT SECTION AFTER COMPLETING EACH STEP OF THE PREVIOUS SECTION**
### **1. Starting up the server**
1) Open the repository folder in a terminal then run the following command:
```bash
python server.py
```
### **2. Connecting each player (clients)**
1) To connect **player 1**, open the repository folder in a **new terminal** and run:
```bash
python client.py
```
2) To connect **player 2**, open the repository folder in a **new terminal** and run:
```bash
python client.py
```
### **3. Navigating each client terminal**
1) In each instance of **client.py** you will be greeted with this message:
```bash
Enter your name:
```
2) Type a name in the prompt **for each client.py** instance and **press enter**.
### **4. Playing the game**
1) Once you have setup both instances of **client.py** you will be prompted with:
```bash
You have 10 seconds! Guess a number between 1 and 100:
```
2) You will have 10 seconds to type a number and when you finishing typing a number **press enter**.
3) Once the game is finished, **each client will disconnect and shut down**
### **5. Shutting down the server**
1) To shut down the server when the game finishes, **press CTRL-C**

## **References**
To learn about Python's socket and threading libraries, we used their respective documentations:
- [Python socket library documentation](https://docs.python.org/3/library/socket.html)
- [Python threading library documentation](https://docs.python.org/3/library/threading.html)

GenAI usage:
- We used GenAIs to aid our understanding of the referenced documentations.
