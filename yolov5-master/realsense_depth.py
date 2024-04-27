import pyrealsense2 as rs
import numpy as np

class DepthCamera:
    
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()
        

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Get intrinsics
        self.intr = None
        self.profile = self.pipeline.start(config)
        align_to = rs.stream.color
        self.align = rs.align(align_to)
        if self.profile:
            video_stream = self.profile.get_stream(rs.stream.color)
            if video_stream:
                intrinsics = video_stream.as_video_stream_profile().get_intrinsics()
                self.intr = intrinsics
                print("Intrinsics:", self.intr)
        
    def get_intrinsics(self):
        return self.intr
    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image
    
    def get_depth(self, x, y):
      
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics

        # Get depth value at given pixel coordinates
        depth = depth_frame.get_distance(x, y)

        return depth

    def release(self):
        self.pipeline.stop()