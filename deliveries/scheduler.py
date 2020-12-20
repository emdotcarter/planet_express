import random


class Scheduler:
    @classmethod
    def assign_crew_members(cls, delivery):
        available_crew_members = CrewMember.available_crew_members()

        selected_crew_members = available_crew_members.sample(
            delivery.contract.crew_size
        )
        delivery.assign_crew(selected_crew_members)
