
# class Status:
#     status: int
#     description: str
#     succeed: int

class CourseChapter:
    course_id: str
    chapter_id: str
    name: str
    children: list

    def __init__(self, course_id, chapter_id, name) -> None:
        self.course_id = course_id
        self.chapter_id = chapter_id
        self.name = name
    
    def set_children(self, children):
        self.children = children

class QianYuJie:
    data: list

    def __init__(self, data: list) -> None:
        self.data = data