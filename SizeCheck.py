import os
from PIL import Image
import plotly.graph_objs as go

def collect_image_data(folder_path):
    total_files = 0
    completed_files = 0

    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)

    widths = []
    heights = []
    areas = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg', 'gif')):
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    width, height = img.size
                    area = width * height
                    widths.append(width)
                    heights.append(height)
                    areas.append(area)

            completed_files += 1
            percent_completed = (completed_files / total_files) * 100
            print(f'Progress: {percent_completed:.2f}%')
    return widths, heights, areas


def plot_image_dimensions(widths, heights, areas, low_area_threshold, high_area_threshold):
    low_area_images = [(w, h) for w, h, a in zip(widths, heights, areas) if a <= low_area_threshold]
    high_area_images = [(w, h) for w, h, a in zip(widths, heights, areas) if a >= high_area_threshold]
    normal_area_images = [(w, h) for w, h, a in zip(widths, heights, areas) if
                          low_area_threshold < a < high_area_threshold]

    trace_low = go.Scatter(
        x=[w for w, _ in low_area_images],
        y=[h for _, h in low_area_images],
        mode='markers',
        marker=dict(color='red'),
        name='Background Images'
    )

    trace_normal = go.Scatter(
        x=[w for w, _ in normal_area_images],
        y=[h for _, h in normal_area_images],
        mode='markers',
        marker=dict(color='blue'),
        name='In Between Images'
    )

    trace_high = go.Scatter(
        x=[w for w, _ in high_area_images],
        y=[h for _, h in high_area_images],
        mode='markers',
        marker=dict(color='green'),
        name='Foreground Images'
    )

    layout = go.Layout(
        title=dict(
            text='HR Dataset - Size Distribution',
            font=dict(size=40)  # Adjust the size as needed
        ),
        xaxis=dict(title='Width [pixels]', titlefont=dict(size=30), tickfont=dict(size=25)),
        yaxis=dict(title='Height [pixels]', titlefont=dict(size=30), tickfont=dict(size=25)),
        hovermode='closest',
        showlegend=True,
        #legend=dict(font=dict(size=35))
    )

    fig = go.Figure(data=[trace_high, trace_normal, trace_low], layout=layout)
    fig.show()

folder_path = '03_Daten_PreProcessing/00_HighRes_Images/0_combined'
low_area_threshold = int(0)
high_area_threshold = int(100000000)
widths, heights, areas = collect_image_data(folder_path)
plot_image_dimensions(widths, heights, areas, low_area_threshold, high_area_threshold)

