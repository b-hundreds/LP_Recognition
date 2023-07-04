## License Plate Recognition
Đây là một project xây dựng một web nhận dạng biển số xe, gồm 2 chức năng:<br>

* Nhận dạng biển số xe (Đầu vào là một bức ảnh), lưu kết quả vào database
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
