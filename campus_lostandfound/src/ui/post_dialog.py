import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from src.models.item import LostItem
from src.services.data_service import DataService
from src.utils.config import ITEM_TYPES


class PostDialog(tk.Toplevel):
    def __init__(self, parent, data_service: DataService):
        super().__init__(parent)
        self.title('发布失物信息')
        self.geometry('520x600')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.data_service = data_service
        
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
            main_frame, text='发布失物信息',
            font=('Arial', 16, 'bold'),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_brown']
        )
        title_label.pack(pady=(0, 20))
        
        item_section = tk.Frame(main_frame, bg=self._colors['bg_cream'])
        item_section.pack(fill=tk.X, pady=(0, 15))
        
        self._add_separator(main_frame, 15)
        
        basic_section = tk.Frame(main_frame, bg=self._colors['bg_cream'])
        basic_section.pack(fill=tk.X, pady=(15, 15))
        
        self._add_separator(main_frame, 15)
        
        contact_section = tk.Frame(main_frame, bg=self._colors['bg_cream'])
        contact_section.pack(fill=tk.X, pady=(15, 0))
        
        self._create_item_inputs(item_section)
        self._create_basic_inputs(basic_section)
        self._create_contact_inputs(contact_section)
        
        self._create_buttons(main_frame)

    def _add_separator(self, parent, pady):
        sep = tk.Frame(parent, bg=self._colors['bg_light_orange'], height=3)
        sep.pack(fill=tk.X, pady=pady)

    def _create_item_inputs(self, parent):
        section_title = tk.Label(
            parent, text='物品信息',
            font=('Arial', 12, 'bold'),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_orange']
        )
        section_title.pack(anchor='w', pady=(0, 12))
        
        self._add_input_row(parent, '物品名称：', '请输入物品名称', 'name_var')
        self._add_combobox_row(parent, '物品类型：', ITEM_TYPES, 'type_var')
        self._add_text_row(parent, '详细描述：', '请描述物品特征...', 'desc_text')

    def _create_basic_inputs(self, parent):
        section_title = tk.Label(
            parent, text='发现信息',
            font=('Arial', 12, 'bold'),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_orange']
        )
        section_title.pack(anchor='w', pady=(0, 12))
        
        self._add_input_row(parent, '发现地点：', '请输入发现地点', 'location_var')

    def _create_contact_inputs(self, parent):
        section_title = tk.Label(
            parent, text='联系信息',
            font=('Arial', 12, 'bold'),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_orange']
        )
        section_title.pack(anchor='w', pady=(0, 12))
        
        self._add_input_row(parent, '联系人：', '请输入联系人姓名', 'contact_name_var')
        self._add_input_row(parent, '联系电话：', '请输入11位手机号', 'contact_phone_var')

    def _add_input_row(self, parent, label_text, placeholder, var_name):
        row_frame = tk.Frame(parent, bg=self._colors['bg_cream'])
        row_frame.pack(fill=tk.X, pady=6)
        
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
            width=35
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self._apply_placeholder(entry, var, placeholder)

    def _add_combobox_row(self, parent, label_text, values, var_name):
        row_frame = tk.Frame(parent, bg=self._colors['bg_cream'])
        row_frame.pack(fill=tk.X, pady=6)
        
        label = tk.Label(
            row_frame, text=label_text,
            font=('Arial', 11),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_brown'],
            width=10,
            anchor='w'
        )
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        var = tk.StringVar(value=values[0])
        setattr(self, var_name, var)
        
        combobox = ttk.Combobox(
            row_frame, textvariable=var,
            values=values,
            state='readonly',
            font=('Arial', 12),
            width=33
        )
        combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                        fieldbackground='white',
                        background='white',
                        foreground=self._colors['text_brown'])

    def _add_text_row(self, parent, label_text, placeholder, var_name):
        row_frame = tk.Frame(parent, bg=self._colors['bg_cream'])
        row_frame.pack(fill=tk.X, pady=6)
        
        label = tk.Label(
            row_frame, text=label_text,
            font=('Arial', 11),
            bg=self._colors['bg_cream'],
            fg=self._colors['text_brown'],
            width=10,
            anchor='w'
        )
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        text_frame = tk.Frame(row_frame, bg='white', highlightthickness=2, 
                              highlightcolor=self._colors['bg_orange'], 
                              highlightbackground=self._colors['border_color'])
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        text = tk.Text(text_frame, font=('Arial', 12), bg='white', 
                      fg=self._colors['text_brown'], relief='flat', bd=0,
                      wrap=tk.WORD, height=4, width=30)
        text.pack(fill=tk.X, expand=True, padx=5, pady=5)
        setattr(self, var_name, text)
        
        text.insert('1.0', placeholder)
        text.tag_add('placeholder', '1.0', 'end')
        text.tag_config('placeholder', foreground=self._colors['text_gray'])
        
        def on_focus_in(event):
            if text.get('1.0', 'end-1c') == placeholder:
                text.delete('1.0', 'end')
                text.tag_remove('placeholder', '1.0', 'end')
        
        def on_focus_out(event):
            if not text.get('1.0', 'end-1c'):
                text.insert('1.0', placeholder)
                text.tag_add('placeholder', '1.0', 'end')
        
        text.bind('<FocusIn>', on_focus_in)
        text.bind('<FocusOut>', on_focus_out)

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
        
        submit_btn = tk.Button(
            btn_frame, text='发布', command=self._submit,
            font=('Arial', 12, 'bold'),
            bg=self._colors['bg_orange'],
            fg='white',
            padx=30,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        submit_btn.pack(side=tk.LEFT, padx=(0, 15))
        
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

    def _validate_input(self) -> bool:
        if self.name_var.get() in ('', '请输入物品名称'):
            messagebox.showwarning('输入错误', '请填写物品名称')
            return False
        
        if self.location_var.get() in ('', '请输入发现地点'):
            messagebox.showwarning('输入错误', '请填写发现地点')
            return False
        
        if self.contact_name_var.get() in ('', '请输入联系人姓名'):
            messagebox.showwarning('输入错误', '请填写联系人')
            return False
        
        phone = self.contact_phone_var.get().strip()
        if phone in ('', '请输入11位手机号'):
            messagebox.showwarning('输入错误', '请填写联系电话')
            return False
        
        if not phone.isdigit() or len(phone) != 11:
            messagebox.showwarning('输入错误', '请输入有效的11位手机号')
            return False
        
        return True

    def _submit(self):
        if not self._validate_input():
            return
        
        description = self.desc_text.get('1.0', tk.END).strip()
        if description == '请描述物品特征...':
            description = ''
        
        item = LostItem(
            item_id=self.data_service.generate_id(),
            item_name=self.name_var.get().strip(),
            item_type=self.type_var.get(),
            description=description,
            location=self.location_var.get().strip(),
            contact_name=self.contact_name_var.get().strip(),
            contact_phone=self.contact_phone_var.get().strip(),
            report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            status='lost'
        )
        
        self.data_service.add_item(item)
        messagebox.showinfo('成功', '发布成功！')
        self.destroy()