import random
from .validate import calculateCheckSum


def generate(seed: int = None) -> str:
    """Generate a random Thai citizen ID number.
    :param seed: Random seed.
    :type seed: int
    :return: Thai citizen ID number.
    :rtype: str
    """
    if seed is not None:
        random.seed(seed)
    citizen_id = str(random.randint(1, 8))
    for _ in range(11):
        citizen_id += str(random.randint(0, 9))
    citizen_id += str(calculateCheckSum(citizen_id))
    return citizen_id
