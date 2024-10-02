from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from .models import AssessorProfile, AssessmentReports
from django.http import FileResponse, Http404, HttpResponse
import requests, os, json, time, cloudconvert

# Create your views here.
def home_view(request):
    #handle landing page
    return render(request, 'home.html')

def login_assessor(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            assessor = AssessorProfile.objects.get(username=username)
            if check_password(password, assessor.password):
                # Login successful, do something (e.g., redirect to dashboard)
                return redirect('dashboard')  # Replace with your desired view
            else:
                # Handle incorrect password
                return render(request, 'assessor_login.html', {'error': 'Invalid credentials'})
        except AssessorProfile.DoesNotExist:
            # Handle user not found
            return render(request, 'assessor_login.html', {'error': 'User not found'})
    return render(request, 'assessor_login.html')

def dashboard(request):
    #handle landing page
    return render(request, 'upload.html')

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        # Save the file using Django's file system
        uploaded_file = AssessmentReports.objects.create(file=excel_file)

        # Redirect to a success page after saving
        return render(request, 'upload.html', {'success': True})

    return render(request, 'upload.html')

def admin_uploaded_files(request):
    files = AssessmentReports.objects.all()
    return render(request, 'admin_uploaded_files.html', {'files': files})

def download_excel(request, file_id):
    try:
        excel_file = AssessmentReports.objects.get(id=file_id)
        file_path = excel_file.file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    except AssessmentReports.DoesNotExist:
        raise Http404("File does not exist")
    except FileNotFoundError:
        raise Http404("File not found on disk")
    
def clean_filename(filename):
    # Remove any invalid characters and keep only the basename
    filename = os.path.basename(filename)
    # Replace spaces with underscores and ensure it's valid
    filename = filename.replace(' ', '_')
    return filename

apikey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYmI5MTkxZWIzOTgzM2U0ZTg2ZjgzMzE2MGU0NmFiYzU3YTA2MmY3YjJlNzUwMDA3NjY5OGNjMDQzZTU1NWM1NDJjZTg3Mjg2OGNmNmYxNjUiLCJpYXQiOjE3Mjc1MTUxODIuMzY1MDMxLCJuYmYiOjE3Mjc1MTUxODIuMzY1MDMzLCJleHAiOjQ4ODMxODg3ODIuMzYwOTE0LCJzdWIiOiI2OTcyNjkwOCIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIiwid2ViaG9vay5yZWFkIiwid2ViaG9vay53cml0ZSIsInByZXNldC5yZWFkIiwicHJlc2V0LndyaXRlIl19.M8VZocrtb-AwfDoRkgeHMyKqLwPG1iDYnptVIQuwDmTYQEVYhfED-M4oy6tDDbKLjrl7YrXDHelxvUCOMXR1R8OpDmQ0H2bqcfO8h2tCX3PmijlZpuk_U-OJZCztHfrEMpRMBatJBPLmhQFwgzFAPGG4xm8M2wM9EIqbnXv4tU-xxNdSg2CiQNmCSFfbuq67N7-zDb6KELHnRP-FjxJWLSLjqJfpxQM44KAQoMpPKdDPQTt7FF9E5gryV0j2g0AF2j0zAZQKHzJns-k4GJ1O2lerRXeaRnQCVEhJdjxUqc6051IRe74dUNlIDgQFZSQc9LVNrdtDVujvbVHz_qffP9EEl_Ljf-mM4KLCXZaulEt6tLaWslrUG5R3lHXPOuZdQf5cja1axGAVoJ1c12vB7NWidZI6ghXUwlQ0xv4Px1lOA7GuFYSTJKnvzJ_ygPPQsKkoeD4DhOmd1-o3nQq-97HNoRSZkSXDjFRllABu2phCZBUY1XGQxU9DOxMymBf9gVGyCqTtjKDZX7bH94_8mBsL7wOPHF_il8YzLZgwNFsJNdGwLvsW9t5rj8eT6yoTOn1sqpxKKFMOhQ71f-2-p-EOwCf-Xk1jlw8BghDtH-2m3vXKqYSfbkLAOXUHT1puKtD1QdD30fIHJms_Vqg2TqRFSl6oDBxz4gLpXrDxA5M"  # Replace with your actual API key
# Configure CloudConvert API
cloudconvert.configure(api_key=apikey, sandbox=False)

# Function to convert Excel to PDF and download it
def convert_excel_to_pdf(request, file_id):
    # Get the Excel file from the database
    file = get_object_or_404(AssessmentReports, id=file_id)
    file_url = request.build_absolute_uri(file.file.url)  # Generate full URL for the file
    filename = clean_filename(file.file.name)  # Clean the filename
    

    try:
        # Step 1: Create the job with CloudConvert API
        job = cloudconvert.Job.create(payload={
            "tasks": {
                "import-my-file": {
                    "operation": "import/url",
                    "url": file_url,  # The URL of the Excel file on your server
                    "filename": filename  # Use the cleaned filename
                },
                "convert-my-file": {
                    "operation": "convert",
                    "input_format": "xlsx",
                    "output_format": "pdf",
                    "engine": "office",
                    "input": ["import-my-file"],
                },
                "export-my-file": {
                    "operation": "export/url",
                    "input": "convert-my-file"
                }
            }
        })

        # Step 2: Wait for the job to complete
        job = cloudconvert.Job.wait(id=job['id'])

        # Step 3: Check all tasks for status
        for task in job["tasks"]:
            if task.get("name") == "import-my-file" and task.get("status") != "finished":
                return HttpResponse(f"Import task failed: {task.get('message')}", status=500)
            elif task.get("name") == "convert-my-file" and task.get("status") != "finished":
                return HttpResponse(f"Conversion task failed: {task.get('message')}", status=500)
            elif task.get("name") == "export-my-file" and task.get("status") != "finished":
                return HttpResponse(f"Export task failed: {task.get('message')}", status=500)

        # Step 4: If all tasks succeeded, get the export task
        export_task = None
        for task in job["tasks"]:
            if task.get("name") == "export-my-file" and task.get("status") == "finished":
                export_task = task
                break

        if export_task is None:
            return HttpResponse("Error: Export task not completed", status=500)

        # Step 5: Get the result file and download URL
        file_info = export_task.get("result").get("files")[0]
        pdf_file_url = file_info['url']  # URL of the converted PDF

        # Step 6: Download the PDF and send it as a response
        response = cloudconvert.download(filename=file_info['filename'], url=pdf_file_url)
        return redirect(pdf_file_url)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
