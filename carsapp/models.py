from django.db import models

class AssessorProfile(models.Model):
    names = models.CharField(max_length=255)
    id_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.names

class AssessmentReports(models.Model):
    file = models.FileField(upload_to='uploads/excel_files/')  # This will store the file in the 'uploads/excel_files/' directory
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
    class Meta:
        db_table = 'assessmentreports'  # New table name