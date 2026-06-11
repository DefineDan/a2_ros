import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    camera_info_url = 'file://' + os.path.join(
        get_package_share_directory('a2_ros'),
        'config', 'camera', 'camera_info.yaml',
    )

    gscam_config = (
        "udpsrc address=230.1.1.1 port=1720 multicast-iface=eth0 "
        "! queue "
        "! application/x-rtp, media=video, encoding-name=H264 "
        "! rtph264depay ! h264parse ! avdec_h264 "
        "! videoconvert "
        "! video/x-raw,format=RGB"
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'camera_name',
            default_value='camera',
            description='Camera namespace',
        ),
        DeclareLaunchArgument(
            'image_encoding',
            default_value='rgb8',
            description='Image encoding passed to gscam2',
        ),
        DeclareLaunchArgument(
            'gscam_config',
            default_value=gscam_config,
            description='GStreamer pipeline string',
        ),
        DeclareLaunchArgument(
            'camera_frame',
            default_value='front_camera_optical_frame',
            description='TF frame stamped on image/camera_info headers '
                        '(optical frame defined in a2_description URDF)',
        ),

        Node(
            package='gscam2',
            executable='gscam_main',
            name='gscam2',
            output='screen',
            parameters=[{
                'gscam_config':    LaunchConfiguration('gscam_config'),
                'camera_name':     LaunchConfiguration('camera_name'),
                'image_encoding':  LaunchConfiguration('image_encoding'),
                'camera_info_url': camera_info_url,
                'frame_id':        LaunchConfiguration('camera_frame'),
            }],
            remappings=[
                ('image_raw', 'camera/image_raw'),
                ('camera_info', 'camera/camera_info'),
            ],
        ),

    ])