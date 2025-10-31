# PATRIC
### Player Assessment via TrueSkill: Rating of Impact & Consistency
Application of the TrueSkill Through Time algorithm to Ultimate Frisbee practices.

---
#### Overview 
PATRIC estimates individual player skill from weekly practice games of Ultimate Frisbee using Microsoft's TrueSkill algorithm in its TrueSkill Through Time (TTT) variant. Unlike the Elo ranking algorithm, TrueSkill supports team-based games of any team size and takes into account uncertainty about a player's skill.

##### TrueSkill

Each player's performance is modelled as a Gaussian distribution with mean μ (skill) and standard deviation σ (uncertainty). The TrueSkill value is a conservative rating of a player's skill calculated typically as μ − 3σ, meaning a player's true skill is very likely above that value (see the [3 sigma rule](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule)).

A team performance is a sum of the player's performances (a sum of Gaussian distributions also is one). Outcomes of games move players' μ up or down, larger upsets move it more. Playing games also gradually reduces the uncertainty σ. New players start with high uncertainty and calibrate as they play games, which by itself improves their TrueSkill rating.

##### TrueSkill Through Time (TTT)
The TrueSkill Through Time variant focuses on propagating the results through time via a Baysian Network. 
TODO: why is it better.

[See the docs for more info.](https://trueskillthroughtime.readthedocs.io/en/latest/)

Applying the TTT algorithm for Ultimate Frisbee was inspired by Jake Smart, who has done this for the College team Brownian Motion.

#### Usage
- Store the game results in the csv file `games_db.csv`
- Game format: TODO, weights: TODO
- Run the `main.py` module, which will run the TTT algorithm from the stored games and will dump the player ratings into a csv  file `leaderboard.csv`
- plotting: TODO
- player curves: TODO


#### Requirements
TODO

#### Literature
- A primer: https://www.moserware.com/2010/03/computing-your-skill.html
- Jake Smart about using TrueSkill Through Time for Ultimate: https://creators.spotify.com/pod/profile/pod-practice/episodes/Jake-Smart--Brown-BMo--Boston-DiG--Boston-Glory--Ep-78-e2tv5dm, minutes 0:42 - 0:55.
- Microsoft's Article about TrueSkill: https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/
- TrueSkill original paper: https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/TR-2006-80.pdf
- TrueSkill Through Time paper: https://www.jstatsoft.org/article/view/v112i06

