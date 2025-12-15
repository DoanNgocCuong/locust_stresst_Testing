"""
Module đọc dữ liệu từ file Excel cho stress test.
Tuân thủ nguyên tắc Single Responsibility:
- Chỉ chịu trách nhiệm đọc và quản lý dữ liệu từ Excel.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List
import random
import threading


class ExcelDataLoader:
    """
    Class để load và quản lý dữ liệu từ file Excel.
    Ưu tiên cột 'user_input'; fallback 'new_data' để giữ tương thích cũ.
    """

    def __init__(self, excel_path: str):
        """
        Khởi tạo ExcelDataLoader.

        Args:
            excel_path: Đường dẫn đến file Excel chứa dữ liệu
        """
        self.excel_path = Path(excel_path)
        if not self.excel_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {excel_path}")
        
        self._df: Optional[pd.DataFrame] = None
        self._data_list: List[str] = []
        self._data_column: str = ""
        self._load_data()

    def _load_data(self):
        """Load dữ liệu từ file Excel."""
        try:
            self._df = pd.read_excel(self.excel_path)

            # Xác định cột dùng để lấy nội dung
            if "user_input" in self._df.columns:
                self._data_column = "user_input"
            elif "new_data" in self._df.columns:
                self._data_column = "new_data"
            else:
                raise ValueError(
                    "File Excel thiếu cột 'user_input' (ưu tiên) hoặc 'new_data' (fallback). "
                    f"Các cột hiện có: {list(self._df.columns)}"
                )

            # Lọc các dòng có dữ liệu hợp lệ
            self._data_list = (
                self._df[self._data_column]
                .dropna()
                .astype(str)
                .tolist()
            )
            
            # Lọc các chuỗi rỗng
            self._data_list = [
                data for data in self._data_list 
                if data.strip() != '' and data.strip().lower() != 'nan'
            ]
            
            if not self._data_list:
                raise ValueError(
                    f"Không tìm thấy dữ liệu hợp lệ trong cột '{self._data_column}'"
                )
            
            print(
                f"✅ Đã load {len(self._data_list)} dòng dữ liệu từ cột "
                f"'{self._data_column}' trong {self.excel_path.name}"
            )
            
        except Exception as e:
            raise RuntimeError(f"Lỗi khi đọc file Excel: {e}")

    def _estimate_tokens(self, text: str) -> int:
        """
        Ước tính số tokens từ text.
        Quy tắc đơn giản: ~4 ký tự = 1 token (cho tiếng Việt và tiếng Anh).
        
        Args:
            text: Chuỗi text cần ước tính
            
        Returns:
            Số tokens ước tính
        """
        # Ước tính: 4 ký tự = 1 token (conservative estimate)
        # Với system prompt ~400 tokens, còn lại ~200 tokens cho user content
        # Giới hạn an toàn: ~800 ký tự cho user content
        return len(text) // 4
    
    def get_random_new_data(self, max_tokens: int = 200) -> str:
        """
        Lấy một giá trị ngẫu nhiên từ cột new_data.
        Nếu dữ liệu quá dài, sẽ tự động truncate (cắt ngắn) thay vì bỏ đi.

        Args:
            max_tokens: Số tokens tối đa cho phép (mặc định 200, để lại ~400 cho system prompt)

        Returns:
            Chuỗi nội dung từ cột new_data (có thể đã được truncate nếu quá dài)
        """
        if not self._data_list:
            raise RuntimeError("Không có dữ liệu để lấy. Vui lòng kiểm tra file Excel.")
        
        # Lấy dữ liệu ngẫu nhiên (KHÔNG bỏ đi dữ liệu nào)
        data = random.choice(self._data_list)
        
        # Nếu dữ liệu quá dài, truncate (cắt ngắn) thay vì bỏ đi
        max_chars = max_tokens * 4  # ~4 ký tự = 1 token
        if len(data) > max_chars:
            # Truncate và thêm dấu hiệu để biết đã bị cắt
            truncated = data[:max_chars]
            # Cố gắng cắt ở vị trí hợp lý (không cắt giữa từ)
            # Tìm vị trí xuống dòng hoặc khoảng trắng gần nhất
            last_newline = truncated.rfind('\n')
            last_space = truncated.rfind(' ')
            cut_pos = max(last_newline, last_space)
            
            if cut_pos > max_chars * 0.8:  # Nếu tìm được vị trí hợp lý (trong 80% cuối)
                return truncated[:cut_pos]
            else:
                return truncated
        
        return data

    def get_all_data(self) -> List[str]:
        """
        Lấy toàn bộ dữ liệu từ cột new_data.

        Returns:
            Danh sách tất cả giá trị trong cột new_data
        """
        return self._data_list.copy()

    def get_data_count(self) -> int:
        """
        Lấy số lượng dòng dữ liệu có sẵn.

        Returns:
            Số lượng dòng dữ liệu
        """
        return len(self._data_list)


# Shared loader instance - được load 1 lần duy nhất và chia sẻ cho tất cả users
_shared_loader: Optional[ExcelDataLoader] = None
_loader_lock = threading.Lock()


def get_shared_loader(excel_path: Optional[str] = None) -> Optional[ExcelDataLoader]:
    """
    Lấy shared ExcelDataLoader instance.
    Load 1 lần duy nhất và chia sẻ cho tất cả users.
    
    Args:
        excel_path: Đường dẫn file Excel (chỉ cần truyền lần đầu)
        
    Returns:
        ExcelDataLoader instance hoặc None nếu không load được
    """
    global _shared_loader
    
    # Nếu đã có loader, trả về luôn
    if _shared_loader is not None:
        return _shared_loader
    
    # Nếu chưa có và không có excel_path, trả về None
    if excel_path is None:
        return None
    
    # Thread-safe: chỉ load 1 lần
    with _loader_lock:
        # Double-check: có thể đã được load bởi thread khác
        if _shared_loader is not None:
            return _shared_loader
        
        try:
            _shared_loader = ExcelDataLoader(excel_path)
            return _shared_loader
        except Exception as e:
            print(f"⚠️  Không thể load Excel: {e}")
            return None

