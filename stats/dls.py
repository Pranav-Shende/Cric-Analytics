from math import floor
from .overs import remaining_overs  # Added the dot (.) here
from .resources import get_resource # Added the dot (.) here

MINUTES_PER_OVER = 4.0

def overs_lost_from_delay(delay_minutes):
    return int(delay_minutes // MINUTES_PER_OVER)


def scheduled_overs(fmt):
    return 50 if fmt == "odi" else 20

# 1️⃣ PRE–FIRST INNINGS DLS

def dls_pre_first_innings(fmt, delay_minutes):
    fmt = fmt.lower()
    original = scheduled_overs(fmt)

    overs_lost = overs_lost_from_delay(delay_minutes)
    new_overs = max(original - overs_lost, 0)

    return {
        "new_overs": new_overs
    }


# 2️⃣ MID–FIRST INNINGS DLS

def dls_mid_first_innings(fmt, overs_bowled, wickets_lost, delay_minutes):
    fmt = fmt.lower()
    original = scheduled_overs(fmt)

    overs_lost = overs_lost_from_delay(delay_minutes)
    revised_total = max(original - overs_lost, 0)

    overs_remaining = remaining_overs(revised_total, overs_bowled)

    resources_remaining = get_resource(
        int(overs_remaining),
        wickets_lost,
        fmt
    )

    return {
        "revised_total_overs": revised_total,
        "overs_remaining": overs_remaining,
        "resources_remaining": resources_remaining
    }


# 3️⃣ PRE–SECOND INNINGS DLS

def dls_pre_second_innings(fmt, team1_score, delay_minutes):
    fmt = fmt.lower()
    original = scheduled_overs(fmt)

    overs_lost = overs_lost_from_delay(delay_minutes)
    new_overs = max(original - overs_lost, 0)

    R1 = get_resource(original, 0, fmt)
    R2 = get_resource(new_overs, 0, fmt)

    target = floor(team1_score * (R2 / R1)) + 1
    rrr = round(target / new_overs, 2) if new_overs > 0 else float("inf")

    return {
        "new_total_overs": new_overs,
        "revised_target": target,
        "runs_needed": target,
        "required_run_rate": rrr
    }


# 4️⃣ MID–SECOND INNINGS DLS 

def dls_mid_second_innings(fmt, team1_score, team2_score,
                           overs_bowled, wickets_lost, delay_minutes):

    fmt = fmt.lower()
    original = scheduled_overs(fmt)

    if overs_bowled == 0:
        return dls_pre_second_innings(fmt, team1_score, delay_minutes)

    overs_lost = overs_lost_from_delay(delay_minutes)
    revised_total = max(original - overs_lost, 0)

    overs_remaining_before = remaining_overs(original, overs_bowled)
    overs_remaining_after = remaining_overs(revised_total, overs_bowled)

    R1 = get_resource(original, 0, fmt)
    R_start = get_resource(original, 0, fmt)

    R_now = get_resource(
        int(overs_remaining_before),
        wickets_lost,
        fmt
    )

    R_after = get_resource(
        int(overs_remaining_after),
        wickets_lost,
        fmt
    )

    par_score = team1_score * ((R_start - R_now) / R1)

    revised_target = floor(
        team1_score * ((R_start - R_after) / R1)
    ) + 1

    runs_needed = revised_target - team2_score
    rrr = (
        round(runs_needed / overs_remaining_after, 2)
        if overs_remaining_after > 0 else float("inf")
    )

    return {
        "new_total_overs": revised_total,
        "overs_remaining": overs_remaining_after,
        "par_score": round(par_score, 1),
        "revised_target": revised_target,
        "runs_needed": runs_needed,
        "required_run_rate": rrr
    }
