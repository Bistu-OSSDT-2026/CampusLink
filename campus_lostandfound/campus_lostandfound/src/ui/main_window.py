import tkinter as tk
from tkinter import ttk, messagebox

from src.models.item import LostItem
from src.services.data_service import DataService
from src.ui.post_dialog import PostDialog
from src.ui.search_dialog import SearchDialog
from src.utils.config import APP_TITLE, APP_WIDTH, APP_HEIGHT, STATUS_OPTIONS


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
        self.resizable(True, True)
        
        self.data_service = DataService()
        self.selected_item_id = None
        
        self._setup_colors()
        self._setup_ui()
        self._load_items()

    def _setup_colors(self):
        self.bg_cream_start = '#FFF8E7'
        self.bg_cream_end = '#FFF5E6'
        self.bg_orange = '#E8792B'
        self.bg_orange_dark = '#D46820'
        self.bg_light_orange = '#FFE4CC'
        self.bg_card = '#FFFFFF'
        self.text_brown = '#5D3A1A'
        self.text_orange = '#E8792B'
        self.text_gray = '#6B6B6B'
        self.text_light_gray = '#999999'
        self.border_color = '#FFD4A3'

    def _setup_ui(self):
        self._create_gradient_background()
        self._create_menu()
        self._create_header()
        self._create_toolbar()
        self._create_card_list()
        self._create_status_bar()
        self._add_decorations()

    def _create_gradient_background(self):
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        width = APP_WIDTH
        height = APP_HEIGHT
        steps = 20
        
        for i in range(steps):
            ratio = i / steps
            r = int(255 * (1 - ratio * 0.02))
            g = int(248 * (1 - ratio * 0.03))
            b = int(231 * (1 - ratio * 0.05))
            color = f'#{r:02X}{g:02X}{b:02X}'
            
            y1 = int(height * (i / steps))
            y2 = int(height * ((i + 1) / steps))
            self.canvas.create_rectangle(0, y1, width, y2, fill=color, outline='')

    def _create_menu(self):
        menubar = tk.Menu(self, bg=self.bg_cream_end, fg=self.text_brown, font=('Arial', 10))
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_cream_end, fg=self.text_brown, font=('Arial', 10))
        file_menu.add_command(label='发布失物信息', command=self._open_post_dialog)
        file_menu.add_separator()
        file_menu.add_command(label='退出', command=self.quit)
        menubar.add_cascade(label='文件', menu=file_menu)
        
        search_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_cream_end, fg=self.text_brown, font=('Arial', 10))
        search_menu.add_command(label='搜索', command=self._open_search_dialog)
        search_menu.add_command(label='刷新列表', command=self._load_items)
        menubar.add_cascade(label='操作', menu=search_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_cream_end, fg=self.text_brown, font=('Arial', 10))
        help_menu.add_command(label='使用帮助', command=self._show_help)
        help_menu.add_command(label='关于', command=self._show_about)
        menubar.add_cascade(label='帮助', menu=help_menu)
        
        self.config(menu=menubar)

    def _create_header(self):
        header_frame = tk.Frame(self, bg=self.bg_cream_end, padx=25, pady=15)
        self.canvas.create_window(0, 0, anchor='nw', window=header_frame)
        
        header_inner = tk.Frame(header_frame, bg=self.bg_cream_end)
        header_inner.pack(fill=tk.X, anchor='w')
        
        title_row = tk.Frame(header_inner, bg=self.bg_cream_end)
        title_row.pack(anchor='w')
        
        icon_canvas = tk.Canvas(title_row, width=40, height=40, bg=self.bg_cream_end, highlightthickness=0)
        icon_canvas.pack(side=tk.LEFT, padx=(0, 12))
        self._draw_campus_icon(icon_canvas)
        
        title_label = tk.Label(
            title_row, 
            text='北京信息科技大学', 
            font=('Arial', 20, 'bold'),
            bg=self.bg_cream_end,
            fg=self.text_brown,
            anchor='w'
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header_inner, 
            text='校园失物招领系统', 
            font=('Arial', 12),
            bg=self.bg_cream_end,
            fg=self.text_orange,
            anchor='w'
        )
        subtitle_label.pack(anchor='w', pady=(4, 0))
        
        sep_frame = tk.Frame(header_inner, bg=self.bg_orange, height=2)
        sep_frame.pack(fill=tk.X, pady=(10, 0))
        
        decor_canvas = tk.Canvas(header_inner, height=8, bg=self.bg_cream_end, highlightthickness=0)
        decor_canvas.pack(fill=tk.X, pady=(5, 0))
        self._draw_decor_line(decor_canvas)

    def _draw_campus_icon(self, canvas):
        canvas.create_polygon(20, 5, 35, 25, 5, 25, fill=self.bg_orange, outline='')
        canvas.create_rectangle(15, 25, 25, 35, fill=self.bg_light_orange, outline='')
        canvas.create_rectangle(17, 27, 23, 33, fill=self.text_brown, outline='')

    def _draw_decor_line(self, canvas):
        canvas.create_line(0, 4, 60, 4, fill=self.bg_light_orange, width=2)
        canvas.create_line(80, 4, 140, 4, fill=self.bg_light_orange, width=2)
        canvas.create_line(160, 4, 220, 4, fill=self.bg_light_orange, width=2)
        
        canvas.create_oval(30, 2, 34, 6, fill=self.bg_orange)
        canvas.create_oval(110, 2, 114, 6, fill=self.bg_orange)
        canvas.create_oval(190, 2, 194, 6, fill=self.bg_orange)

    def _create_toolbar(self):
        toolbar = tk.Frame(self, bg=self.bg_cream_end, padx=15, pady=8)
        self.canvas.create_window(0, 60, anchor='nw', window=toolbar)
        
        btn_style = {'font': ('Arial', 11), 'padx': 15, 'pady': 6, 'cursor': 'hand2'}
        
        self.btn_post = tk.Button(
            toolbar, text='发布失物', command=self._open_post_dialog,
            bg=self.bg_orange, fg='white', **btn_style, relief='flat'
        )
        self.btn_post.pack(side=tk.LEFT, padx=5)
        self._add_hover_effect(self.btn_post, self.bg_orange, self.bg_orange_dark)
        
        self.btn_search = tk.Button(
            toolbar, text='搜索', command=self._open_search_dialog,
            bg='white', fg=self.text_brown, **btn_style, relief='solid', borderwidth=1
        )
        self.btn_search.pack(side=tk.LEFT, padx=5)
        self._add_hover_effect(self.btn_search, 'white', '#FFFAF0')
        
        self.btn_refresh = tk.Button(
            toolbar, text='刷新', command=self._load_items,
            bg='white', fg=self.text_brown, **btn_style, relief='solid', borderwidth=1
        )
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        self._add_hover_effect(self.btn_refresh, 'white', '#FFFAF0')
        
        self.btn_mark_found = tk.Button(
            toolbar, text='标记已找到', command=self._mark_selected_found,
            bg='white', fg=self.text_brown, **btn_style, relief='solid', borderwidth=1
        )
        self.btn_mark_found.pack(side=tk.LEFT, padx=5)
        self._add_hover_effect(self.btn_mark_found, 'white', '#FFFAF0')
        
        self.btn_delete = tk.Button(
            toolbar, text='删除', command=self._delete_selected,
            bg='white', fg='#C44536', **btn_style, relief='solid', borderwidth=1
        )
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        self._add_hover_effect(self.btn_delete, 'white', '#FFF5F5')

    def _add_hover_effect(self, button, normal_color, hover_color):
        def on_enter(event):
            button.config(bg=hover_color)
            button.pack_configure(padx=4)
            
        def on_leave(event):
            button.config(bg=normal_color)
            button.pack_configure(padx=5)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def _create_card_list(self):
        self.card_frame = tk.Frame(self, bg=self.bg_cream_start)
        self.canvas.create_window(0, 110, anchor='nw', window=self.card_frame, width=APP_WIDTH)
        
        self.scroll_canvas = tk.Canvas(self.card_frame, bg=self.bg_cream_start, highlightthickness=0)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.card_frame, orient=tk.VERTICAL, command=self.scroll_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.items_container = tk.Frame(self.scroll_canvas, bg=self.bg_cream_start)
        self.scroll_canvas.create_window(0, 0, anchor='nw', window=self.items_container)
        
        self.items_container.bind('<Configure>', lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all')))
        
        self.scroll_canvas.bind('<MouseWheel>', self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def _create_item_card(self, item):
        card = tk.Frame(
            self.items_container, 
            bg=self.bg_card,
            padx=15,
            pady=12
        )
        card.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        shadow_frame = tk.Frame(card, bg=self.bg_light_orange)
        shadow_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)
        
        card.bind('<Button-1>', lambda e, id=item.item_id: self._select_card(id, card))
        card.bind('<Double-1>', lambda e, id=item.item_id: self._show_item_detail_by_id(id))
        
        top_row = tk.Frame(card, bg=self.bg_card)
        top_row.pack(fill=tk.X)
        
        name_label = tk.Label(
            top_row, text=item.item_name,
            font=('Arial', 14, 'bold'),
            bg=self.bg_card,
            fg=self.text_brown
        )
        name_label.pack(side=tk.LEFT)
        
        type_label = tk.Label(
            top_row, text=item.item_type,
            font=('Arial', 10),
            bg=self.bg_light_orange,
            fg=self.text_orange,
            padx=6,
            pady=2
        )
        type_label.pack(side=tk.LEFT, padx=10)
        
        status_label = tk.Label(
            top_row, 
            text='已找到' if item.status == 'found' else '丢失中',
            font=('Arial', 10, 'bold'),
            bg='#D4EDDA' if item.status == 'found' else '#FFF3CD',
            fg='#155724' if item.status == 'found' else '#856404',
            padx=8,
            pady=2
        )
        status_label.pack(side=tk.RIGHT)
        
        desc_label = tk.Label(
            card, text=item.description if item.description else '暂无描述',
            font=('Arial', 11),
            bg=self.bg_card,
            fg=self.text_gray,
            anchor='w',
            wraplength=700
        )
        desc_label.pack(fill=tk.X, pady=(5, 5), anchor='w')
        
        bottom_row = tk.Frame(card, bg=self.bg_card)
        bottom_row.pack(fill=tk.X, pady=(5, 0))
        
        loc_label = tk.Label(
            bottom_row, text=f'📍 {item.location}',
            font=('Arial', 10),
            bg=self.bg_card,
            fg=self.text_light_gray
        )
        loc_label.pack(side=tk.LEFT)
        
        contact_label = tk.Label(
            bottom_row, text=f'👤 {item.contact_name}',
            font=('Arial', 10),
            bg=self.bg_card,
            fg=self.text_light_gray
        )
        contact_label.pack(side=tk.LEFT, padx=15)
        
        time_label = tk.Label(
            bottom_row, text=f'🕐 {item.report_time}',
            font=('Arial', 10),
            bg=self.bg_card,
            fg=self.text_light_gray
        )
        time_label.pack(side=tk.RIGHT)

    def _select_card(self, item_id, card):
        self.selected_item_id = item_id
        
        for child in self.items_container.winfo_children():
            child.config(bg=self.bg_card)
            for sub in child.winfo_children():
                if isinstance(sub, tk.Frame) and sub != card:
                    sub.config(bg=self.bg_light_orange)
        
        card.config(bg=self.bg_light_orange)

    def _create_status_bar(self):
        self.status_var = tk.StringVar(value='就绪')
        status_bar = tk.Label(
            self, textvariable=self.status_var, 
            bg=self.bg_cream_end, fg=self.text_brown,
            font=('Arial', 10),
            relief=tk.FLAT, anchor=tk.W,
            padx=15, pady=5
        )
        self.canvas.create_window(0, APP_HEIGHT - 30, anchor='sw', window=status_bar, width=APP_WIDTH)

    def _add_decorations(self):
        decor_frame = tk.Frame(self, bg=self.bg_cream_end)
        self.canvas.create_window(APP_WIDTH - 100, 60, anchor='ne', window=decor_frame)
        
        decor_canvas = tk.Canvas(decor_frame, width=80, height=40, bg=self.bg_cream_end, highlightthickness=0)
        decor_canvas.pack()
        
        decor_canvas.create_arc(10, 10, 30, 30, start=0, extent=180, fill=self.bg_light_orange, outline='')
        decor_canvas.create_oval(50, 10, 70, 30, fill=self.bg_orange, outline='')
        decor_canvas.create_oval(55, 15, 65, 25, fill='white', outline='')

    def _load_items(self, items=None):
        for child in self.items_container.winfo_children():
            child.destroy()
        
        self.selected_item_id = None
        
        if items is None:
            items = self.data_service.get_all_items()
        
        if not items:
            empty_label = tk.Label(
                self.items_container, 
                text='暂无失物信息，点击「发布失物」添加',
                font=('Arial', 14),
                bg=self.bg_cream_start,
                fg=self.text_light_gray,
                padx=20,
                pady=60
            )
            empty_label.pack()
        else:
            for item in items:
                self._create_item_card(item)
        
        self.status_var.set(f'共 {len(items)} 条记录')

    def _open_post_dialog(self):
        dialog = PostDialog(self, self.data_service)
        self.wait_window(dialog)
        self._load_items()

    def _open_search_dialog(self):
        dialog = SearchDialog(self, self.data_service)
        self.wait_window(dialog)
        if dialog.results:
            self._load_items(dialog.results)

    def _show_item_detail(self, event):
        pass

    def _show_item_detail_by_id(self, item_id):
        item = self.data_service.get_item_by_id(item_id)
        
        if item:
            detail = f"物品名称: {item.item_name}\n"
            detail += f"物品类型: {item.item_type}\n"
            detail += f"详细描述: {item.description}\n"
            detail += f"发现地点: {item.location}\n"
            detail += f"联系人: {item.contact_name}\n"
            detail += f"联系电话: {item.contact_phone}\n"
            detail += f"发布时间: {item.report_time}\n"
            detail += f"状态: {'已找到' if item.status == 'found' else '丢失中'}"
            messagebox.showinfo('物品详情', detail)

    def _mark_selected_found(self):
        if not self.selected_item_id:
            messagebox.showwarning('提示', '请先选择一条记录')
            return
        
        item = self.data_service.get_item_by_id(self.selected_item_id)
        
        if item:
            if item.status == 'found':
                messagebox.showinfo('提示', '该物品已经是已找到状态')
                return
            
            item.mark_found()
            self.data_service.update_item(item)
            self._load_items()
            messagebox.showinfo('提示', '已标记为已找到')

    def _delete_selected(self):
        if not self.selected_item_id:
            messagebox.showwarning('提示', '请先选择一条记录')
            return
        
        item = self.data_service.get_item_by_id(self.selected_item_id)
        
        if item and messagebox.askyesno('确认删除', f'确定要删除「{item.item_name}」这条记录吗？'):
            self.data_service.delete_item(self.selected_item_id)
            self._load_items()
            messagebox.showinfo('提示', '删除成功')

    def _show_help(self):
        help_text = """校园失物招领平台使用说明：

1. 发布失物信息：
   - 点击"发布失物"按钮
   - 填写物品名称、类型、描述等信息
   - 填写联系人信息
   - 点击"发布"保存

2. 搜索物品：
   - 点击"搜索"按钮
   - 输入关键词、选择类型或状态
   - 点击"搜索"查看结果

3. 标记已找到：
   - 在列表中选中一条记录
   - 点击"标记已找到"按钮

4. 删除记录：
   - 在列表中选中一条记录
   - 点击"删除"按钮确认删除

5. 查看详情：
   - 双击列表中的记录查看详细信息
"""
        messagebox.showinfo('使用帮助', help_text)

    def _show_about(self):
        about_text = """校园失物招领平台 v1.0

开发团队：5人小组
技术栈：Python + Tkinter
数据存储：本地JSON文件

本工具旨在帮助校园内失物招领信息的发布与查询，
方便失主找回遗失物品。
"""
        messagebox.showinfo('关于', about_text)

    def run(self):
        self.mainloop()