import random
import torch
from models import *
from aiGame import AIGame
# from game import
from utils import *

actions = AIGame().getLegalActions()

def trainActor(discount_rate=0.8, lr=0.1, hidden_dims=120, num_epochs=10):
    actor = Actor(430, 9, hidden_dims=hidden_dims)
    actor_optimizer = torch.optim.Adam(actor.parameters(), lr=lr)

    def run_episode():
        game = AIGame()
        state = game.toTensor()
        reward = 0

        losses = []
        logprobs = []
        rewards = []
        while not game.isDead():
            state = game.toTensor()
            action_logprob, action_index = actor.choose_action(state)
            action = actions[action_index]
            oldScore = game.heuristicScore()
            game = game.move(action)
            newScore = game.heuristicScore()
            reward = newScore - oldScore
            if game.isDead():
                reward -= 10 # death penalty
            reward -= 1 # living penalty
            rewards.append(reward)
            logprobs.append(action_logprob)
        
        values = []
        R = 0
        for reward in rewards[::-1]:
            R = reward + discount_rate * R
            values.insert(0,R)
        for logprob, value in zip(logprobs, values):
            actor.zero_grad()
            score = logprob * value
            loss = -score
            loss.backward()
            actor_optimizer.step()
            losses.append(loss)
        
        losses = torch.tensor(losses)
        mean_loss = losses.mean()
        print("score:",game.score())
        print("heuristic:",game.heuristicScore())
        print("age:", game.game.frameCount / 60)
        print("mean loss:",mean_loss)
        return mean_loss
    
    for epoch in range(num_epochs):
        print("running epoch",epoch+1)
        run_episode()

    return actor

if __name__ == "__main__":
    trainActor()            
