# DSAN 6650 PROJECT - "Search and Rescue" Game

### Introduction to the project:

<p>For my final reinforcement learning class project I created a game called “Search and Rescue”, based around the concept of a bloodhound dog scent-tracking and trailing a lost baby in a forest. In the game, the goal is for the dog, our agent, to track and reach the lost baby located on the other side of the forest. However, in the unknown forest environment, the dog must determine which directions lead to winding, navigable pathways and which directions are blocked by dense areas of trees that cannot be crossed or dead ends on the forest trails. The game ends when the dog reaches the baby.</p>

<p>Overall, my goals for this project were to take a spin on and add complexity to the concept of an agent trying to navigate through and escape a 2-D maze environment. To do this, I added a number of unique features, including: random generation of maps for each episode set in which the walls and pathways would all be mixed around, both 10x10 and 25x25-dimension map configurations, a “fog-of-war” view that would hide the true walls and pathways of the map until the dog uncovered them through movement, the use of both stock image and open game asset pixel art to give the environment a 16-bit video game feel, and the implementation of both shallow, tabular Q-Learning and deep Q-Learning models to determine which was better suited to maximizing the programmed rewards and winning the game as quickly as possible.</p> 

Remaining project information is included in the Final Project Write Up submitted on Canvas. 
