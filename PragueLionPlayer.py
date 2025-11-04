from trueskillthroughtime import *

class PragueLionPlayer:
    """A class for representing one individual player (do not interchange this with the Player class from the TrueSkillThroughTime library).

    Attributes:

    name: the player's name used in the scoring records.
    mu: the player's TrueSkill mean rating.
    sigma: the player's TrueSkill deviation. Sigma and mu are represented by the Gaussian object.
    number_of_practices: number of practices attended by the given player (different dates played on).
    number_of_games: total number of games the player participated in across all practices
    learning_curve: the player's learning curve as computed by TrueSkill Through Time. Is a list of tuples (game_index, Gaussian object).
    k: uncertainty factor used in TrueSkill calculations (default is 3).

    """
    
    name: str
    mu: float
    sigma: float
    number_of_practices: int = 0
    number_of_games: int = 0
    learning_curve: list[tuple[int, Gaussian]] = []
    k: float = 3.0
    def __init__(self, name: str, learning_curve: list[tuple[int, Gaussian]], mu: float = 25, sigma: float = (28/3), number_of_practices: int = 0, number_of_games: int = 0) -> None:
        """Initialize the PragueLionPlayer with a name, mu, sigma, and number of practices attended.
        Use default TrueSkill starting values for mu and sigma.
        Compute True Skill as mu - k * sigma.
        """
        self.name = name
        self.mu = mu
        self.sigma = sigma
        self.learning_curve = learning_curve
        self.number_of_practices = number_of_practices
        self.number_of_games = number_of_games
        self.true_skill = mu - self.k * sigma


    def __str__(self) -> str:
        """
        Return a string dump of all fields as a string.     
        """
        return f"{self.name},{self.number_of_practices},{self.number_of_games},{self.true_skill:.3f},{self.mu:.3f},{self.sigma:.3f}"       

    def plot_learning_curve(self):
        """Plot the learning curve of the player using matplotlib."""
        # TODO: implement plotting
        pass
    
