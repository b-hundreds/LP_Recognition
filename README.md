## License Plate Recognition
Đây là một project xây dựng một web nhận dạng biển số, gồm 2 chức năng:<br>

* Nhận dạng biển số xe (Dùng yolov8 cho cả 2 task là detection và recognition, sử dụng thư viện albumentation để quay ảnh ngẫu nhiên trong khoảng -45 độ đến 45 độ), lưu kết quả vào database
* Tìm kiếm ảnh biển số xe trong database theo chuỗi chữ số của biển

## Install environments
```
pip install -r requirements.txt
```
Ngoài ra, mongodb cũng cần được cài trên máy (Đã được bật, đường kết nối là "mongodb://localhost:27017")

## Start web project
```
python -m flask run
```
Sau khi chạy, bật link http://127.0.0.1:5000 để tương tác với web
Chú ý: biển 2 dòng sẽ được định dạng là "A-B" (A là dòng trên, B là dòng dưới), còn biển 1 dòng sẽ được định dạng thành 1 chuỗi liên tục "ABCDS..."

## Results

   <p align="left" >
   <img src="results1.jpg" >
    Chức năng nhận diện biển số
</p>

   <p align="right" >
   <img src="results3.jpg" >
    Chức năng tìm kiếm biển số
</p>