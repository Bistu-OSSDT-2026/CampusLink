import tkinter as tk
from tkinter import ttk

from src.models.item import LostItem
from src.services.data_service import DataService
from src.utils.config import ITEM_TYPES


class SearchDialog(tk.Toplevel):
    def __init__(self, parent, data_service: DataService):
        super().__init__(parent)
        self.title('搜索物品')
        self.geometry('480x380')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.data_service = data_service
        self.results: list[LostItem] = []
        
        self._colors = {
            'bg_cream': '#FFF5E6',
            'bg_orange': '#E8792B',
            'bg_light_orange': '#FFE4CC',
            'text_brown': '#5D3A1A',
            'text_orange': '#E8792B',
            'text_gray': '#999999',
            'border_color': '#FFD4A3'
        }
        
        self._setup_ui()

    def _setup_ui(self):
        main_frame = tk.Frame(self, bg=self._colors['bg_cream'], padx=25, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            main_frame, text='搜索物品',
            font=('Arial', 16, 'bold'),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_brown']
        )
        title_label.pack(pady=(0, 20))
        
        self._add_input_row(main_frame, '关键词：', '输入物品名称或描述', 'keyword_var')
        self._add_combobox_row(main_frame, '物品类型：', [''] + ITEM_TYPES, 'type_var', True)
        self._add_combobox_row(main_frame, '状态：', ['', 'lost', 'found'], 'status_var', True)
        self._add_input_row(main_frame, '地点：', '输入发现地点', 'location_var')
        
        self._create_buttons(main_frame)

    def _add_input_row(self, parent, label_text, placeholder, var_name):
        row_frame = tk.Frame(parent, bg=self._colors['bg_cream'])
        row_frame.pack(fill=tk.X, pady=8)
        
        label = tk.Label(
            row_frame, text=label_text,
            font=('Arial', 11),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_brown'],
            width=10,
            anchor='w'
        )
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        var = tk.StringVar()
        setattr(self, var_name, var)
        
        entry = tk.Entry(
            row_frame, textvariable=var,
            font=('Arial', 12),
            bg='white',
            fg=self._colors['text_brown'],
            insertbackground=self._colors['text_brown'],
            relief='flat',
            bd=0,
            highlightthickness=2,
            highlightcolor=self._colors['bg_orange'],
            highlightbackground=self._colors['border_color'],
            width=30
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self._apply_placeholder(entry, var, placeholder)

    def _add_combobox_row(self, parent, label_text, values, var_name, is_empty_first):
        row_frame = tk.Frame(parent, bg=self._colors['bg_cream'])
        row_frame.pack(fill=tk.X, pady=8)
        
        label = tk.Label(
            row_frame, text=label_text,
            font=('Arial', 11),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_brown'],
            width=10,
            anchor='w'
        )
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        var = tk.StringVar(value='')
        setattr(self, var_name, var)
        
        combobox = ttk.Combobox(
            row_frame, textvariable=var,
            values=values,
            state='readonly',
            font=('Arial', 12),
            width=28
        )
        combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                        fieldbackground='white',
                        background='white',
                        foreground=self._colors['text_brown'])

    def _apply_placeholder(self, entry, var, placeholder):
        var.set(placeholder)
        entry.config(fg=self._colors['text_gray'])
        
        def on_focus_in(event):
            if var.get() == placeholder:
                var.set('')
                entry.config(fg=self._colors['text_brown'])
        
        def on_focus_out(event):
            if not var.get():
                var.set(placeholder)
                entry.config(fg=self._colors['text_gray'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def _create_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg=self._colors['bg_cream'])
        btn_frame.pack(fill=tk.X, pady=(25, 0))
        
        search_btn = tk.Button(
            btn_frame, text='搜索', command=self._search,
            font=('Arial', 12, 'bold'),
            bg=self._colors['bg_orange'],
            fg='white',
            padx=30,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        cancel_btn = tk.Button(
            btn_frame, text='取消', command=self.destroy,
            font=('Arial', 12),
            bg='white',
            fg=self._colors['text_brown'],
            padx=30,
            pady=8,
            relief='solid',
            borderwidth=1,
            bordercolor=self._colors['border_color'],
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)

    def _search(self):
        keyword = self.keyword_var.get().strip()
        if keyword == '输入物品名称或描述':
            keyword = ''
        
        item_type = self.type_var.get()
        status = self.status_var.get()
        
        location = self.location_var.get().strip()
        if location == '输入发现地点':
            location = ''
        
        self.results = self.data_service.search_items(
            keyword=keyword,
            item_type=item_type,
            status=status,
            location=location
        )
        
        self.destroy()