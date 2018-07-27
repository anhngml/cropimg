import cv2
import os
# rtsp://192.168.10.28:554


class ImgCrop:
    def __init__(self, scale=1, stream_path='vlc-output_16.mp4', cam_indx=16):
        self.ix, self.iy, self.ex, self.ey = 100, 100, 200, 200
        self.scale = scale
        self.drawing = False
        self.croping = False
        self.stream_path = stream_path
        self.cam_indx = cam_indx

        self.vid = cv2.VideoCapture(self.stream_path)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.stream_path)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.cnt = 0

    def get_crop_area(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self.ex, self.ey = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                if self.scale <= 0:
                    self.ex, self.ey = x, y
                else:
                    self.ex = x
                    self.ey = ((x - self.ix) * self.scale) + self.iy

        elif event == cv2.EVENT_LBUTTONUP:
            if self.scale <= 0:
                self.ex, self.ey = x, y
            else:
                self.ex = x
                self.ey = ((x - self.ix) * self.scale) + self.iy
            self.drawing = False

    def get_frame(self, show=False):
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Create opencv video capture object
        # cap = cv2.VideoCapture(self.stream_path)
        while self.vid.isOpened():
            self.cnt += 1
            ret, frame = self.vid.read()
            if self.croping and self.cnt % 10 == 0:
                fileName = '{}{}_{}.jpg'.format(
                    self.save_path, self.cam_indx, self.cnt)
                img_crop = frame[self.iy:self.ey, self.ix:self.ex]

                if self.crop_resize_w > 0 and self.crop_resize_h > 0:
                    dim = (self.crop_resize_w, self.crop_resize_h)
                    resized = cv2.resize(
                        img_crop, dim, interpolation=cv2.INTER_AREA)
                else:
                    resized = img_crop

                msg = "Saving '{}'".format(fileName)
                cv2.putText(frame, msg, (10, 70), font, 0.65,
                            (255, 255, 0), 2, cv2.LINE_AA)
                cv2.imwrite(fileName, resized)
            if show:
                cv2.namedWindow('vid')
                cv2.setMouseCallback('vid', self.get_crop_area, frame)
            cv2.rectangle(frame, (self.ix, self.iy),
                          (self.ex, self.ey), (0, 255, 0), 5)
            st = 'Area: {}, {}, {}, {}'.format(
                self.ix, self.iy, self.ex, self.ey)
            size = 'Size: {}x{}'.format(self.ex - self.ix, self.ey - self.iy)
            cv2.putText(frame, st, (10, 30), font, 0.65,
                        (255, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, size, (10, 50), font, 0.65,
                        (255, 0, 255), 2, cv2.LINE_AA)
            if show:
                cv2.imshow('vid', frame)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)

            if show:
                k = cv2.waitKey(1) & 0xFF
                if k == ord('c'):
                    self.croping = True
                elif k == ord('s'):
                    self.croping = False
        else:
            return (ret, None)

    def crop_imgs(self, resize_w=0, resize_h=0):
        self.crop_resize_w = resize_w
        self.crop_resize_h = resize_h
        self.croping = True

    def stop_cropping(self):
        self.croping = False

    def set_cropping_box(self, s_id, x, y, w, h):
        self.cam_indx = s_id
        self.save_path = 'images/cam{}/'.format(self.cam_indx)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        self.ix = x
        self.iy = y
        self.ex = x + w
        self.ey = y + h

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


if __name__ == "__main__":
    imgc = ImgCrop()
    imgc.get_frame()
