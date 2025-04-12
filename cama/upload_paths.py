# your_app/upload_paths.py

def profile_image_path(instance, filename):
    return f'users/{instance.user.id}/profile/{filename}'

def course_video_path(instance, filename):
    return f'users/{instance.user.id}/videos/{filename}'