from django.core.management.base import BaseCommand
from authentication.models import CustomUser, StudentProfile

class Command(BaseCommand):
    help = "Create missing student profiles for users with user_type='student'"

    def handle(self, *args, **kwargs):
        students_without_profiles = CustomUser.objects.filter(user_type="student").exclude(
            student_profile__isnull=False
        )

        for user in students_without_profiles:
            StudentProfile.objects.create(
                user=user,
                full_name=user.username,  # Adjust if needed
                roll_number="N/A",  # Placeholder; update manually
                class_name="Unknown",
                section="N/A",
                date_of_birth="2000-01-01",  # Placeholder
                phone_number="0000000000",  # Placeholder
                address="Not provided",
            )
            self.stdout.write(self.style.SUCCESS(f"Created profile for {user.email}"))

        if not students_without_profiles.exists():
            self.stdout.write(self.style.SUCCESS("No missing profiles found."))
