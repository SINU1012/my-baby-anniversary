import os
import numpy as np
from PIL import Image
from moviepy.video.VideoClip import VideoClip

def create_slideshow():
    """
    1) test_images 폴더에 여러 장의 JPG가 있고,
    2) 각 이미지를 높이 1080에 맞추어 리사이즈,
    3) 1920×1080 검은 배경에 중앙 배치,
    4) 한 장당 1초씩 순서대로 보여주는 슬라이드쇼 영상을 만들기
    5) output: test_output.mp4 (libx264, fps=24)
    """

    # A. test_images 폴더의 JPG 목록
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'test_images')
    img_files = [
        f for f in sorted(os.listdir(img_dir))
        if f.lower().endswith('.jpg')
    ]

    # B. 모든 이미지를 (1920×1080) np.array 형태로 전처리
    frame_arrays = []
    for fname in img_files:
        path = os.path.join(img_dir, fname)
        
        # 1) Pillow로 이미지 열기
        im = Image.open(path).convert("RGB")
        orig_w, orig_h = im.size

        # 2) 높이를 1080으로 리사이즈 (가로는 비율대로)
        new_h = 1080
        new_w = int(orig_w * (new_h / orig_h))

        # 혹시 가로가 0이 되면 안 되므로 최소한 1은 유지
        if new_w < 1:
            new_w = 1

        im = im.resize((new_w, new_h), Image.LANCZOS)

        # 3) x264 인코딩 문제 방지(가로가 홀수면 -1)
        if (im.size[0] % 2) != 0:
            im = im.resize((im.size[0]-1, im.size[1]))

        # 4) 최종 1920×1080 흑백 배경
        final_bg = Image.new("RGB", (1920, 1080), (0, 0, 0))  
        # 중앙 배치할 좌표 계산
        paste_x = (1920 - im.size[0]) // 2
        paste_y = (1080 - im.size[1]) // 2

        final_bg.paste(im, (paste_x, paste_y))

        # 5) numpy array 변환 (shape: (1080, 1920, 3))
        frame = np.array(final_bg, dtype=np.uint8)
        frame_arrays.append(frame)

    # C. 슬라이드쇼 총 길이는 "이미지 수" 초
    duration = len(frame_arrays)

    # D. make_frame(t) : t초에 보여줄 프레임 반환
    def make_frame(t):
        idx = int(t)  # 한 장당 1초
        if idx >= len(frame_arrays):
            idx = len(frame_arrays) - 1
        return frame_arrays[idx]

    # E. MoviePy VideoClip 생성
    #    - duration=슬라이드쇼 길이(초)
    slideshow_clip = VideoClip(make_frame, duration=duration)

    # F. 출력 파일 경로
    output_path = os.path.join(os.path.dirname(__file__), '..', 'test_output.mp4')
    if os.path.exists(output_path):
        os.remove(output_path)

    # G. 영상으로 내보내기
    slideshow_clip.write_videofile(output_path, fps=24, codec='libx264')

if __name__ == '__main__':
    create_slideshow()
