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
    Hỗ trợ đọc cột new_data và cung cấp dữ liệu ngẫu nhiên cho stress test.
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
        self._new_data_list: List[str] = []
        self._load_data()

    def _load_data(self):
        """Load dữ liệu từ file Excel."""
        try:
            self._df = pd.read_excel(self.excel_path)
            
            # Kiểm tra cột new_data có tồn tại không
            if 'new_data' not in self._df.columns:
                raise ValueError(
                    f"File Excel không có cột 'new_data'. "
                    f"Các cột hiện có: {list(self._df.columns)}"
                )
            
            # Lọc các dòng có dữ liệu hợp lệ
            self._new_data_list = (
                self._df['new_data']
                .dropna()
                .astype(str)
                .tolist()
            )
            
            # Lọc các chuỗi rỗng
            self._new_data_list = [
                data for data in self._new_data_list 
                if data.strip() != '' and data.strip().lower() != 'nan'
            ]
            
            if not self._new_data_list:
                raise ValueError("Không tìm thấy dữ liệu hợp lệ trong cột 'new_data'")
            
            print(f"✅ Đã load {len(self._new_data_list)} dòng dữ liệu từ {self.excel_path.name}")
            
        except Exception as e:
            raise RuntimeError(f"Lỗi khi đọc file Excel: {e}")

    def get_random_new_data(self) -> str:
        """
        Lấy một giá trị ngẫu nhiên từ cột new_data.

        Returns:
            Chuỗi nội dung từ cột new_data
        """
        if not self._new_data_list:
            raise RuntimeError("Không có dữ liệu để lấy. Vui lòng kiểm tra file Excel.")
        
        return random.choice(self._new_data_list)

    def get_all_data(self) -> List[str]:
        """
        Lấy toàn bộ dữ liệu từ cột new_data.

        Returns:
            Danh sách tất cả giá trị trong cột new_data
        """
        return self._new_data_list.copy()

    def get_data_count(self) -> int:
        """
        Lấy số lượng dòng dữ liệu có sẵn.

        Returns:
            Số lượng dòng dữ liệu
        """
        return len(self._new_data_list)


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

