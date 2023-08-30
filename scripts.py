from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson, Commendation
from random import choice


def fix_marks(kid: str):
    schoolkid = fetch_kid(kid)
    kid_marks = Mark.objects.filter(schoolkid=schoolkid)
    kid_bad_marks = kid_marks.filter(points__lte=3)
    kid_bad_marks.update(points=5)


def remove_chastisements(kid: str):
    schoolkid = fetch_kid(kid)
    kid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    kid_chastisements.delete()


def create_commendation(kid: str, subject_name: str):
    schoolkid = fetch_kid(kid)
    try:
        subject = Subject.objects.get(
            title=subject_name,
            year_of_study=schoolkid.year_of_study
        )

        lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject=subject
        ).order_by("-date").first()

        text_choices = [
            "Молодцом!",
            "Хвалю!",
            "Внимательно слушает учителя",
            "Лучший ответ в классе!",
            "Так держать!",
            "Невероятный успех!",
            "Лучше всех!",
            "Пример для подражания",
            "Гордость класса!",
        ]

        Commendation.objects.create(
            text=choice(text_choices),
            created=lesson.date,
            schoolkid=schoolkid,
            subject=subject,
            teacher=lesson.teacher,
        )
    except Subject.DoesNotExist:
        print("Нет такого предмета")


def fetch_kid(kid_name: str):
    try:
        kid = Schoolkid.objects.get(full_name__contains=kid_name)
        return kid
    except Schoolkid.DoesNotExist:
        print("Такого имени не существует")
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено больше 1 совпадения")
