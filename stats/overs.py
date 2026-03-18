BALLS_PER_OVER = 6

def overs_to_balls(overs):
    whole = int(overs)
    balls = int(round((overs - whole) * 10))
    if balls < 0 or balls > 5:
        raise ValueError(f"Invalid overs notation: {overs}")
    return whole * BALLS_PER_OVER + balls


def balls_to_overs(balls):
    if balls < 0:
        raise ValueError("Balls cannot be negative")
    return float(f"{balls // BALLS_PER_OVER}.{balls % BALLS_PER_OVER}")


def remaining_overs(total_overs, overs_bowled):
    total_balls = total_overs * BALLS_PER_OVER
    bowled = overs_to_balls(overs_bowled)
    remaining = max(total_balls - bowled, 0)
    return balls_to_overs(remaining)
