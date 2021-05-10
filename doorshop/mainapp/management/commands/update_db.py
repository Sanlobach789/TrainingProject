from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            users_profile = UserProfile.objects.create(user=user)
            users_profile.save()
