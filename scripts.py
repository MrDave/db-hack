from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson, Commendation
from random import choice


TEXT_CHOICES = [
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


def fix_marks(kid: str):
    schoolkid = fetch_kid(kid)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    bad_marks.update(points=5)


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

        Commendation.objects.create(
            text=choice(TEXT_CHOICES),
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
