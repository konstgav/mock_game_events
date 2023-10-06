import random
import matplotlib.pyplot as plt

num_samples = 1000
num_steps = 50
scores = num_steps*[0]
for sample in range(num_samples):
    player_scores = num_steps*[0]
    for step in range(num_steps):        
        rnd_num = random.randint(1,6)
        sum = 0
        counter = 0
        while (rnd_num != 1) and (counter < 6):
            sum += rnd_num
            rnd_num = random.randint(1,6)
            counter += 1
        if (rnd_num == 1):
            sum = 0  
        player_scores[step] += sum
        if step > 0:
            player_scores[step] += player_scores[step-1]
        scores[step] += player_scores[step]

for step in range(num_steps):        
    scores[step] = scores[step] / num_samples

plt.plot(scores)
plt.show()