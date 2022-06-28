import numpy as np


def neighbor_segmentation():
    width, height = (256, 256)
    img = np.zeros((width, height, 3), np.uint8)
    # [segment1, segment2, ...]
    segments = calc_segments(img)

    # 初期化
    # {(x, y) => 1, (x, y) => 0, (x, y) => segment_idx}
    # {(x, y) => set(0, 1), (x, y) => set(1), (x, y) => set(segment_idxes)}
    pixel_segment_map = dict()
    for i in range(width):
        for j in range(height):
            pixel_segment_map[(i, j)] = -1

    # 各ピクセルにセグメントindexを割り当てる
    for i, segment in enumerate(segments):
        for (x, y) in segment:
            pixel_segment_map[(x, y)] = i

    # 一個だけセグメント計算のサンプル
    ans = set()
    segment = segments[0]
    # 右から時計回りに一周してる
    # 右が1, 左が-1, 上が-1, 下が1
    nx = [1, 1, 0, -1, -1, -1, 0, 1]
    ny = [0, 1, 1, 1, 0, -1, -1, -1]
    for (x, y) in segment:
        # (x, y) = (3, 3)
        for i in range(8):
            dx = x + nx[i]
            dy = y + ny[i]
            # (dx, dy) = [(4, 3), (4, 4), ...]
            if 0 <= dx < width and 0 <= dy < height:
                segment_idx = pixel_segment_map[(dx, dy)]
                ans.add(segment_idx)

    ans.remove(0)
    return ans