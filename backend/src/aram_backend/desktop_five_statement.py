"""Native, offline Windows pilot for five nonofficial ARAM statement candidates.

No official statements, accounting approvals, database writes, or report exports.
Tk is a presentation layer over the existing bounded local preview pipeline.
"""
from __future__ import annotations

from queue import Empty, Queue
import json
import sys
import tempfile
from threading import Thread
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from typing import Callable

from aram_backend.desktop_five_statement_core import (
    DesktopFiveInputError, DesktopFiveStatementController,
)
from aram_backend.desktop_five_statement_figures import build_preview_figures
from aram_backend.desktop_five_statement_details import PreviewDetail, build_preview_details
from aram_backend.coverage_preview import CoverageError
from aram_backend.synthetic_five_statement_demo import (
    pipeline_manifest, source_workbook,
)

TITLE = "آرام | پنج صورت مالی — پیش‌نمایش آزمایشی و غیررسمی"
ACTIONS = {
    "file.workbook": "select_workbook",
    "file.manifest": "select_manifest",
    "file.run": "run_review",
    "file.clear": "clear_selection",
    "file.exit": "exit_application",
    "help.about": "show_about",
}
MAX_VISIBLE_FINDINGS = 2000
TAB_NAMES = ("بررسی پنج صورت مالی", "خلاصه مبالغ", "ریز اقلام", "محدودیت‌ها", "راهنما")
CANDIDATE_NAMES = (
    ("balance_sheet", "ترازنامه"),
    ("income_statement", "سود و زیان"),
    ("equity_changes", "تغییرات حقوق مالکانه"),
    ("cash_flow", "جریان وجوه نقد"),
    ("trial_balance", "تراز آزمایشی"),
)


class FiveStatementWindow(tk.Tk):
    """Only implemented native controls are enabled and clickable."""

    def __init__(
        self, *,
        picker: Callable[[str], str] | None = None,
        info: Callable[[str, str], None] | None = None,
    ) -> None:
        super().__init__()
        self.controller = DesktopFiveStatementController()
        self._picker = picker or self._pick_file
        self._info = info or (
            lambda heading, msg: messagebox.showinfo(heading, msg, parent=self)
        )
        self._events: Queue[tuple[int, object, str | None]] = Queue()
        self._busy = False
        self._detail_rows: tuple[PreviewDetail, ...] = ()
        self._filtered_detail_rows: tuple[PreviewDetail, ...] = ()
        self._detail_page = 0
        self._detail_page_size = 200
        self.title(TITLE)
        self.geometry("1060x730")
        self.minsize(840, 610)
        self.configure(bg="#f3f6fa")
        self.workbook_label = tk.StringVar(value="فایل اکسل انتخاب نشده است")
        self.manifest_label = tk.StringVar(value="فایل سیاست‌ها/اسناد انتخاب نشده است")
        self.overview = tk.StringVar(value="ابتدا هر دو فایل را انتخاب کنید")
        self.status = tk.StringVar(value="آفلاین | فقط خواندن | بدون صدور یا تأیید")
        self.amount_units = tk.StringVar(value="واحد: طبق داده‌های ورودی | هنوز محاسبه نشده")
        self._configure_styles()
        self._build_menu()
        self._build_tabs()
        self._register_shortcuts()
        self._refresh()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Aram.Title.TLabel", font=("Tahoma", 18, "bold"))
        style.configure("Aram.Banner.TLabel", font=("Tahoma", 10, "bold"),
                        background="#fff4d6", foreground="#76480d", padding=12)
        style.configure("Aram.TButton", font=("Tahoma", 10), padding=(12, 8))
        style.configure("Aram.Treeview", font=("Tahoma", 10), rowheight=28)
        style.configure("Aram.Treeview.Heading", font=("Tahoma", 10, "bold"))

    def _pick_file(self, kind: str) -> str:
        if kind == "workbook":
            return filedialog.askopenfilename(
                parent=self, title="انتخاب اکسل پایلوت",
                filetypes=[("Excel Workbook", "*.xlsx")],
            )
        return filedialog.askopenfilename(
            parent=self, title="انتخاب JSON سیاست‌ها و اسناد",
            filetypes=[("Pipeline JSON", "*.json")],
        )

    def _build_menu(self) -> None:
        menu = tk.Menu(self)
        self.file_menu = tk.Menu(menu, tearoff=0)
        self.file_menu.add_command(
            label="انتخاب اکسل", command=self.select_workbook, accelerator="Ctrl+O",
        )
        self.file_menu.add_command(
            label="انتخاب فایل تنظیمات", command=self.select_manifest, accelerator="Ctrl+M",
        )
        self.file_menu.add_command(
            label="اجرای کنترل", command=self.run_review, accelerator="Ctrl+R",
        )
        self.file_menu.add_command(
            label="پاک‌کردن انتخاب", command=self.clear_selection,
            accelerator="Ctrl+L",
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="خروج", command=self.exit_application, accelerator="Ctrl+Q",
        )
        menu.add_cascade(label="فایل", menu=self.file_menu)
        self.help_menu = tk.Menu(menu, tearoff=0)
        self.help_menu.add_command(
            label="درباره", command=self.show_about, accelerator="F1",
        )
        menu.add_cascade(label="راهنما", menu=self.help_menu)
        self.config(menu=menu)

    def _build_tabs(self) -> None:
        outer = ttk.Frame(self, padding=18)
        outer.pack(fill="both", expand=True)
        ttk.Label(
            outer, text="آرام — بررسی آزمایشی پنج صورت مالی",
            style="Aram.Title.TLabel", anchor="e",
        ).pack(fill="x")
        ttk.Label(
            outer,
            text=(
                "آزمایشی و فاقد مجوز انتشار | فقط پیش‌نمایش حسابداری "
                "بر مبنای فایل‌های ارائه‌شده | بدون ثبت، تأیید یا خروجی رسمی"
            ),
            style="Aram.Banner.TLabel", anchor="e",
        ).pack(fill="x", pady=(12, 16))
        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill="both", expand=True)
        main = ttk.Frame(self.tabs, padding=12)
        figures = ttk.Frame(self.tabs, padding=12)
        details = ttk.Frame(self.tabs, padding=12)
        limitations = ttk.Frame(self.tabs, padding=18)
        help_tab = ttk.Frame(self.tabs, padding=18)
        for tab, title in zip((main, figures, details, limitations, help_tab), TAB_NAMES):
            self.tabs.add(tab, text=title)

        ttk.Label(main, textvariable=self.workbook_label, anchor="e").pack(
            fill="x", pady=(0, 8),
        )
        ttk.Label(main, textvariable=self.manifest_label, anchor="e").pack(
            fill="x", pady=(0, 8),
        )
        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(4, 12))
        self.workbook_button = ttk.Button(
            buttons, text="انتخاب اکسل", command=self.select_workbook,
            style="Aram.TButton",
        )
        self.workbook_button.pack(side="right", padx=4)
        self.manifest_button = ttk.Button(
            buttons, text="انتخاب تنظیمات", command=self.select_manifest,
            style="Aram.TButton",
        )
        self.manifest_button.pack(side="right", padx=4)
        self.run_button = ttk.Button(
            buttons, text="اجرای کنترل پنج صورت مالی", command=self.run_review,
            style="Aram.TButton",
        )
        self.run_button.pack(side="right", padx=4)
        self.clear_button = ttk.Button(
            buttons, text="پاک‌کردن انتخاب", command=self.clear_selection,
            style="Aram.TButton",
        )
        self.clear_button.pack(side="right", padx=4)

        ttk.Label(
            main, textvariable=self.overview, anchor="e",
            font=("Tahoma", 11, "bold"),
        ).pack(fill="x", pady=(0, 8))
        area = ttk.Frame(main)
        area.pack(fill="both", expand=True)
        columns = ("kind", "state", "detail")
        self.outcome_tree = ttk.Treeview(
            area, columns=columns, show="headings", style="Aram.Treeview",
        )
        for key, heading, width in (
            ("kind", "خروجی", 230),
            ("state", "وضعیت", 135),
            ("detail", "توضیح / کد مغایرت", 560),
        ):
            self.outcome_tree.heading(key, text=heading)
            self.outcome_tree.column(
                key, width=width, anchor="e",
                stretch=(key == "detail"),
            )
        scrollbar = ttk.Scrollbar(
            area, orient="vertical", command=self.outcome_tree.yview,
        )
        self.outcome_tree.configure(yscrollcommand=scrollbar.set)
        self.outcome_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(0, weight=1)

        ttk.Label(
            figures,
            text="مبالغ خام پنج صورت مالی — صرفاً نامزد بررسی کارشناسی",
            font=("Tahoma", 11, "bold"), anchor="e",
        ).pack(fill="x", pady=(0, 7))
        ttk.Label(
            figures, textvariable=self.amount_units, anchor="e",
        ).pack(fill="x", pady=(0, 8))
        figure_area = ttk.Frame(figures)
        figure_area.pack(fill="both", expand=True)
        self.figures_tree = ttk.Treeview(
            figure_area, columns=("statement", "label", "amount", "state"),
            show="headings", style="Aram.Treeview",
        )
        for key, title, width in (
            ("statement", "صورت مالی", 190),
            ("label", "شاخص", 220),
            ("amount", "مبلغ (بدون گردکردن)", 200),
            ("state", "اعتبار نتیجه", 230),
        ):
            self.figures_tree.heading(key, text=title)
            self.figures_tree.column(key, width=width, anchor="e")
        figures_scrollbar = ttk.Scrollbar(
            figure_area, orient="vertical", command=self.figures_tree.yview,
        )
        self.figures_tree.configure(yscrollcommand=figures_scrollbar.set)
        self.figures_tree.grid(row=0, column=0, sticky="nsew")
        figures_scrollbar.grid(row=0, column=1, sticky="ns")
        figure_area.grid_columnconfigure(0, weight=1)
        figure_area.grid_rowconfigure(0, weight=1)

        ttk.Label(
            details,
            text="ریز اقلام و ردگیری منبع — فقط خواندنی و غیررسمی",
            font=("Tahoma", 11, "bold"), anchor="e",
        ).pack(fill="x", pady=(0, 7))
        controls = ttk.Frame(details)
        controls.pack(fill="x", pady=(0, 8))
        self.detail_filter_var = tk.StringVar(value="همه")
        self.detail_filter_combo = ttk.Combobox(
            controls, textvariable=self.detail_filter_var, state="readonly",
            values=(
                "همه", "ترازنامه", "سود و زیان",
                "تغییرات حقوق مالکانه", "جریان وجوه نقد", "تراز آزمایشی",
            ),
            width=22,
        )
        self.detail_filter_combo.pack(side="right", padx=4)
        self.detail_filter_combo.bind(
            "<<ComboboxSelected>>", lambda event: self._apply_detail_filter(),
        )
        self.detail_search_var = tk.StringVar(value="")
        self.detail_search_entry = ttk.Entry(
            controls, textvariable=self.detail_search_var, width=28,
        )
        self.detail_search_entry.pack(side="right", padx=4)
        self.detail_search_entry.bind(
            "<Return>", lambda event: self._apply_detail_filter(),
        )
        self.detail_search_button = ttk.Button(
            controls, text="جستجو", command=self._apply_detail_filter,
        )
        self.detail_search_button.pack(side="right", padx=4)
        self.detail_status = tk.StringVar(value="پس از اجرای کنترل، ریز اقلام نمایش داده می‌شود")
        ttk.Label(details, textvariable=self.detail_status, anchor="e").pack(
            fill="x", pady=(0, 6),
        )
        detail_area = ttk.Frame(details)
        detail_area.pack(fill="both", expand=True)
        detail_columns = (
            "statement", "item", "reference", "source", "opening",
            "debit", "credit", "movement", "closing", "trace", "state",
        )
        self.detail_tree = ttk.Treeview(
            detail_area, columns=detail_columns, show="headings",
            style="Aram.Treeview",
        )
        detail_headers = (
            ("statement", "صورت مالی", 150),
            ("item", "شرح / حساب / فعالیت", 190),
            ("reference", "یادداشت / شناسه", 190),
            ("source", "مواجهه / ردیف منبع", 180),
            ("opening", "افتتاحیه / منبع", 130),
            ("debit", "بدهکار / ورودی", 130),
            ("credit", "بستانکار / خروجی", 130),
            ("movement", "تغییر", 130),
            ("closing", "اختتامیه / ارائه", 150),
            ("trace", "مدرک / سیاست / ردگیری", 330),
            ("state", "وضعیت", 160),
        )
        for key, heading, width in detail_headers:
            self.detail_tree.heading(key, text=heading)
            self.detail_tree.column(key, width=width, minwidth=80, anchor="e")
        detail_y = ttk.Scrollbar(
            detail_area, orient="vertical", command=self.detail_tree.yview,
        )
        detail_x = ttk.Scrollbar(
            detail_area, orient="horizontal", command=self.detail_tree.xview,
        )
        self.detail_tree.configure(
            yscrollcommand=detail_y.set, xscrollcommand=detail_x.set,
        )
        self.detail_tree.grid(row=0, column=0, sticky="nsew")
        detail_y.grid(row=0, column=1, sticky="ns")
        detail_x.grid(row=1, column=0, sticky="ew")
        detail_area.grid_columnconfigure(0, weight=1)
        detail_area.grid_rowconfigure(0, weight=1)
        paging = ttk.Frame(details)
        paging.pack(fill="x", pady=(7, 0))
        self.detail_prev_button = ttk.Button(
            paging, text="صفحه قبل", command=lambda: self._change_detail_page(-1),
            state="disabled",
        )
        self.detail_prev_button.pack(side="right", padx=4)
        self.detail_next_button = ttk.Button(
            paging, text="صفحه بعد", command=lambda: self._change_detail_page(1),
            state="disabled",
        )
        self.detail_next_button.pack(side="right", padx=4)

        for item in (
            "• موفقیت آزمون به‌معنای کامل‌بودن سندها، مانده‌ها یا نگاشت‌های حسابداری نیست.",
            "• طبقه‌بندی جریان نقد به ریزاسناد جفت‌شده و فهرست حساب‌های نقد نیاز دارد.",
            "• انتخاب یادداشت‌های نقد و سیاست‌های ارائه در JSON، صرفاً ادعای فایل است.",
            "• تأیید مدیر مالی، کنترل مستقل C1/C2/C3 و قابلیت استناد رسمی وجود ندارد.",
            "• تهیه، امضای دیجیتال، چاپ و صدور PDF/Excel رسمی در این پایلوت غیرفعال است.",
            "• برای اجرای واقعی، کارشناس مسئول باید محرمانگی فایل‌ها را بررسی کند.",
        ):
            ttk.Label(
                limitations, text=item, anchor="e", justify="right",
                wraplength=900, font=("Tahoma", 11),
            ).pack(fill="x", pady=9)
        ttk.Label(
            help_tab, anchor="e", justify="right", wraplength=920,
            font=("Tahoma", 11),
            text=(
                "۱. یک فایل XLSX منطبق با قرارداد Pilot و یک manifest.json "
                "مطابق docs/FIVE_STATEMENT_PIPELINE_CLI.md انتخاب کنید.\n\n"
                "۲. کنترل را اجرا کنید. نتیجه‌ها و کدهای مغایرت فقط در حافظه "
                "نمایش داده می‌شوند و در هیچ فایلی ذخیره نمی‌شوند.\n\n"
                "۳. پاک‌کردن انتخاب، تمام نتایج قبلی را از پنجره پاک می‌کند.\n\n"
                "۴. اجرای موفق فقط مجوز بررسی کارشناسی است؛ "
                "نه صورت مالی قانونی، نه تأیید، نه مجوز چاپ یا صدور."
            ),
        ).pack(fill="x")
        ttk.Label(outer, textvariable=self.status, anchor="e").pack(
            fill="x", pady=(12, 0),
        )

    def _register_shortcuts(self) -> None:
        keys = {
            "<Control-o>": self.select_workbook,
            "<Control-m>": self.select_manifest,
            "<Control-r>": self.run_review,
            "<Control-l>": self.clear_selection,
            "<Control-q>": self.exit_application,
            "<F1>": self.show_about,
        }
        for key, action in keys.items():
            self.bind_all(key, lambda event, callback=action: callback())

    def _refresh(self) -> None:
        if not self.winfo_exists():
            return
        selectable = "disabled" if self._busy else "normal"
        executable = (
            "normal" if self.controller.can_run and not self._busy else "disabled"
        )
        self.workbook_button.configure(state=selectable)
        self.manifest_button.configure(state=selectable)
        self.clear_button.configure(state=selectable)
        self.run_button.configure(state=executable)
        self.detail_filter_combo.configure(state="disabled" if self._busy else "readonly")
        self.detail_search_entry.configure(state=selectable)
        self.detail_search_button.configure(state=selectable)
        for i in (0, 1, 3):
            self.file_menu.entryconfigure(i, state=selectable)
        self.file_menu.entryconfigure(2, state=executable)
        self._render_detail_page()

    def _apply_detail_filter(self) -> None:
        statement = self.detail_filter_var.get()
        query = self.detail_search_var.get().strip().casefold()
        self._filtered_detail_rows = tuple(
            row for row in self._detail_rows
            if (statement == "همه" or row.statement == statement)
            and (not query or query in " ".join(row.values()).casefold())
        )
        self._detail_page = 0
        self._render_detail_page()

    def _render_detail_page(self) -> None:
        if not hasattr(self, "detail_tree") or not self.detail_tree.winfo_exists():
            return
        children = self.detail_tree.get_children()
        if children:
            self.detail_tree.delete(*children)
        total = len(self._filtered_detail_rows)
        pages = max(1, (total + self._detail_page_size - 1) // self._detail_page_size)
        self._detail_page = min(max(0, self._detail_page), pages - 1)
        start = self._detail_page * self._detail_page_size
        end = min(start + self._detail_page_size, total)
        for row in self._filtered_detail_rows[start:end]:
            self.detail_tree.insert("", "end", values=row.values())
        if total:
            self.detail_status.set(
                f"نمایش {start + 1} تا {end} از {total} ردیف | "
                f"صفحه {self._detail_page + 1} از {pages} | هر صفحه حداکثر ۲۰۰ ردیف"
            )
        else:
            self.detail_status.set("ردیفی با این فیلتر پیدا نشد")
        button_state = "disabled" if self._busy else "normal"
        self.detail_prev_button.configure(
            state=(button_state if self._detail_page > 0 else "disabled"),
        )
        self.detail_next_button.configure(
            state=(button_state if self._detail_page + 1 < pages else "disabled"),
        )

    def _change_detail_page(self, delta: int) -> None:
        if self._busy:
            return
        self._detail_page += delta
        self._render_detail_page()

    def _clear_rows(self) -> None:
        for tree in (self.outcome_tree, self.figures_tree, self.detail_tree):
            children = tree.get_children()
            if children:
                tree.delete(*children)
        self._detail_rows = ()
        self._filtered_detail_rows = ()
        self._detail_page = 0
        self.detail_filter_var.set("همه")
        self.detail_search_var.set("")
        self.detail_status.set("پس از اجرای کنترل، ریز اقلام نمایش داده می‌شود")
        self.amount_units.set("واحد: طبق داده‌های ورودی | هنوز محاسبه نشده")
        self._render_detail_page()

    def select_workbook(self) -> None:
        if self._busy:
            return
        selected = self._picker("workbook")
        if not selected:
            return
        try:
            self.controller.select_workbook(selected)
        except DesktopFiveInputError as exc:
            self.workbook_label.set("فایل اکسل معتبر انتخاب نشده است")
            self.status.set(str(exc))
        else:
            self.workbook_label.set(str(self.controller.workbook_path))
            self.status.set("اکسل انتخاب شد؛ کنترل مالی هنوز انجام نشده است")
        self._clear_rows()
        self.overview.set("نتیجه قبلی نامعتبر شد؛ کنترل را دوباره اجرا کنید")
        self._refresh()

    def select_manifest(self) -> None:
        if self._busy:
            return
        selected = self._picker("manifest")
        if not selected:
            return
        try:
            self.controller.select_manifest(selected)
        except DesktopFiveInputError as exc:
            self.manifest_label.set("فایل JSON معتبر انتخاب نشده است")
            self.status.set(str(exc))
        else:
            self.manifest_label.set(str(self.controller.manifest_path))
            self.status.set("تنظیمات انتخاب شد؛ صحت آن هنوز تأیید نشده است")
        self._clear_rows()
        self.overview.set("نتیجه قبلی نامعتبر شد؛ کنترل را دوباره اجرا کنید")
        self._refresh()

    def run_review(self) -> None:
        if self._busy or not self.controller.can_run:
            return
        self._busy = True
        self._clear_rows()
        self.overview.set("کنترل پنج صورت مالی در حال اجراست")
        self.status.set("در حال خواندن امن فایل‌ها؛ هیچ داده‌ای نوشته نمی‌شود")
        generation = self.controller.generation
        self._refresh()

        def worker() -> None:
            try:
                result = self.controller.validate()
            except DesktopFiveInputError as exc:
                self._events.put((generation, None, str(exc)))
            except Exception:
                # Do not disclose a private filesystem or financial traceback.
                self._events.put((generation, None, "INTERNAL_REVIEW_FAILED"))
            else:
                self._events.put((generation, result, None))

        Thread(target=worker, daemon=True).start()
        self.after(80, self._poll)

    def _poll(self) -> None:
        try:
            generation, result, error = self._events.get_nowait()
        except Empty:
            if self._busy:
                self.after(80, self._poll)
            return
        if generation != self.controller.generation:
            self._busy = False
            self._refresh()
            return
        self._busy = False
        if error is not None:
            self.controller.result = None
            self.controller.state = "INPUT_ERROR"
            self._clear_rows()
            self.overview.set("ورودی نامعتبر یا کنترل ناموفق")
            self.status.set("کد خطا: " + error)
        else:
            outcome = result
            try:
                if (
                    outcome.balance_sheet.equity_total
                    != outcome.reconciliation.balance_sheet_equity_total
                    or outcome.income_statement.net_result
                    != outcome.reconciliation.income_statement_net_result
                    or outcome.cash_flow.closing_cash_and_equivalents
                    != outcome.reconciliation.cash_flow_closing_cash
                ):
                    raise CoverageError("DESKTOP_FIGURES_SUMMARY_MISMATCH")
                figure_rows = build_preview_figures(outcome)
            except (CoverageError, AttributeError, TypeError, ValueError):
                # Refuse to render unverified numeric data as a green preview.
                self.controller.result = None
                self.controller.state = "INPUT_ERROR"
                self._clear_rows()
                self.overview.set("نمایش مبالغ نامعتبر؛ پیش‌نمایش مسدود شد")
                self.status.set("DESKTOP_FIGURES_INVALID")
                self._refresh()
                return
            self.amount_units.set(
                "شرکت " + outcome.company_code
                + " | سال " + str(outcome.fiscal_year)
                + " | واحد " + outcome.cash_flow.unit
                + " | ارز " + outcome.cash_flow.currency
                + " | غیررسمی"
            )
            for figure in figure_rows:
                self.figures_tree.insert(
                    "", "end",
                    values=(figure.statement, figure.label,
                            figure.value, figure.state),
                )
            eligible = outcome.eligible_for_analyst_review
            self.overview.set(
                "تطبیق حسابی مناسب بررسی کارشناسی؛ نه تأیید رسمی"
                if eligible else "تطبیق مسدود شد؛ مغایرت‌ها را بررسی کنید"
            )
            for key, label in CANDIDATE_NAMES:
                candidate = getattr(outcome, key)
                approved = (
                    candidate.balanced_for_analyst_review if key == "trial_balance"
                    else candidate.eligible_for_analyst_review
                )
                self.outcome_tree.insert(
                    "", "end", values=(
                        label, "قابل بررسی" if approved else "مسدود",
                        "صرفاً کنترل‌های تحلیلی؛ نه صدور صورت مالی",
                    ),
                )
            for code in outcome.findings[:MAX_VISIBLE_FINDINGS]:
                self.outcome_tree.insert("", "end", values=("مغایرت", "مسدود", code))
            overflow = len(outcome.findings) - MAX_VISIBLE_FINDINGS
            self.status.set(
                ("منبع SHA256: " + outcome.source_sha256[:16] + "… | "
                 + ("نتایج کامل نمایش داده شد" if overflow <= 0
                    else f"{overflow} مغایرت دیگر نمایش داده نشده"))
            )
        self._refresh()

    def clear_selection(self) -> None:
        if self._busy:
            return
        self.controller.clear()
        self.workbook_label.set("فایل اکسل انتخاب نشده است")
        self.manifest_label.set("فایل سیاست‌ها/اسناد انتخاب نشده است")
        self.overview.set("ابتدا هر دو فایل را انتخاب کنید")
        self.status.set("انتخاب و نمایش پاک شد؛ فایل‌های ورودی تغییر نکردند")
        self._clear_rows()
        self._refresh()

    def exit_application(self) -> None:
        self.destroy()

    def show_about(self) -> None:
        self._info(
            "درباره آرام",
            "ARAM Five-Statement Pilot — UNSIGNED / UNRELEASED\n"
            "Read-only local analyst preview. No accounting posting or approval.\n"
            "Not an official financial statement, signed release, or audited source.",
        )


def self_test() -> int:
    ctrl = DesktopFiveStatementController()
    if ctrl.state != "EMPTY" or ctrl.can_run or ctrl.result is not None:
        return 3
    if len(ACTIONS) != 6 or len(CANDIDATE_NAMES) != 5:
        return 4
    return 0


def ui_smoke_test() -> int:
    """Windows-only actual Tk widget smoke against synthetic invalid inputs."""
    with tempfile.TemporaryDirectory() as directory:
        folder = Path(directory)
        xlsx = folder / "synthetic.xlsx"
        manifest = folder / "synthetic.json"
        xlsx.write_bytes(b"not a valid workbook")
        manifest.write_bytes(b"not valid json")
        files = {"workbook": str(xlsx), "manifest": str(manifest)}
        dialogs = []
        window = FiveStatementWindow(
            picker=lambda kind: files[kind],
            info=lambda title, msg: dialogs.append(title),
        )
        try:
            window.withdraw()
            window.update_idletasks()
            if str(window.run_button.cget("state")) != "disabled":
                return 10
            if window.tabs.index("end") != len(TAB_NAMES):
                return 11
            for key in ("<Control-o>", "<Control-m>", "<Control-r>",
                        "<Control-l>", "<Control-q>", "<F1>"):
                if not window.bind_all(key):
                    return 12
            window.workbook_button.invoke()
            window.manifest_button.invoke()
            if not window.controller.can_run:
                return 13
            if str(window.run_button.cget("state")) != "normal":
                return 14
            window.run_button.invoke()
            import time
            for _ in range(400):
                window.update()
                if not window._busy:
                    break
                time.sleep(0.02)
            if window._busy or window.controller.state != "INPUT_ERROR":
                return 15
            window.help_menu.invoke(0)
            if dialogs != ["درباره آرام"]:
                return 16
            window.clear_button.invoke()
            if window.controller.can_run or window.outcome_tree.get_children():
                return 17
            window.file_menu.invoke(5)
            return 0
        finally:
            try:
                if window.winfo_exists():
                    window.destroy()
            except tk.TclError:
                pass


def ui_valid_smoke_test() -> int:
    """Exercise frozen Tk with a truly valid synthetic five-statement input.

    This is an automated widget check, not human review or official approval.
    """
    import time
    with tempfile.TemporaryDirectory() as directory:
        folder = Path(directory)
        workbook = folder / "ARAM-SYNTHETIC-ONLY.xlsx"
        manifest = folder / "ARAM-SYNTHETIC-ONLY.json"
        workbook.write_bytes(source_workbook())
        manifest.write_text(
            json.dumps(pipeline_manifest(), ensure_ascii=True), encoding="utf-8",
        )
        selected = {"workbook": str(workbook), "manifest": str(manifest)}
        window = FiveStatementWindow(picker=lambda kind: selected[kind])
        try:
            window.withdraw()
            window.update_idletasks()
            if str(window.run_button.cget("state")) != "disabled":
                return 20
            window.workbook_button.invoke()
            window.manifest_button.invoke()
            if not window.controller.can_run:
                return 21
            window.run_button.invoke()
            for _ in range(500):
                window.update()
                if not window._busy:
                    break
                time.sleep(0.02)
            if window._busy or window.controller.state != "ELIGIBLE":
                return 22
            if not window.controller.result or not window.controller.result.eligible_for_analyst_review:
                return 23
            rows = window.outcome_tree.get_children()
            if len(rows) != 5:
                return 24
            amount_rows = [
                window.figures_tree.item(row, "values")
                for row in window.figures_tree.get_children()
            ]
            if len(amount_rows) != 28:
                return 28
            if not any(
                row[0] == "سود و زیان" and row[1] == "سود خالص"
                and row[2] == "20" for row in amount_rows
            ):
                return 29
            if any(
                window.outcome_tree.item(row, "values")[1] != "قابل بررسی"
                for row in rows
            ):
                return 25
            window.clear_button.invoke()
            if window.controller.result is not None or window.outcome_tree.get_children():
                return 26
            if str(window.run_button.cget("state")) != "disabled":
                return 27
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
    if args == ["--ui-valid-smoke"]:
        return ui_valid_smoke_test()
    if args:
        print("Supported: --self-test, --ui-smoke, --ui-valid-smoke, or no arguments", file=sys.stderr)
        return 2
    window = FiveStatementWindow()
    window.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
