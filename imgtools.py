import os
import numpy as np
from PIL import Image
import cv2

def load_image (img_path):
    """
        Đọc ảnh từ đường dẫn cho trước và trả về đối tượng ảnh
        Args: image_path
        Returns: đối tượng hình ảnh
    """
    try:
        img = Image.open(img_path)
        return img
    except Exception as e:
        print("Lỗi không in được ra ảnh từ: ",img_path," ", e)
        return None

def is_image_file(folder_path):
    """
        Kiểm tra có phải là ảnh không
        Args: folder_path
        Returns: true nếu là ảnh
                 false nếu không phải ảnh
    """
    extension = (".jpg", ".png", ".jpeg", "gif", "bmp")
    return folder_path.lower().endswith(extension)

def get_image_list(folder_path):
    """
        Hiển thị ảnh từ đường dẫn
        Args: folder_path
        Returns: hiển thị danh sách hình ảnh từ đường dẫn
    """
    image_list = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        for filename in files:
            file_path = os.path.join(folder_path,filename)
            if is_image_file(file_path) and os.path.isfile(file_path):
                img = load_image(file_path)
                image_list.append(img)
    return image_list

def histogram_equalization(img, nbr_bins=256):
    """
        Returns: Chuyển ảnh xám về cân bằng
    """
    # Đảm bảo là ảnh xám
    if img.mode != "L":
        img = img.convert("L")

    # Chuyển đổi ảnh và array
    img_array = np.array(img)

    # Tính toán histogram của ảnh
    histogram, bins = np.histogram(img_array, bins=nbr_bins, range=(0,256),density=True)

    # Tính toán hàm phân phối tích luỹ CDF
    cdf = histogram.cumsum()
    cdf = 255 * cdf / cdf[-1]

    # lấy giá trị mới cho từng pixel dựa trên CDF
    img_equal = np.interp(img_array,bins[:-1],cdf)

    # Chuyển đổi mảng kết quả thành hình ảnh
    equal_img = Image.fromarray(img_equal.astype("uint8"))

    return equal_img

def average_imgae(img_list):
    total_array = 0
    count = 0
    
    for img_path in img_list:
        try:
            img_array = np.array(Image.open(img_path),"f")
            total_array += img_array
            count += 1
        except:
            print("Skip ", img_path)
    # Tính trung bình:
    average_array = total_array/count

    # Chuyển đổi kết quả trung bình về hình ảnh:
    average_img = Image.fromarray(average_array.astype("uint8"))

    return average_img

def display4CV(title,img):
    """
        Hiển thị ảnh khi dùng openCV
        Args: title là tiêu đề của ảnh
        Returns: Hiện thị ảnh và đóng ảnh dễ dàng
    """
    cv2.imshow(title,img)
    # Chờ:
    cv2.waitKey(0)
    # Đóng ảnh:
    cv2.destroyWindow(title)
    