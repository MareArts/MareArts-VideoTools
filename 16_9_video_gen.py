import cv2
import numpy as np
import argparse
import os

def convert_to_16_9(input_video, output_video):
    """
    Convert a video to 16:9 aspect ratio by adding black bars while preserving original resolution.
    
    Args:
        input_video (str): Path to the input video file
        output_video (str): Path to save the output video file
    """
    # Open the video file
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video}")
        return
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate current aspect ratio
    current_ratio = width / height
    target_ratio = 16 / 9
    
    # Determine new dimensions to achieve 16:9
    if current_ratio < target_ratio:
        # Video is too tall - add horizontal padding (letterboxing)
        new_width = int(height * target_ratio)
        new_height = height
        h_padding = (new_width - width) // 2
        v_padding = 0
    else:
        # Video is too wide - add vertical padding (pillarboxing)
        new_width = width
        new_height = int(width / target_ratio)
        h_padding = 0
        v_padding = (new_height - height) // 2
    
    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change codec as needed
    out = cv2.VideoWriter(output_video, fourcc, fps, (new_width, new_height))
    
    # Progress tracking
    print(f"Converting video to 16:9 aspect ratio...")
    print(f"Original dimensions: {width}x{height} (ratio: {current_ratio:.4f})")
    print(f"New dimensions: {new_width}x{new_height} (ratio: {new_width/new_height:.4f})")
    
    processed_frames = 0
    
    # Process the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Create a black canvas of the new size
        canvas = np.zeros((new_height, new_width, 3), dtype=np.uint8)
        
        # Place the original frame onto the canvas
        canvas[v_padding:v_padding+height, h_padding:h_padding+width] = frame
        
        # Write the frame
        out.write(canvas)
        
        # Update progress
        processed_frames += 1
        if processed_frames % 100 == 0:
            percentage = (processed_frames / frame_count) * 100
            print(f"Progress: {percentage:.1f}% ({processed_frames}/{frame_count} frames)")
    
    # Release resources
    cap.release()
    out.release()
    print(f"Conversion complete. Output saved to {output_video}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert video to 16:9 aspect ratio with black bars")
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("output", help="Output video file path")
    args = parser.parse_args()
    
    convert_to_16_9(args.input, args.output)