import cv2
import os

def png2vedio(image_path, vedio_path, fps = 24):
    img_list = sorted(os.listdir(image_path)) # 获取图片列表
    img = cv2.imread(os.path.join(image_path, img_list[0]))
    video_writer = cv2.VideoWriter(vedio_path, 
                                   cv2.VideoWriter_fourcc(*'avc1'), 
                                   fps, (img.shape[1], img.shape[0])) # 创建视频写入对象
    for img_name in img_list: # 遍历图片列表
        img = cv2.imread(os.path.join(image_path, img_name)) # 读取图片文件
        video_writer.write(img) # 写入视频

    video_writer.release() # 释放资源

def run():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="图片目录")
    parser.add_argument("vedio_path", help="目标视频文件名")
    parser.add_argument("-f", "--fps", type=int, default=24, help="视频的帧率")
    args = parser.parse_args()
    # 调用函数
    png2vedio(args.image_path,args.vedio_path,args.fps)


    