class Lesson:
    def __init__(self, name, teacher, room, is_multiple_hour):
        self.name = name
        self.teacher = teacher
        self.room = room
        self.is_multiple_hour = is_multiple_hour

    def __str__(self):
        return f"{self.name} with {self.teacher} in {self.room}"
    def getName(self):
        return self.name
    def getTeacher(self):
        return self.teacher
    def getRoom(self):
        return self.room
    def getis_multiple_hour(self):
        return self.is_multiple_hour
    def __eq__(self, other):
        if isinstance(other, Lesson):
            return (
                    self.name == other.name
                    and self.teacher == other.teacher
                    and self.room == other.room
                    and self.is_multiple_hour == other.is_multiple_hour
            )
        return False

    def __hash__(self):
        return hash((self.name, self.teacher, self.room, self.is_multiple_hour))