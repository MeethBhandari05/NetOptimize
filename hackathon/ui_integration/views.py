from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.

def index(request):
    return render(request, 'input_form.html')  # Render the template


def process_tlbo_form(request):
    
    if request.method == "POST":
        input_values = [
            request.POST.get("grid_size"),
            request.POST.get("sensor_radius"),
            request.POST.get("num_sensors"),
            request.POST.get("num_targets"),
            request.POST.get("initial_power"),
            request.POST.get("qj_coverage"),
            request.POST.get("energy_rate"),
        ]

        target_file = request.FILES.get("target_file")
        target_data = []

        if target_file:
            # Save file to media directory
            file_path = f"{settings.MEDIA_ROOT}/{target_file.name}"
            with open(file_path, "wb+") as destination:
                for chunk in target_file.chunks():
                    destination.write(chunk)

            # Read the saved CSV file
            df = pd.read_csv(file_path)
            target_data = df.values.tolist()
            input_values.append(target_data)
        

        print("Received Form Inputs:")
        labels = [
            "Grid Size", "Sensor Radius", "Number of Sensors", "Number of Targets",
            "Initial Power", "Qj Coverage", "Energy Consumption Rate"
        ]
        
        for label, value in zip(labels, input_values[:7]):
            print(f"{label}: {value}")

        # Print CSV file data
        if target_data:
            print("\nTarget File Data:")
            for row in target_data:
                print(row)

        return HttpResponse("Form submitted successfully. Check server logs for input values.")

    return render(request, "input_form.html") 
