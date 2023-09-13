# SnakeAI-DQN
Snake game with agent controlled by deep Q learning algorithm

# Game Interface and Agent Training

This repository contains code for both the game interface and training an agent from scratch.

## Game Interface (main.py)

To run the game interface, execute the following command:

```bash
python main.py
```

This will start the game interface, allowing you to interact with the game.

## Agent Training (train_agent.py)
To train an agent from scratch, use the following command:

```bash
python train_agent.py
```
Running this command will initiate the agent training process, starting from scratch.

The training is divided into 2 stages:
first the agent learns about the goal of the game and the rules of moving in the environment, the agent is re-trained after each move.
Rewards:
- snake eats food: reward = 10
- snake hits a boundary or itself: reward = -10
- regular movement: reward = 0  
The second stage begins when the score = 20 this stage is to speed up the training process, now the agent knows how to move in the environment so the agent is only trained when it eats food or hits something.

  <p align="center">
  <b> Deep Q-learning agent after training <b/>   
  
  ![](https://github.com/Passonei/SnakeAI_DQL/blob/main/gifs/SnakeAgentDQL.gif)  
  </p>