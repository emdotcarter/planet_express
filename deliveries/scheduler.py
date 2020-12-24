import random

from crew.crew_member import CrewMember


class Scheduler:
    @classmethod
    def assign_crew_members(cls, delivery, cursor):
        available_crew_members = CrewMember.all(cursor)

        selected_crew_members = random.sample(
            available_crew_members, delivery.contract(cursor).crew_size
        )
        delivery.assign_crew(selected_crew_members, cursor)
