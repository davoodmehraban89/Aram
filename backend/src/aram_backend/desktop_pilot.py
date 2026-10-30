"""Native Tk/ttk Windows Pilot UI: read-only XLSX validation, no posting.

The current program is NOT the final financial statements product. Unbuilt
workflows are textual blockers, never decorative clickable dead buttons.
"""
from __future__ import annotations

import sys
import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Callable

from aram_backend.desktop_pilot_core import DesktopPilotController, PilotInputError
from aram_backend.pilot_workbook import SHEET_HEADERS, preflight_pilot_workbook

APP_TITLE = "آرام | پایلوت دسکتاپ — آزمایشی و فاقد مجوز صدور صورت مالی"
PILOT_ACTIONS = {
    "file.open": "open_workbook",
    "file.validate": "validate_workbook",
    "file.clear": "clear_workbook",
    "file.exit": "exit_application",
    "help.about": "show_about",
}
MAX_VISIBLE_ISSUES = 3000


class PilotWindow(tk.Tk):
    """Real native desktop controls; all enabled actions have callbacks."""

    def __init__(
        self, *,
        file_picker: Callable[[], str] | None = None,
        info_dialog: Callable[[str, str], None] | None = None,
    ) -> None:
        super().__init__()
        self.controller = DesktopPilotController()
        self._file_picker = file_picker or (
            lambda: filedialog.askopenfilename(
                parent=self, title="انتخاب فایل اکسل پایلوت آرام",
                filetypes=[("Pilot workbook", "*.xlsx")],
            )
        )
        self._info_dialog = info_dialog or (
            lambda title, text: messagebox.showinfo(title, text, parent=self)
        )
        self.title(APP_TITLE)
        self.geometry("1080x710")
        self.minsize(820, 560)
        self.configure(bg="#edf2f7")
        self.file_name = tk.StringVar(value="فایلی انتخاب نشده است.")
        self.summary = tk.StringVar(value="ابتدا یک فایل با قالب پایلوت انتخاب کنید.")
        self.status = tk.StringVar(value="حالت ایمن: هیچ داده‌ای ثبت یا تأیید نمی‌شود.")
        self._set_style()
        self._build_menu()
        self._build_content()
        self._register_keys()
        self._refresh_controls()

    def _set_style(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Pilot.TLabel", font=("Tahoma", 11), background="#edf2f7")
        style.configure("PilotTitle.TLabel", font=("Tahoma", 20, "bold"),
                        background="#edf2f7", foreground="#152e4d")
        style.configure("PilotBanner.TLabel", font=("Tahoma", 10, "bold"),
                        background="#fff0d8", foreground="#78350f",
                        padding=12)
        style.configure("Pilot.TButton", font=("Tahoma", 11), padding=10)
        style.configure("Pilot.TNotebook.Tab", font=("Tahoma", 11), padding=(18, 12))
        style.configure("Pilot.Treeview", font=("Tahoma", 10), rowheight=28)
        style.configure("Pilot.Treeview.Heading", font=("Tahoma", 10, "bold"))

    def _build_menu(self) -> None:
        self._bar = tk.Menu(self)
        self.file_menu = tk.Menu(self._bar, tearoff=0)
        self.file_menu.add_command(
            label="انتخاب فایل اکسل", accelerator="Ctrl+O",
            command=self.open_workbook,
        )
        self.file_menu.add_command(
            label="اجرای پیش‌بررسی", accelerator="Ctrl+R",
            command=self.validate_workbook,
        )
        self.file_menu.add_command(
            label="پاک‌کردن انتخاب", accelerator="Ctrl+L",
            command=self.clear_workbook,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="خروج", accelerator="Ctrl+Q", command=self.exit_application,
        )
        self._bar.add_cascade(label="فایل", menu=self.file_menu)
        self.help_menu = tk.Menu(self._bar, tearoff=0)
        self.help_menu.add_command(
            label="درباره و محدودیت‌های پایلوت", accelerator="F1",
            command=self.show_about,
        )
        self._bar.add_cascade(label="راهنما", menu=self.help_menu)
        self.config(menu=self._bar)

    def _build_content(self) -> None:
        outer = ttk.Frame(self, padding=18)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="آرام — پایلوت کنترل اولیه فایل اکسل",
                  style="PilotTitle.TLabel", anchor="e").pack(fill="x")
        ttk.Label(
            outer,
            text=(
                "نسخه آزمایشی دسکتاپ | فقط خواندن و اعتبارسنجی اولیه | "
                "فاقد تهیه، ثبت، تأیید، چاپ یا صدور صورت‌های مالی"
            ),
            style="PilotBanner.TLabel", anchor="e", wraplength=930,
        ).pack(fill="x", pady=(14, 18))

        tabs = ttk.Notebook(outer, style="Pilot.TNotebook")
        tabs.pack(fill="both", expand=True)
        self.tabs = tabs

        preflight_tab = ttk.Frame(tabs, padding=16)
        tabs.add(preflight_tab, text="اعتبارسنجی اکسل")
        workflow_tab = ttk.Frame(tabs, padding=24)
        tabs.add(workflow_tab, text="مراحل مالی و محدودیت‌ها")
        help_tab = ttk.Frame(tabs, padding=24)
        tabs.add(help_tab, text="راهنما")

        ttk.Label(
            preflight_tab, textvariable=self.file_name,
            anchor="e", justify="right", wraplength=850,
            font=("Tahoma", 11),
        ).pack(fill="x", pady=(0, 12))
        buttons = ttk.Frame(preflight_tab)
        buttons.pack(fill="x")
        self.open_button = ttk.Button(
            buttons, text="انتخاب فایل اکسل", command=self.open_workbook,
            style="Pilot.TButton",
        )
        self.open_button.pack(side="right", padx=5)
        self.validate_button = ttk.Button(
            buttons, text="بررسی فایل", command=self.validate_workbook,
            style="Pilot.TButton",
        )
        self.validate_button.pack(side="right", padx=5)
        self.clear_button = ttk.Button(
            buttons, text="پاک‌کردن انتخاب", command=self.clear_workbook,
            style="Pilot.TButton",
        )
        self.clear_button.pack(side="right", padx=5)

        ttk.Label(
            preflight_tab, textvariable=self.summary, anchor="e",
            font=("Tahoma", 11),
        ).pack(fill="x", pady=(16, 12))

        issue_area = ttk.Frame(preflight_tab)
        issue_area.pack(fill="both", expand=True)
        columns = ("severity", "code", "sheet", "row", "field", "message")
        self.issue_tree = ttk.Treeview(
            issue_area, columns=columns, show="headings", style="Pilot.Treeview",
            selectmode="browse",
        )
        header_labels = {
            "severity": "اهمیت", "code": "کد خطا", "sheet": "شیت",
            "row": "ردیف", "field": "ستون", "message": "توضیح کنترل",
        }
        sizes = {
            "severity": 75, "code": 170, "sheet": 100,
            "row": 70, "field": 145, "message": 400,
        }
        for column in columns:
            self.issue_tree.heading(column, text=header_labels[column])
            self.issue_tree.column(
                column, width=sizes[column],
                minwidth=65, anchor="e", stretch=(column == "message"),
            )
        scroll_y = ttk.Scrollbar(
            issue_area, orient="vertical", command=self.issue_tree.yview,
        )
        scroll_x = ttk.Scrollbar(
            issue_area, orient="horizontal", command=self.issue_tree.xview,
        )
        self.issue_tree.configure(
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,
        )
        self.issue_tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        issue_area.grid_rowconfigure(0, weight=1)
        issue_area.grid_columnconfigure(0, weight=1)

        blocked_features = (
            "• انتخاب شرکت و سال مالی از دیتابیس — هنوز به برنامه دسکتاپ متصل نیست.",
            "• ورود و ذخیره اسناد حسابداری — غیرفعال؛ فقط بررسی ساختار فایل ممکن است.",
            "• نگاشت حساب به یادداشت و زیر‌یادداشت — هنوز گردش تأیید نهایی ندارد.",
            "• تهیه صورت وضعیت مالی، سود و زیان، جریان وجه نقد و حقوق مالکانه — غیرفعال.",
            "• کنترل تطبیق و ردیابی اقلام تا حساب و سند منبع — برای پایلوت نهایی لازم است.",
            "• بازبینی مستقل، امضای تصمیم، صدور PDF/Excel و چاپ — غیرفعال.",
        )
        ttk.Label(
            workflow_tab, text="این بخش‌ها هنوز عملیاتی نیستند؛ دکمهٔ نمایشی ندارند.",
            anchor="e", justify="right",
            font=("Tahoma", 12, "bold"),
        ).pack(fill="x", pady=(0, 14))
        for item in blocked_features:
            ttk.Label(
                workflow_tab, text=item, anchor="e", justify="right",
                wraplength=880, font=("Tahoma", 11),
            ).pack(fill="x", pady=9)

        ttk.Label(
            help_tab,
            text=(
                "۱. از منوی «فایل» یا دکمهٔ «انتخاب فایل اکسل» یک فایل *.xlsx "
                "منطبق با قالب پایلوت باز کنید.\n\n"
                "۲. «بررسی فایل» را اجرا کنید؛ خطاها با شیت، ردیف و ستون نمایش داده می‌شوند.\n\n"
                "۳. «پاک‌کردن انتخاب» فقط وضعیت همین پنجره را پاک می‌کند.\n\n"
                "این پایلوت آفلاین کار می‌کند، هیچ فایل ورودی را تغییر نمی‌دهد و "
                "داده‌ها را در دیتابیس یا شبکه ثبت نمی‌کند. "
                "موفقیت پیش‌بررسی صرفاً بررسی قالب و قواعد پایه است، نه "
                "تأیید صحت ارقام یا تأیید تهیه صورت‌های مالی."
            ),
            anchor="e", justify="right", wraplength=880,
            font=("Tahoma", 12),
        ).pack(fill="x")

        ttk.Label(
            outer, textvariable=self.status, anchor="e",
            style="Pilot.TLabel",
        ).pack(fill="x", pady=(12, 0))

    def _register_keys(self) -> None:
        bindings = {
            "<Control-o>": self.open_workbook,
            "<Control-r>": self.validate_workbook,
            "<Control-l>": self.clear_workbook,
            "<Control-q>": self.exit_application,
            "<F1>": self.show_about,
        }
        for sequence, callback in bindings.items():
            self.bind_all(sequence, lambda event, fn=callback: fn())

    def _refresh_controls(self) -> None:
        enabled = self.controller.selected_path is not None
        self.validate_button.configure(state="normal" if enabled else "disabled")
        self.file_menu.entryconfigure(1, state="normal" if enabled else "disabled")

    def open_workbook(self) -> None:
        selected = self._file_picker()
        if not selected:  # Cancel must not clear the current selection.
            return
        try:
            self.controller.choose_file(selected)
        except PilotInputError as exc:
            self.file_name.set("فایلی انتخاب نشده است.")
            self.summary.set("انتخاب فایل معتبر انجام نشد.")
            self.status.set(str(exc))
        else:
            self.file_name.set(str(self.controller.selected_path))
            self.summary.set("فایل انتخاب شد؛ بررسی هنوز اجرا نشده است.")
            self.status.set("انتخاب فایل به معنی ورود یا ذخیرهٔ اطلاعات نیست.")
        self._clear_issues()
        self._refresh_controls()

    def validate_workbook(self) -> None:
        if self.controller.selected_path is None:
            self.status.set("ابتدا فایل اکسل را انتخاب کنید.")
            return
        self._clear_issues()
        try:
            checked = self.controller.validate()
        except PilotInputError as exc:
            self.summary.set("بررسی فایل انجام نشد.")
            self.status.set(str(exc))
        else:
            issues = checked.issues
            for issue in issues[:MAX_VISIBLE_ISSUES]:
                self.issue_tree.insert(
                    "", "end",
                    values=(
                        issue.severity, issue.code, issue.sheet,
                        issue.row, issue.field, issue.message,
                    ),
                )
            if checked.valid:
                self.summary.set(
                    "پیش‌بررسی قالب با موفقیت گذشت؛ صحت مالی و تأیید حسابرسی اثبات نشده است."
                )
            else:
                self.summary.set(
                    f"فایل رد شد: {len(issues)} مورد اخطار/خطای قابل گزارش."
                )
            if len(issues) > MAX_VISIBLE_ISSUES:
                self.status.set(
                    f"فقط {MAX_VISIBLE_ISSUES} مورد نخست نمایش داده شد؛ "
                    "همهٔ خطاها در نتیجهٔ بررسی داخل حافظه موجودند."
                )
            else:
                self.status.set(
                    "پیش‌بررسی تکمیل شد؛ هیچ منبع مالی تغییر داده نشد."
                )
        self._refresh_controls()

    def _clear_issues(self) -> None:
        items = self.issue_tree.get_children()
        if items:
            self.issue_tree.delete(*items)

    def clear_workbook(self) -> None:
        self.controller.clear()
        self._clear_issues()
        self.file_name.set("فایلی انتخاب نشده است.")
        self.summary.set("ابتدا یک فایل با قالب پایلوت انتخاب کنید.")
        self.status.set("انتخاب پاک شد؛ هیچ فایل ورودی حذف نشد.")
        self._refresh_controls()

    def exit_application(self) -> None:
        self.destroy()

    def show_about(self) -> None:
        self._info_dialog(
            "درباره آرام",
            "ARAM Native Desktop Pilot — UNRELEASED\n"
            "فقط پیش‌بررسی فایل اکسل؛ فاقد تهیه و تأیید صورت‌های مالی.\n"
            "بدون شبکه، بدون ثبت دیتابیس، بدون دسترسی به داده‌های اصلی.",
        )


def self_test() -> int:
    """Headless import/validation smoke for a frozen Windows executable."""
    from aram_backend.desktop_pilot_core import DesktopPilotController
    if DesktopPilotController().state != "EMPTY":
        return 3
    result = preflight_pilot_workbook(b"not an xlsx")
    if result.valid or not result.issues:
        return 4
    if len(PILOT_ACTIONS) != 5:
        return 5
    return 0


def ui_smoke_test() -> int:
    """Invoke actual native widgets/menus on a synthetic workbook (Windows CI).

    Programmatic Tk widget/OS-menu invocation, NOT a human pointer click or
    full end-to-end financial statements acceptance.
    """
    from io import BytesIO
    from openpyxl import Workbook

    book = Workbook()
    book.remove(book.active)
    for name, headers in SHEET_HEADERS.items():
        book.create_sheet(name).append(list(headers))
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic_pilot.xlsx"
        book.save(path)
        info_calls: list[str] = []
        window = PilotWindow(
            file_picker=lambda: str(path),
            info_dialog=lambda title, text: info_calls.append(title),
        )
        try:
            window.withdraw()
            window.update_idletasks()
            for tab_index in range(window.tabs.index("end")):
                window.tabs.select(tab_index)
                if window.tabs.index(window.tabs.select()) != tab_index:
                    return 17
            for key in ("<Control-o>", "<Control-r>", "<Control-l>", "<Control-q>", "<F1>"):
                if not window.bind_all(key):
                    return 18
            if str(window.validate_button.cget("state")) != "disabled":
                return 10
            window.file_menu.invoke(0)  # open (real Tk menu callback)
            if window.controller.selected_path != path:
                return 11
            if str(window.validate_button.cget("state")) != "normal":
                return 12
            window.validate_button.invoke()  # validate (real Tk button)
            if window.controller.result is None:
                return 13
            window.file_menu.invoke(1)  # repeat validation (real Tk menu)
            window.help_menu.invoke(0)  # about (injected safe dialog)
            if len(info_calls) != 1:
                return 14
            window.clear_button.invoke()  # clear button
            if window.controller.selected_path is not None:
                return 15
            window.open_button.invoke()  # open button, not just menu
            if window.controller.selected_path != path:
                return 19
            window.file_menu.invoke(2)  # clear via menu
            if window.controller.selected_path is not None:
                return 16
            window.file_menu.invoke(4)  # exit via menu
            return 0
        finally:
            try:
                if window.winfo_exists():
                    window.destroy()
            except tk.TclError:
                pass


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--self-test"]:
        return self_test()
    if args == ["--ui-smoke"]:
        return ui_smoke_test()
    if args:
        print("Supported: --self-test, --ui-smoke, or no arguments", file=sys.stderr)
        return 2
    window = PilotWindow()
    window.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
