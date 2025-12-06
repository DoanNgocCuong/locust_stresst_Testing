"""
Script để tạo cột new_data từ hai cột:
- BOT_RESPONSE_CONVERSATION_with_USER
- BOT_RESPONSE_CONVERSATION_next

Logic:
1. Previous Question: Lượt nói cuối cùng của assistant trong BOT_RESPONSE_CONVERSATION_with_USER
2. Previous Answer: Lượt nói cuối cùng của user trong BOT_RESPONSE_CONVERSATION_with_USER
3. Response to check: Toàn bộ nội dung của BOT_RESPONSE_CONVERSATION_next

Usage:
    python generate_new_data.py --sample 5    # Chạy 5 dòng đầu
    python generate_new_data.py --all         # Chạy toàn bộ file
"""

import json
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime


def generate_checklost_data(row: pd.Series) -> str:
    """
    Tạo nội dung cho cột new_data từ một dòng dữ liệu.
    
    Args:
        row: Một dòng dữ liệu từ DataFrame (pandas Series)
        
    Returns:
        Chuỗi văn bản đã được định dạng với 3 phần:
        - Previous Question
        - Previous Answer
        - Response to check
    """
    # Bước 1: Đọc và kiểm tra dữ liệu từ cột BOT_RESPONSE_CONVERSATION_with_USER
    conversation_str = row.get('BOT_RESPONSE_CONVERSATION_with_USER', '')
    
    # Kiểm tra dữ liệu rỗng
    if pd.isna(conversation_str) or conversation_str == '':
        return ''
    
    # Bước 2: Parse JSON từ chuỗi
    try:
        conversation_list = json.loads(conversation_str)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Lỗi parse JSON: {e}")
        return ''
    
    # Kiểm tra conversation_list có phải là list không
    if not isinstance(conversation_list, list):
        return ''
    
    # Bước 3: Tìm Previous Question (lượt nói cuối cùng của assistant)
    last_assistant_message = ''
    for message in reversed(conversation_list):
        if isinstance(message, dict) and message.get('role') == 'assistant':
            last_assistant_message = message.get('content', '')
            break
    
    # Bước 4: Tìm Previous Answer (lượt nói cuối cùng của user)
    last_user_message = ''
    for message in reversed(conversation_list):
        if isinstance(message, dict) and message.get('role') == 'user':
            last_user_message = message.get('content', '')
            break
    
    # Bước 5: Lấy Response to check từ cột BOT_RESPONSE_CONVERSATION_next
    response_to_check = row.get('BOT_RESPONSE_CONVERSATION_next', '')
    if pd.isna(response_to_check):
        response_to_check = ''
    
    # Bước 6: Tổng hợp và định dạng kết quả
    result = (
        f"Previous Question: {last_assistant_message}\n"
        f"Previous Answer: {last_user_message}\n"
        f"Response to check: {response_to_check}"
    )
    
    return result


def process_dataframe(df: pd.DataFrame, num_rows: int = None, show_details: bool = True) -> pd.DataFrame:
    """
    Xử lý DataFrame và tạo cột new_data.
    
    Args:
        df: DataFrame cần xử lý
        num_rows: Số dòng cần xử lý (None = tất cả)
        show_details: Có hiển thị chi tiết từng dòng không
        
    Returns:
        DataFrame đã được xử lý
    """
    # Lấy số dòng cần xử lý
    if num_rows is not None:
        df_processed = df.head(num_rows).copy()
        print(f"\n{'='*80}")
        print(f"XỬ LÝ {num_rows} DÒNG ĐẦU TIÊN")
        print(f"{'='*80}\n")
    else:
        df_processed = df.copy()
        print(f"\n{'='*80}")
        print(f"XỬ LÝ TOÀN BỘ FILE ({len(df_processed)} dòng)")
        print(f"{'='*80}\n")
    
    # Áp dụng hàm generate_checklost_data cho từng dòng
    print("Đang xử lý dữ liệu...")
    df_processed['new_data'] = df_processed.apply(generate_checklost_data, axis=1)
    
    # Hiển thị kết quả chi tiết (chỉ khi xử lý ít dòng)
    if show_details and (num_rows is None or num_rows <= 10):
        for idx, row in df_processed.iterrows():
            print(f"\n{'='*80}")
            print(f"DÒNG {idx + 1}")
            print(f"{'='*80}")
            
            # Hiển thị dữ liệu gốc (rút gọn)
            print(f"\nBOT_RESPONSE_CONVERSATION_with_USER (rút gọn):")
            conv_str = str(row.get('BOT_RESPONSE_CONVERSATION_with_USER', ''))[:200]
            print(f"{conv_str}...")
            
            print(f"\nBOT_RESPONSE_CONVERSATION_next (rút gọn):")
            next_str = str(row.get('BOT_RESPONSE_CONVERSATION_next', ''))[:200]
            print(f"{next_str}...")
            
            print(f"\nKẾT QUẢ new_data:")
            print(f"{row['new_data']}")
            print(f"\n{'-'*80}")
    else:
        print(f"✅ Đã xử lý xong {len(df_processed)} dòng")
    
    return df_processed


def main():
    """
    Hàm chính để đọc file Excel và xử lý dữ liệu.
    """
    # Parse tham số dòng lệnh
    parser = argparse.ArgumentParser(
        description='Tạo cột new_data từ file Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python generate_new_data.py --sample 5     # Chạy 5 dòng đầu
  python generate_new_data.py --all          # Chạy toàn bộ file
  python generate_new_data.py                # Mặc định: 5 dòng đầu
        """
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--sample',
        type=int,
        metavar='N',
        help='Số dòng đầu tiên cần xử lý (ví dụ: --sample 5)'
    )
    group.add_argument(
        '--all',
        action='store_true',
        help='Xử lý toàn bộ file'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        default=None,
        help='Đường dẫn file Excel đầu vào (mặc định: data_for_stressTest.xlsx)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Đường dẫn file Excel đầu ra (mặc định: tự động tạo tên)'
    )
    
    args = parser.parse_args()
    
    # Xác định đường dẫn file
    script_dir = Path(__file__).parent
    if args.input:
        excel_path = Path(args.input)
    else:
        excel_path = script_dir / "data_for_stressTest.xlsx"
    
    # Xác định số dòng cần xử lý
    if args.all:
        num_rows = None
    elif args.sample:
        num_rows = args.sample
    else:
        num_rows = 5  # Mặc định
    
    # Xác định đường dẫn file output
    if args.output:
        output_path = Path(args.output)
    else:
        if num_rows:
            output_path = script_dir / f"result_sample_{num_rows}_rows.xlsx"
        else:
            output_path = script_dir / "result_all_rows.xlsx"
    
    print(f"Đang đọc file: {excel_path}")
    
    try:
        # Đọc file Excel
        df = pd.read_excel(excel_path)
        
        print(f"\nTổng số dòng trong file: {len(df)}")
        print(f"Các cột trong file: {list(df.columns)}")
        
        # Xử lý dữ liệu
        show_details = num_rows is None or num_rows <= 10
        df_processed = process_dataframe(df, num_rows, show_details)
        
        # Lưu kết quả
        print(f"\nĐang lưu kết quả...")
        try:
            df_processed.to_excel(output_path, index=False)
            print(f"✅ Đã lưu kết quả vào: {output_path}")
            print(f"   - Tổng số dòng đã xử lý: {len(df_processed)}")
        except PermissionError:
            # Nếu file đang được mở, tạo file mới với timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path_new = output_path.parent / f"{output_path.stem}_{timestamp}{output_path.suffix}"
            df_processed.to_excel(output_path_new, index=False)
            print(f"⚠️  File gốc đang được mở, đã lưu vào: {output_path_new}")
            print(f"   - Tổng số dòng đã xử lý: {len(df_processed)}")
        
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {excel_path}")
    except Exception as e:
        print(f"❌ Lỗi khi xử lý: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

