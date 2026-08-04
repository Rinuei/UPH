from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk


class UPHCalculatorApp:

  def __init__(self, root):
    self.root = root
    self.root.title("進階 UPH 計算、達標與時間預估工具")
    self.root.geometry("450x600")
    self.root.resizable(False, False)

    # 標題
    title_label = tk.Label(
        root, text="生產效率 (UPH) 計算器", font=("Arial", 16, "bold")
    )
    title_label.pack(pady=10)

    # 模式選擇
    mode_frame = tk.Frame(root)
    mode_frame.pack(pady=5)

    tk.Label(mode_frame, text="選擇計算模式：", font=("Arial", 11)).pack(
        side=tk.LEFT, padx=5
    )
    self.mode_var = tk.StringVar(value="單次作業時間模式")
    self.mode_combo = ttk.Combobox(
        mode_frame,
        textvariable=self.mode_var,
        values=[
            "單次作業時間模式",
            "日期區間產能模式",
            "產能達標與評估模式",
            "生產時間預估模式",
        ],
        state="readonly",
        width=18,
        font=("Arial", 10),
    )
    self.mode_combo.pack(side=tk.LEFT, padx=5)
    self.mode_combo.bind("<<ComboboxSelected>>", self.switch_mode)

    # 內容切換的容器 Frame
    self.container = tk.Frame(root)
    self.container.pack(pady=10, fill="both", expand=True)

    # 初始化四種模式的介面
    self.create_mode1_widgets()
    self.create_mode2_widgets()
    self.create_mode3_widgets()
    self.create_mode4_widgets()

    # 結果顯示標籤
    self.result_label = tk.Label(
        root,
        text="請輸入資料進行計算...",
        font=("Arial", 11),
        fg="#333",
        justify=tk.LEFT,
    )
    self.result_label.pack(pady=5)

    # 計算按鈕
    calc_button = tk.Button(
        root,
        text="開始計算",
        font=("Arial", 11, "bold"),
        bg="#4CAF50",
        fg="white",
        width=15,
        command=self.calculate,
    )
    calc_button.pack(pady=10)

    # 預設顯示模式 1
    self.show_mode(1)

  def create_mode1_widgets(self):
    """模式 1：單次作業時間"""
    self.frame1 = tk.Frame(self.container)

    tk.Label(self.frame1, text="總生產數量 (pcs):", font=("Arial", 11)).grid(
        row=0, column=0, sticky="w", pady=8
    )
    self.qty1_entry = tk.Entry(self.frame1, font=("Arial", 11), width=15)
    self.qty1_entry.grid(row=0, column=1, padx=10, pady=8)

    tk.Label(self.frame1, text="作業時間:", font=("Arial", 11)).grid(
        row=1, column=0, sticky="w", pady=8
    )
    self.time1_entry = tk.Entry(self.frame1, font=("Arial", 11), width=15)
    self.time1_entry.grid(row=1, column=1, padx=10, pady=8)

    self.time_unit_var = tk.StringVar(value="minutes")
    unit_frame = tk.Frame(self.frame1)
    unit_frame.grid(row=2, column=0, columnspan=2, pady=5)

    tk.Radiobutton(
        unit_frame,
        text="分鐘 (Minutes)",
        variable=self.time_unit_var,
        value="minutes",
        font=("Arial", 10),
    ).pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(
        unit_frame,
        text="小時 (Hours)",
        variable=self.time_unit_var,
        value="hours",
        font=("Arial", 10),
    ).pack(side=tk.LEFT, padx=10)

  def create_mode2_widgets(self):
    """模式 2：日期區間產能"""
    self.frame2 = tk.Frame(self.container)

    tk.Label(self.frame2, text="總生產數量 (pcs):", font=("Arial", 11)).grid(
        row=0, column=0, sticky="w", pady=6
    )
    self.qty2_entry = tk.Entry(self.frame2, font=("Arial", 11), width=15)
    self.qty2_entry.grid(row=0, column=1, padx=10, pady=6)

    tk.Label(
        self.frame2, text="開始日期 (YYYY-MM-DD):", font=("Arial", 11)
    ).grid(row=1, column=0, sticky="w", pady=6)
    self.start_date_entry = tk.Entry(self.frame2, font=("Arial", 11), width=15)
    self.start_date_entry.grid(row=1, column=1, padx=10, pady=6)
    self.start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    tk.Label(
        self.frame2, text="結束日期 (YYYY-MM-DD):", font=("Arial", 11)
    ).grid(row=2, column=0, sticky="w", pady=6)
    self.end_date_entry = tk.Entry(self.frame2, font=("Arial", 11), width=15)
    self.end_date_entry.grid(row=2, column=1, padx=10, pady=6)
    self.end_date_entry.insert(
        0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    )

    tk.Label(
        self.frame2, text="每日工作時數 (小時):", font=("Arial", 11)
    ).grid(row=3, column=0, sticky="w", pady=6)
    self.daily_hours_entry = tk.Entry(self.frame2, font=("Arial", 11), width=15)
    self.daily_hours_entry.grid(row=3, column=1, padx=10, pady=6)
    self.daily_hours_entry.insert(0, "8")

    self.include_weekend_var2 = tk.BooleanVar(value=False)
    tk.Checkbutton(
        self.frame2,
        text="包含週末（六、日也計算工作天）",
        variable=self.include_weekend_var2,
        font=("Arial", 10),
    ).grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

  def create_mode3_widgets(self):
    """模式 3：產能達標與評估模式"""
    self.frame3 = tk.Frame(self.container)

    tk.Label(self.frame3, text="目標生產數量 (pcs):", font=("Arial", 11)).grid(
        row=0, column=0, sticky="w", pady=5
    )
    self.qty3_entry = tk.Entry(self.frame3, font=("Arial", 11), width=15)
    self.qty3_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(
        self.frame3, text="開始日期 (YYYY-MM-DD):", font=("Arial", 11)
    ).grid(row=1, column=0, sticky="w", pady=5)
    self.start_date3_entry = tk.Entry(self.frame3, font=("Arial", 11), width=15)
    self.start_date3_entry.grid(row=1, column=1, padx=10, pady=5)
    self.start_date3_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    tk.Label(
        self.frame3, text="截止日期 (YYYY-MM-DD):", font=("Arial", 11)
    ).grid(row=2, column=0, sticky="w", pady=5)
    self.end_date3_entry = tk.Entry(self.frame3, font=("Arial", 11), width=15)
    self.end_date3_entry.grid(row=2, column=1, padx=10, pady=5)
    self.end_date3_entry.insert(
        0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    )

    tk.Label(
        self.frame3, text="每日工作時數 (小時):", font=("Arial", 11)
    ).grid(row=3, column=0, sticky="w", pady=5)
    self.daily_hours3_entry = tk.Entry(self.frame3, font=("Arial", 11), width=15)
    self.daily_hours3_entry.grid(row=3, column=1, padx=10, pady=5)
    self.daily_hours3_entry.insert(0, "8")

    tk.Label(self.frame3, text="目前實際 UPH:", font=("Arial", 11)).grid(
        row=4, column=0, sticky="w", pady=5
    )
    self.current_uph_entry = tk.Entry(self.frame3, font=("Arial", 11), width=15)
    self.current_uph_entry.grid(row=4, column=1, padx=10, pady=5)

    self.include_weekend_var3 = tk.BooleanVar(value=False)
    tk.Checkbutton(
        self.frame3,
        text="包含週末（六、日也計算工作天）",
        variable=self.include_weekend_var3,
        font=("Arial", 10),
    ).grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

  def create_mode4_widgets(self):
    """模式 4：生產時間預估模式"""
    self.frame4 = tk.Frame(self.container)

    tk.Label(self.frame4, text="目標生產數量 (pcs):", font=("Arial", 11)).grid(
        row=0, column=0, sticky="w", pady=6
    )
    self.qty4_entry = tk.Entry(self.frame4, font=("Arial", 11), width=15)
    self.qty4_entry.grid(row=0, column=1, padx=10, pady=6)

    tk.Label(self.frame4, text="目前實際 UPH:", font=("Arial", 11)).grid(
        row=1, column=0, sticky="w", pady=6
    )
    self.uph4_entry = tk.Entry(self.frame4, font=("Arial", 11), width=15)
    self.uph4_entry.grid(row=1, column=1, padx=10, pady=6)

    tk.Label(
        self.frame4, text="開始生產日期 (YYYY-MM-DD):", font=("Arial", 11)
    ).grid(row=2, column=0, sticky="w", pady=6)
    self.start_date4_entry = tk.Entry(self.frame4, font=("Arial", 11), width=15)
    self.start_date4_entry.grid(row=2, column=1, padx=10, pady=6)
    self.start_date4_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    tk.Label(
        self.frame4, text="每日工作時數 (小時):", font=("Arial", 11)
    ).grid(row=3, column=0, sticky="w", pady=6)
    self.daily_hours4_entry = tk.Entry(self.frame4, font=("Arial", 11), width=15)
    self.daily_hours4_entry.grid(row=3, column=1, padx=10, pady=6)
    self.daily_hours4_entry.insert(0, "8")

    self.include_weekend_var4 = tk.BooleanVar(value=False)
    tk.Checkbutton(
        self.frame4,
        text="包含週末（六、日也計算工作天）",
        variable=self.include_weekend_var4,
        font=("Arial", 10),
    ).grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

  def switch_mode(self, event=None):
    mode = self.mode_var.get()
    if mode == "單次作業時間模式":
      self.show_mode(1)
    elif mode == "日期區間產能模式":
      self.show_mode(2)
    elif mode == "產能達標與評估模式":
      self.show_mode(3)
    else:
      self.show_mode(4)

  def show_mode(self, mode_num):
    self.frame1.pack_forget()
    self.frame2.pack_forget()
    self.frame3.pack_forget()
    self.frame4.pack_forget()

    if mode_num == 1:
      self.frame1.pack(fill="both", expand=True)
    elif mode_num == 2:
      self.frame2.pack(fill="both", expand=True)
    elif mode_num == 3:
      self.frame3.pack(fill="both", expand=True)
    else:
      self.frame4.pack(fill="both", expand=True)

    if hasattr(self, "result_label"):
      self.result_label.config(text="請輸入資料進行計算...")

  def calculate(self):
    try:
      current_mode = self.mode_var.get()

      if current_mode == "單次作業時間模式":
        qty_text = self.qty1_entry.get().strip()
        time_text = self.time1_entry.get().strip()

        if not qty_text or not time_text:
          messagebox.showerror("錯誤", "請填寫所有欄位！")
          return

        quantity = float(qty_text)
        time_val = float(time_text)

        if quantity < 0 or time_val <= 0:
          messagebox.showerror("錯誤", "數量與時間必須大於 0！")
          return

        unit = self.time_unit_var.get()
        hours = time_val / 60.0 if unit == "minutes" else time_val
        uph = quantity / hours
        ct_seconds = 3600 / uph if uph > 0 else 0

        result_text = (
            f"🚀 UPH (平均每小時產出): {uph:.2f} pcs/hr\n"
            f"⏱️ 平均週期時間 (CT): {ct_seconds:.2f} 秒/pc"
        )
        self.result_label.config(text=result_text, fg="#006600")

      elif current_mode == "日期區間產能模式":
        qty_text = self.qty2_entry.get().strip()
        start_str = self.start_date_entry.get().strip()
        end_str = self.end_date_entry.get().strip()
        daily_hours_text = self.daily_hours_entry.get().strip()

        if not qty_text or not start_str or not end_str or not daily_hours_text:
          messagebox.showerror("錯誤", "請填寫所有日期與產量欄位！")
          return

        quantity = float(qty_text)
        daily_hours = float(daily_hours_text)

        if quantity < 0 or daily_hours <= 0:
          messagebox.showerror("錯誤", "數量與每日時數必須大於 0！")
          return

        try:
          start_date = datetime.strptime(start_str, "%Y-%m-%d")
          end_date = datetime.strptime(end_str, "%Y-%m-%d")
        except ValueError:
          messagebox.showerror(
              "格式錯誤", "日期格式錯誤，請使用 YYYY-MM-DD（例如 2026-06-01）"
          )
          return

        if start_date > end_date:
          messagebox.showerror("錯誤", "開始日期不能大於結束日期！")
          return

        work_days = 0
        current = start_date
        while current <= end_date:
          if self.include_weekend_var2.get() or current.weekday() < 5:
            work_days += 1
          current += timedelta(days=1)

        if work_days == 0:
          messagebox.showerror("錯誤", "所選區間內沒有有效的工作天！")
          return

        total_hours = work_days * daily_hours
        uph = quantity / total_hours
        ct_seconds = 3600 / uph if uph > 0 else 0

        result_text = (
            f"🚀 UPH (平均每小時產出): {uph:.2f} pcs/hr\n"
            f"⏱️ 平均週期時間 (CT): {ct_seconds:.2f} 秒/pc\n"
            f"📅 總工作天數: {work_days} 天 (總工時: {total_hours} 小時)"
        )
        self.result_label.config(text=result_text, fg="#006600")

      elif current_mode == "產能達標與評估模式":
        qty_text = self.qty3_entry.get().strip()
        start_str = self.start_date3_entry.get().strip()
        end_str = self.end_date3_entry.get().strip()
        daily_hours_text = self.daily_hours3_entry.get().strip()
        current_uph_text = self.current_uph_entry.get().strip()

        if (
            not qty_text
            or not start_str
            or not end_str
            or not daily_hours_text
            or not current_uph_text
        ):
          messagebox.showerror("錯誤", "請填寫所有評估欄位！")
          return

        target_qty = float(qty_text)
        daily_hours = float(daily_hours_text)
        current_uph = float(current_uph_text)

        if target_qty < 0 or daily_hours <= 0 or current_uph <= 0:
          messagebox.showerror("錯誤", "數量、時數與 UPH 數值必須大於 0！")
          return

        try:
          start_date = datetime.strptime(start_str, "%Y-%m-%d")
          end_date = datetime.strptime(end_str, "%Y-%m-%d")
        except ValueError:
          messagebox.showerror(
              "格式錯誤", "日期格式錯誤，請使用 YYYY-MM-DD（例如 2026-06-01）"
          )
          return

        if start_date > end_date:
          messagebox.showerror("錯誤", "開始日期不能大於結束日期！")
          return

        work_days = 0
        current = start_date
        while current <= end_date:
          if self.include_weekend_var3.get() or current.weekday() < 5:
            work_days += 1
          current += timedelta(days=1)

        if work_days == 0:
          messagebox.showerror("錯誤", "所選區間內沒有有效的工作天！")
          return

        total_hours = work_days * daily_hours
        expected_total_qty = current_uph * total_hours
        required_uph = target_qty / total_hours

        if expected_total_qty >= target_qty:
          result_text = (
              f"✅ 評估結果：【可以如期達標】\n"
              f"📅 總工作天數: {work_days} 天 (總工時: {total_hours} 小時)\n"
              f"🎯 預計產出總量: {expected_total_qty:.0f} pcs (目標: {target_qty:.0f})\n"
              f"💡 表現良好！維持現有 UPH 即可輕鬆完成。"
          )
          self.result_label.config(text=result_text, fg="#006600")
        else:
          shortage = target_qty - expected_total_qty
          result_text = (
              f"❌ 評估結果：【無法如期達標】\n"
              f"📅 總工作天數: {work_days} 天 (總工時: {total_hours} 小時)\n"
              f"⚠️ 產量落差: 還差 {shortage:.0f} pcs\n"
              f"🔥 必須將 UPH 提升至: {required_uph:.2f} pcs/hr\n"
              f"   (需比目前 UPH 增加約 {(required_uph - current_uph):.2f} pcs/hr)"
          )
          self.result_label.config(text=result_text, fg="#CC0000")

      else:  # 模式 4：生產時間預估模式
        qty_text = self.qty4_entry.get().strip()
        uph_text = self.uph4_entry.get().strip()
        start_str = self.start_date4_entry.get().strip()
        daily_hours_text = self.daily_hours4_entry.get().strip()

        if not qty_text or not uph_text or not start_str or not daily_hours_text:
          messagebox.showerror("錯誤", "請填寫所有預估欄位！")
          return

        target_qty = float(qty_text)
        uph = float(uph_text)
        daily_hours = float(daily_hours_text)

        if target_qty <= 0 or uph <= 0 or daily_hours <= 0:
          messagebox.showerror("錯誤", "數量、UPH 與每日時數必須大於 0！")
          return

        try:
          start_date = datetime.strptime(start_str, "%Y-%m-%d")
        except ValueError:
          messagebox.showerror(
              "格式錯誤", "開始日期格式錯誤，請使用 YYYY-MM-DD"
          )
          return

        # 計算需要的總小時數
        total_hours_needed = target_qty / uph

        # 計算需要多少完整的工作天與剩餘小時
        full_work_days = total_hours_needed / daily_hours

        # 透過日曆遞增來精準推算完成日期（排除週末）
        current = start_date
        hours_accumulated = 0
        days_counted = 0

        # 如果第一天剛好是週末且不包含週末，直接往後推直到第一個工作天
        while not self.include_weekend_var4.get() and current.weekday() >= 5:
          current += timedelta(days=1)

        while hours_accumulated < total_hours_needed:
          # 判斷今天是否為工作天
          if self.include_weekend_var4.get() or current.weekday() < 5:
            days_counted += 1
            hours_accumulated += daily_hours

          if hours_accumulated < total_hours_needed:
            current += timedelta(days=1)

        completion_date = current.strftime("%Y-%m-%d")

        result_text = (
            f"⏱️ 預估生產時間結果：\n"
            f"📊 總需工時: {total_hours_needed:.1f} 小時\n"
            f"📅 預估工作天數: {full_work_days:.1f} 天 (約 {days_counted} 個工作日)\n"
            f"🏁 預計完成日期: {completion_date}"
        )
        self.result_label.config(text=result_text, fg="#006600")

    except ValueError:
      messagebox.showerror("格式錯誤", "請輸入有效的數字！")


if __name__ == "__main__":
  root = tk.Tk()
  app = UPHCalculatorApp(root)
  root.mainloop()