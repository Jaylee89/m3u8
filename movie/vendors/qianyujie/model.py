
class Status(object):
    status: int
    description: str
    succeed: int

    def __init__(self, status, description, succeed) -> None:
        self.status = status
        self.description = description
        self.succeed = succeed

class CourseChapterObject(object):
    course_id: str
    chapter_id: str
    name: str
    children: list

    def __init__(self, course_id, chapter_id, name, children: list) -> None:
        self.course_id = course_id
        self.chapter_id = chapter_id
        self.name = name
        self.children = children

class CourseChapterList(object):
    course_chapter: list

    def __init__(self, course_chapter: list):
        self.course_chapter = course_chapter

class QianYuJieResponse(object):
    status: Status
    data: CourseChapterList

    def __init__(self, status, data):
        self.status = status
        self.data = data

# original class
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

class QianYuJie(object):
    data: list

    def __init__(self, data: list):
        self.data = data