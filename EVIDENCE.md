# Booking Lab Evidence Record

**Name:** Pakawun Jindawat
**Student ID:** 6681453


**Repository:** https://github.com/Pakawun/iccs471-booking-lab-Pakawun-Jid.git

## Goal
The goal is to fix the `create_booking` so that a new booking overlapping an existing one **in the same room** raises `ValueError` and doesn't get stored. Bookings use `[start, end)`, so touching boundaries (like 10:00 right after a 09:00–10:00) don't count as overlapping. Different rooms overlapping is fine. 

## Constraints / Out of Scope
I could only edit `booking_app/booking.py` and `tests/test_booking.py`. Everything else — `demo.py`, `pyproject.toml`, the config files — had to stay untouched. The existing behavior had to keep working too: blank room/guest rejection, invalid time ranges, and bookings staying in creation order. No dates, no persistence, no web stuff, no room-name normalization.


## Key Decision and Agent Claim
In Planemode, copilot's plan look right, but its verification section suggest running `pytest tests/test_booking.py`. I didn't accept that cause this project uses `uv` and the standard `unittest` module, and pytest isn't even a dependency, so I stuck with `uv run python -m unittest discover -s tests -v` instead. I also made sure the overlap-rejection test asserted the list still contained the first booking rather than being empty, since an overlap can only happen when something's already there.


## Verification: Claim → Evidence
- **Claim:** A same-room overlap (including one booking fully inside another) is rejected and not stored, while adjacency and different rooms still work.
- **Command or test I ran:**  `uv run python -m unittest discover -s tests -v`
- **Actual result:** All 8 tests passed, including my new ones for overlap rejection, unchanged storage after rejection, adjacency, different rooms, and full containment (A 550–560 inside A 540–600).
- **What this supports:** It gives me reason to believe the overlap rule works across the cases I care about and that I didn't break any of the original four baseline tests.

## Manual Validation
When I ran `uv run python demo.py` myself, it printed that the overlapping booking in room A was **rejected** with the "booking overlaps an existing booking in the same room" message, the adjacent booking in room A was accepted, the overlapping time in room B was accepted, and `Stored bookings: 3`. Before the fix it said the overlap was accepted (BUG) with 4 stored, so the demo confirmed the behavior changed the way it was supposed to — separately from the tests.


## Remaining Uncertainty
My tests don't cover weirder inputs like a zero-length or backwards interval combined with an overlap, or identical bookings created twice in the same room. The existing time-range validation should catch invalid ranges before the overlap check ever runs, but I didn't write a test that specifically proves the two rules interact correctly, so that's one corner I'm not 100% certain about.