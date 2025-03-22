from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from .tlbo_algorithm import run_tlbo
# Create your views here.

def index(request):
    return render(request, 'input_form.html')  # Render the template


def process_tlbo_form(request):
    
    if request.method == "POST":
        input_values = {
            "grid_size": int(request.POST.get("grid_size")),
            "sensor_radius": int(request.POST.get("sensor_radius")),
            "num_sensors": int(request.POST.get("num_sensors")),
            "num_targets": int(request.POST.get("num_targets")),
            "initial_power": int(request.POST.get("initial_power")),
            "qj_coverage": int(request.POST.get("qj_coverage")),
            "energy_rate": int(request.POST.get("energy_rate")),
        }

        target_file = request.FILES.get("target_file")
        target_data = []

        if target_file:
            df = pd.read_csv(target_file)
            target_data = df.values.tolist()
            input_values["target_coordinates"] = target_data


        run_tlbo(input_values)
        
        return redirect("results")
        
    return render(request, "input_form.html")

def results(request):
    # Paths to generated images
    random_image = "./static/images/random_sensor_plot.png"
    optimal_image = "./static/images/optimal_sensor_plot.png"
    without_idle_image = "./static/images/removed_idle_sensor_plot.png"

    return render(request, "results.html", {
        "random_image": random_image,
        "optimal_image": optimal_image,
        "without_idle_image": without_idle_image
    })
