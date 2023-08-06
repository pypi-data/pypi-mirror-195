import cv2
import os


def vedio2png(vedio_path, image_path, fps=10):
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    cap = cv2.VideoCapture(vedio_path) # 读取视频文件
    count = 0 # 计数器
    name_counter = 1
    while cap.isOpened(): # 判断视频是否打开
        ret, frame = cap.read() # 读取一帧
        if ret: # 如果成功读取
            if count % fps == 0: # 每隔fps帧保存图片
                cv2.imwrite("{}/{}.png".format(image_path, str(name_counter).zfill(3)), frame) # 保存为png图片
                name_counter += 1
            count += 1 # 计数器加一
        else: # 如果失败读取，说明到达视频末尾，退出循环
            break 
    cap.release() # 释放资源

def run():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("vedio_path", help="视频路径")
    parser.add_argument("image_path", help="输出图片的路径")
    parser.add_argument("-f", "--fps", type=int, default=5, help="每多少帧输出一次")
    args = parser.parse_args()
    # 调用函数
    vedio2png(args.vedio_path, args.image_path, args.fps)
