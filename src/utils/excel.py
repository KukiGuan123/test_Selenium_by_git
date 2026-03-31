import openpyxl
from pathlib import Path
from typing import List, Dict, Union


class ExcelUtil:
    """Excel 工具类：读取指定 sheet 的全部数据（行为字典）"""

    @staticmethod
    def get_sheet(excel_path: str, sheet_name: str) -> List[Dict[str, str | int | float | None]]:
        """
        获取整个 sheet 的所有数据（第一行作为 key，每一行作为字典）
        :param excel_path: Excel 文件路径
        :param sheet_name: Sheet 名称
        :return: [ {col1: val1, col2: val2}, {...} ]
        """
        if not Path(excel_path).exists():
            raise FileNotFoundError(f"Excel文件不存在: {excel_path}")

        # 加载工作簿
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        if sheet_name not in wb.sheetnames:
            raise ValueError(f"Sheet【{sheet_name}】不存在！可用sheet: {wb.sheetnames}")

        ws = wb[sheet_name]
        all_rows = list(ws.rows)
        if not all_rows:
            return []

        # 第一行作为表头 KEY
        headers = [str(cell.value).strip() if cell.value is not None else "" for cell in all_rows[0]]

        # 读取数据行
        result = []
        for row in all_rows[1:]:
            row_dict = {}
            for idx, cell in enumerate(row):
                row_dict[headers[idx]] = cell.value
            result.append(row_dict)

        wb.close()
        return result

    # ======================
    # ✅ 修复后的 get_row（核心）
    # ======================
    @staticmethod
    def get_row(
        data_or_path: Union[str, List[Dict]],
        sheet_name_or_filter: str = None,
        filter_value: str = None
    ) -> Dict:
        """
        两用方法：
        1. 传入 excel_path + sheet_name + filter
        2. 传入 data_list + filter
        """
        # 情况 1：传入路径 (path, sheet, filter)
        if isinstance(data_or_path, str) and sheet_name_or_filter and filter_value:
            all_data = ExcelUtil.get_sheet(data_or_path, sheet_name_or_filter)
            for row in all_data:
                if str(row.get("Filter", "")).strip() == str(filter_value).strip():
                    return row
            return {}

        # 情况 2：传入已经读取的数据 (data_list, filter)
        elif isinstance(data_or_path, list) and sheet_name_or_filter:
            all_data = data_or_path
            for row in all_data:
                if str(row.get("Filter", "")).strip() == str(sheet_name_or_filter).strip():
                    return row
            return {}

        else:
            raise ValueError("参数错误！用法：\n1. get_row(path, sheet, filter) \n2. get_row(data_list, filter)")

    # ======================
    # ✅ 修复后的 get_cell（核心）
    # ======================
    @staticmethod
    def get_cell(
        row_or_path: Union[str, Dict],
        col_or_sheet: str = None,
        filter_val: str = None,
        column_name: str = None
    ):
        """
        两用方法：
        1. 传入 path, sheet, filter, column → 直接取值
        2. 传入 row, column → 直接取值
        """
        # 情况 1：传入 path, sheet, filter, column (4个参数)
        if column_name is not None:
            # 这里的调用：get_row(path, sheet, filter)
            row = ExcelUtil.get_row(row_or_path, col_or_sheet, filter_val)
            return row.get(column_name, None)

        # 情况 2：传入 row, column (2个参数)
        elif isinstance(row_or_path, dict):
            row = row_or_path
            col = col_or_sheet
            return row.get(col, None)

        else:
            raise ValueError("参数错误！用法：\n1. get_cell(path, sheet, filter, column) \n2. get_cell(row, column)")