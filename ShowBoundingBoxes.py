import cv2
import pandas as pd


# Function to draw bounding boxes on each frame
def draw_bounding_boxes(video_path, csv_path, output_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create a VideoWriter object to write the output video
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Get the bounding boxes for the current frame
        frame_data = df[df['frame'] == frame_number]

        for _, row in frame_data.iterrows():
            x, y, w, h = int(row['x_top_left']), int(row['y_top_left']), int(row['width']), int(row['height'])
            color = (0, 255, 0) if row['type'] == 'A' else (255, 0, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"ID: {row['ID']}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Write the frame with the bounding boxes to the output video
        out.write(frame)

        frame_number += 1

    # Release the video objects
    cap.release()
    out.release()
    print("Output video is saved as:", output_path)


gamename = 'rum-09_right'
# File paths
video_path = f'02_Daten_original/{gamename}.mp4'
csv_path = f'02_Daten_original/{gamename}.csv'
output_path = f'02_Daten_original/BoundingBoxes/{gamename}_boundingbox.mp4'

# Run the function
draw_bounding_boxes(video_path, csv_path, output_path)
